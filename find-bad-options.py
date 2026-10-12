from pathlib import Path
import json,collections
qs=json.loads(Path('work/new-quiz-data.json').read_text(encoding='utf-8'))
for i,q in enumerate(qs):
 if i<53: continue
 if any(v.strip() in {'.','', 'A.', 'B.', 'C.', 'D.'} or len(v.strip())<2 for v in q['options']):
  print(i, q['chapter'], q['question'][:210], '|', q['options'], 'ans',q['correct'])
chars=collections.Counter(ch for q in qs for key in ('question','options','explanation') for v in ([q[key]] if isinstance(q[key],str) else q[key]) for ch in v if '\uf000'<=ch<='\uf8ff')
print('PUA',[(hex(ord(c)),n) for c,n in chars.items()])
