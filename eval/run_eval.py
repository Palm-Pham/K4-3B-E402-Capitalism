"""Reproducible live evaluation; never substitutes canned model responses."""
import argparse
import collections
import csv
import hashlib
import itertools
import json
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from codebase.agent import classify_context
HERE = Path(__file__).parent


def check_case(case, result):
    if result['error'] or not result['api_called']:
        return None, ['infrastructure:' + (result['error'] or 'no_live_api_call')]
    exp = case['expected']
    errors = []
    if result['status'] != exp['status']:
        errors.append('wrong_status')
    if result['action'] != exp['action']:
        errors.append('wrong_action')
    if set(result['missing']) != set(exp['missing']):
        errors.append('wrong_missing_fields')
    if exp['status'] != 'MISSING_CONTEXT' and result['reply']:
        errors.append('unwanted_reply')
    if result['reply'] and len(result['reply'].split()) > 100:
        errors.append('reply_too_long')
    return not errors, errors


def coverage(cases):
    counts = collections.Counter(t for c in cases for t in c['taxonomy'])
    groups = collections.Counter(c['difficulty'] for c in cases)
    real = sum(c['source_type'] == 'adapted_real_discord_chatlog' for c in cases)
    assert len(cases) >= 20 and len({c['id'] for c in cases}) == len(cases)
    assert all(counts[t] >= 2 for t in (1,2,3,4)) and real >= 10
    assert 8 <= groups['common'] <= 10 and 2 <= groups['rare'] <= 4
    dims = list(cases[0]['grid'])
    with (HERE / 'input_grid.csv').open('w', encoding='utf-8-sig', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=['id'] + dims)
        writer.writeheader()
        writer.writerows({'id': c['id'], **c['grid']} for c in cases)
    # Explicit pairwise empty cells; some combinations are intentionally inapplicable.
    gaps = []
    for a,b in itertools.combinations(dims, 2):
        seen = {(c['grid'][a], c['grid'][b]) for c in cases}
        for x,y in itertools.product(sorted({c['grid'][a] for c in cases}), sorted({c['grid'][b] for c in cases})):
            if (x,y) not in seen:
                gaps.append({'dimension_1':a, 'value_1':x, 'dimension_2':b, 'value_2':y,
                             'review':'uncovered_or_inapplicable_requires_review'})
    (HERE / 'coverage_gaps.json').write_text(json.dumps(gaps, ensure_ascii=False, indent=2), encoding='utf-8')
    return {'total':len(cases), 'real_derived':real, 'taxonomy':dict(counts), 'groups':dict(groups),
            'empty_pairwise_cells':len(gaps), 'not_covered':['readable images','multi-turn context',
            'edited messages','TA takeover','dismissal','Discord restart/dedup integration']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--coverage-only', action='store_true')
    parser.add_argument('--pilot', action='store_true')
    args = parser.parse_args()
    path = HERE / ('pilot_inputs.json' if args.pilot else 'golden_set_cp3.json')
    cases = json.loads(path.read_text(encoding='utf-8'))
    cov = None if args.pilot else coverage(cases)
    if args.coverage_only:
        print(json.dumps(cov, ensure_ascii=False, indent=2))
        return
    run_id = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    rows = []
    for case in cases:
        result = classify_context(**case['input'])
        passed, failures = (None, []) if args.pilot else check_case(case, result)
        rows.append({'id': case['id'], 'result': result, 'passed': passed, 'failures': failures,
                     'human_grade': None, 'human_notes': None})
        print(case['id'], result['status'], result['error'] or 'completed', flush=True)
    completed = sum(r['result']['api_called'] and not r['result']['error'] for r in rows)
    passed = sum(r['passed'] is True for r in rows)
    failed = sum(r['passed'] is False for r in rows)
    blocked = len(rows) - completed
    predicted_ask = sum(r['result']['action'] == 'ASK_FOR_CONTEXT' and not r['result']['error'] for r in rows)
    true_ask = sum(r['result']['action'] == 'ASK_FOR_CONTEXT' and not r['result']['error'] and
                   c.get('expected',{}).get('action') == 'ASK_FOR_CONTEXT' for c,r in zip(cases,rows))
    expected_ask = sum(c.get('expected',{}).get('action') == 'ASK_FOR_CONTEXT' for c in cases)
    report = {'run_id':run_id, 'mode':'pilot' if args.pilot else 'live',
              'label_status':'provisional', 'dataset_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
              'status':'blocked' if not completed else ('partial' if blocked else 'completed'),
              'attempted':len(rows), 'model_completed':completed, 'passed':passed, 'failed':failed,
              'blocked':blocked, 'pass_rate_percent':round(100*passed/completed,2) if completed and not args.pilot else None,
              'end_to_end_pass_percent':round(100*passed/len(rows),2) if completed and not args.pilot else None,
              'ask_precision':true_ask/predicted_ask if predicted_ask and not args.pilot else None,
              'ask_recall':true_ask/expected_ask if expected_ask and completed and not args.pilot else None,
              'coverage':cov, 'results':rows}
    directory = HERE / 'private-runs'
    directory.mkdir(exist_ok=True)
    prefix = 'pilot' if args.pilot else 'run'
    (directory / f'{prefix}-{run_id}.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (HERE / f'latest_{prefix}.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = [f'# CP3 {prefix} — {run_id}', '', 'Nhãn hiện là bản nháp, chưa có hai thành viên chấm độc lập.', '',
             '| Chỉ số | Kết quả |','|---|---|', f'| Case thử | {len(rows)} |', f'| Model hoàn tất | {completed} |',
             f'| Đạt | {passed} |',f'| Sai | {failed} |', f'| Bị chặn / lỗi hạ tầng | {blocked} |',
             f'| Tỷ lệ đạt trên model hoàn tất | {report["pass_rate_percent"] if report["pass_rate_percent"] is not None else "N/A — chưa đo"} |',
             '', '## Phân tích từng case', '', '| Case | Kết quả | Nguyên nhân |','|---|---|']
    for row in rows:
        state = 'BLOCKED' if row['result']['error'] else ('PENDING HUMAN REVIEW' if args.pilot else ('PASS' if row['passed'] else 'FAIL'))
        lines.append(f'| {row["id"]} | {state} | {row["result"]["error"] or ", ".join(row["failures"]) or "khớp rubric tự động; cần TA review"} |')
    lines += ['', '## Giới hạn', '', 'Không tính fallback UNCERTAIN do lỗi API là dự đoán đúng. '
              'Unit test dùng test double không phải số đo AI. Chưa chấm độc lập, chưa có video gọi AI thật nếu model chưa hoàn tất. '
              'Case sai status: xem trace prompt/output; sai missing: đối chiếu thông tin đã có, trường cần thiết và nhãn TA. '
              'Không sửa nhãn để tăng điểm. Không suy ra chất lượng thực tế chỉ từ schema hợp lệ.']
    (HERE / f'latest_{prefix}.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('results','coverage')}, ensure_ascii=False))
    if not completed:
        sys.exit(2)


if __name__ == '__main__':
    main()
