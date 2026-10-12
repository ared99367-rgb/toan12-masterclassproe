import pypdfium2 as pdfium
from pathlib import Path
for name,path,indices in [('prob',r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf',[5]),('prob',r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf',[1])]:
 p=pdfium.PdfDocument(path)
 for i in indices:
  p[i].render(scale=.9).to_pil().save(Path(f'work/{name}-page-{i+1:03}.png'))
