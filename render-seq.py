import pypdfium2 as pdfium
from pathlib import Path
p=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\30-bai-tap-cap-so-cong-va-cap-so-nhan-nang-cao-nguyen-dinh-sy.pdf')
for i in [8,9,10,11,12]:
 p[i].render(scale=.9).to_pil().save(Path(f'work/seq-page-{i+1:03}.png'))
