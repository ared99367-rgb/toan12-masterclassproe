from pypdf import PdfReader
from pathlib import Path
for name in ['seq','prob']:
 base=Path('work/pdf-text')
 files=sorted(base.glob(f'{name}-page-*.txt'))
 print(name,len(files))
