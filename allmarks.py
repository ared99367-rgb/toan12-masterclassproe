from pathlib import Path
import re
text='\n'.join(p.read_text(encoding='utf-8') for p in sorted(Path('work/pdf-text').glob('prob-page-*.txt')))
allm=list(re.finditer(r'(?i)Câu\s*(\d+)\s*[.]',text))
print('all',len(allm),'anchored',len(list(re.finditer(r'(?im)^\s*Câu\s*(\d+)\s*[.]',text))))
for m in allm:
 line=text[text.rfind('\n',0,m.start())+1:text.find('\n',m.start())]
 if m.start()!=0 and text[m.start()-1]!='\n': print(m.group(1),repr(line[:160]))
