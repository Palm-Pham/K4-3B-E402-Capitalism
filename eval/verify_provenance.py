"""Verify source IDs in a local data pack without copying its contents."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source_csv', type=Path)
    args=parser.parse_args()
    root=Path(__file__).parent
    cases=json.loads((root/'golden_set_cp3.json').read_text(encoding='utf-8'))
    with args.source_csv.open(encoding='utf-8-sig',newline='') as f:
        sources={r['msg_id']:r for r in csv.DictReader(f)}
    verified=[]
    for case in cases:
        if not case['source_message_id']:
            continue
        source=sources[case['source_message_id']]
        assert source['is_bot'].lower()=='false'
        assert int(source['n_attachments'])==len(case['input']['attachments'])
        verified.append({'case_id':case['id'],'msg_id':source['msg_id'],
                         'source_text_sha256':hashlib.sha256(source['content'].encode()).hexdigest(),
                         'original_attachments':int(source['n_attachments']),
                         'method':'ID/attachment checks plus author inspection; paraphrase is not an original quote'})
    report={'source':'data/discord-pack/k4_messages.csv',
            'source_sha256':hashlib.sha256(args.source_csv.read_bytes()).hexdigest(),
            'verified_count':len(verified),'cases':verified}
    (root/'provenance_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Verified {len(verified)} source IDs. No source contents copied.')
