from pathlib import Path
import re
for f in sorted(Path('work/pdf-text').glob('*page-*.txt')):
 t=f.read_text(encoding='utf-8')
 if re.search(r'(?i)hình|đồ thị|sơ đồ',t):
  matches=re.findall(r'(?i).{0,90}(?:hình|đồ thị|sơ đồ).{0,100}',t)
  print(f.name, ' :: ', ' | '.join(matches[:6]))
