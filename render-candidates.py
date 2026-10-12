import pypdfium2 as pdfium
from pathlib import Path
path=r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf'
pdf=pdfium.PdfDocument(path)
for i in [10,11,23,24,25]:
 img=pdf[i].render(scale=.9).to_pil(); img.save(Path(f'work/prob-page-{i+1:03}.png'))
 print(i+1,img.size)
