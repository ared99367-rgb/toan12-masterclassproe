import pypdfium2 as pdfium
from pathlib import Path
p=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf')
p[58].render(scale=.9).to_pil().save('work/prob-page-059.png')
