from pathlib import Path
import re
s='\n'.join(p.read_text(encoding='utf-8') for p in sorted(Path('work/pdf-text').glob('prob-page-*.txt')))
m=re.search(r'(?im)^\s*Câu\s*(\d+)\s*[.]',s)
e=s.find('\nCâu 2.')
b=s[m.start():e]
print(m.group(1),len(b),repr(b[:100]),repr(b[-100:]))
print(re.search(r'(?i)Lờ\s*i\s*giải',b) is not None)
