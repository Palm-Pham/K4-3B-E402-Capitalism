"""Build evaluation inputs from the annotation-focused sample message set."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / 'data' / 'sample_messages.json'
HERE = Path(__file__).parent


def load_sample():
    return json.loads(SAMPLE_PATH.read_text(encoding='utf-8'))


def build_legacy_cases(messages):
    return [
        {key: item[key] for key in ('message', 'label', 'missing')}
        | ({'flags': item['flags']} if 'flags' in item else {})
        for item in messages
    ]


def build_pilot_cases(messages, per_label=3):
    selected = []
    counts = {}
    for item in messages:
        label = item['label']
        if counts.get(label, 0) >= per_label:
            continue
        counts[label] = counts.get(label, 0) + 1
        selected.append({'id': f'PILOT-{len(selected) + 1:02}',
                         'source_type': 'synthetic',
                         'input': {'message': item['message'], 'attachments': []}})
        if len(selected) == per_label * 4:
            break
    return selected


if __name__ == '__main__':
    messages = load_sample()
    (HERE / 'golden_set.json').write_text(
        json.dumps(build_legacy_cases(messages), ensure_ascii=False, indent=2),
        encoding='utf-8')
    (HERE / 'pilot_inputs.json').write_text(
        json.dumps(build_pilot_cases(messages), ensure_ascii=False, indent=2),
        encoding='utf-8')