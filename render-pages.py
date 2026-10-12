import pypdfium2 as pdfium
from pathlib import Path
for name,path,pages in [('seq',r'C:\Users\ADMIN\Downloads\30-bai-tap-cap-so-cong-va-cap-so-nhan-nang-cao-nguyen-dinh-sy.pdf',[0,1,3,11]),('prob',r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf',[0,1,17,57,66])]:
 pdf=pdfium.PdfDocument(path)
 for i in pages:
  img=pdf[i].render(scale=.9).to_pil()
  out=Path(f'work/{name}-page-{i+1:03}.png'); img.save(out)
  print(out, img.size)
