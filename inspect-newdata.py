from pathlib import Path
import json,collections,re
qs=json.loads(Path('work/new-quiz-data.json').read_text(encoding='utf-8'))
chars=collections.Counter(ch for q in qs for key in ('question','options','explanation') for v in ([q[key]] if isinstance(q[key],str) else q[key]) for ch in v if '\uf000'<=ch<='\uf8ff')
print('pua',[(hex(ord(c)),c,n) for c,n in chars.items()])
print('questions',len(qs),'invalid',[i for i,q in enumerate(qs) if len(q['options'])!=4 or q['correct'] not in range(4) or not q['explanation']])
for i in [23,24,29,35,45,52,53,54,62,63,64,92,121,122,123,151]:
 if i<len(qs):
  q=qs[i]; print('\nidx',i,'ch',q['chapter'],'Q',q['question'][:240],'options',q['options'],'correct',q['correct'],'EX',q['explanation'][:260])
