"""Run after two people independently fill rater_a.csv and rater_b.csv."""
import csv
from pathlib import Path

if __name__ == '__main__':
    root = Path(__file__).parent
    ratings = []
    for name in ('rater_a.csv', 'rater_b.csv'):
        with (root / name).open(encoding='utf-8-sig') as f:
            rows = list(csv.DictReader(f))
        if len(rows) != 5 or len({r['id'] for r in rows}) != 5:
            raise SystemExit('Need exactly 5 unique output IDs per rater.')
        if any(r['grade'] not in ('usable','fixable','unacceptable') or not r['trace_id'] for r in rows):
            raise SystemExit('Incomplete ratings: both humans must grade the same 5 real outputs.')
        ratings.append({r['id']:r for r in rows})
    if ratings[0].keys() != ratings[1].keys() or any(ratings[0][k]['trace_id'] != ratings[1][k]['trace_id'] for k in ratings[0]):
        raise SystemExit('Raters did not grade the same outputs.')
    disagreements = sum(ratings[0][k]['grade'] != ratings[1][k]['grade'] for k in ratings[0])
    print(f'Disagreement: {disagreements}/5 = {disagreements*20}%')
    print('Revise rubric and re-rate before freezing.' if disagreements >= 1 else 'No observed disagreement on these 5 outputs.')
