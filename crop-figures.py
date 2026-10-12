import pypdfium2 as pdfium
from pathlib import Path
out=Path('outputs/quiz-assets'); out.mkdir(parents=True,exist_ok=True)
seq=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\30-bai-tap-cap-so-cong-va-cap-so-nhan-nang-cao-nguyen-dinh-sy.pdf')
prob=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf')
def crop(doc,page,box,name):
 img=doc[page-1].render(scale=1.8).to_pil()
 f=1.8/.9
 x,y,w,h=box
 box=(round(x*f),round(y*f),round((x+w)*f),round((y+h)*f))
 img.crop(box).save(out/name,optimize=True)
 print(name,box)
crop(prob,2,(190,135,200,155),'count-cube-q3.png')
crop(prob,6,(100,25,270,175),'count-triangle-q9.png')
crop(prob,11,(177,393,212,110),'count-grid-q18.png')
crop(prob,25,(203,50,175,175),'prob-triangle-q11.png')
crop(prob,58,(170,330,220,390),'prob-polygon-q60.png')
crop(seq,13,(68,50,180,145),'sequence-triangle-q29.png')
crop(seq,13,(300,250,210,165),'sequence-triangle-q30.png')
