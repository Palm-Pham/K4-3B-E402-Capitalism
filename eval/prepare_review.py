"""Create blank human-review worksheets without inventing ratings."""
import csv
import json
from sync_sample_eval import HERE, build_pilot_cases, load_sample

if __name__ == '__main__':
    cases = build_pilot_cases(load_sample())
    (HERE/'pilot_inputs.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
    for name, ids in [('pilot_review.csv',[c['id'] for c in cases]),
                      ('rater_a.csv',[c['id'] for c in cases[:5]]),
                      ('rater_b.csv',[c['id'] for c in cases[:5]])]:
        path=HERE/name
        if path.exists():
            continue  # Never overwrite human annotations.
        with path.open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['id','trace_id','reviewer','grade','error_group','notes'])
            writer.writeheader()
            writer.writerows({'id':i} for i in ids)
