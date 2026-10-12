import pypdfium2 as pdfium
from pathlib import Path
out=Path('outputs/quiz-assets')
seq=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\30-bai-tap-cap-so-cong-va-cap-so-nhan-nang-cao-nguyen-dinh-sy.pdf')
prob=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf')
def crop(doc,page,box,name):
 img=doc[page-1].render(scale=1.8).to_pil(); f=2
 x,y,w,h=box; img.crop((x*f,y*f,(x+w)*f,(y+h)*f)).save(out/name,optimize=True)
crop(prob,6,(108,28,240,145),'count-triangle-q9.png')
crop(prob,25,(205,52,165,163),'prob-triangle-q11.png')
crop(prob,58,(190,345,165,360),'prob-polygon-q60.png')
crop(seq,13,(82,58,160,128),'sequence-triangle-q29.png')
crop(seq,13,(318,285,180,100),'sequence-triangle-q30.png')
