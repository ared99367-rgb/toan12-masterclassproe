import pypdfium2 as pdfium
from pathlib import Path
out=Path('outputs/quiz-assets'); seq=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\30-bai-tap-cap-so-cong-va-cap-so-nhan-nang-cao-nguyen-dinh-sy.pdf'); prob=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf')
def c(d,p,b,n):
 im=d[p-1].render(scale=1.8).to_pil(); x,y,w,h=b; im.crop((x*2,y*2,(x+w)*2,(y+h)*2)).save(out/n,optimize=True)
c(prob,6,(108,28,240,158),'count-triangle-q9.png')
c(prob,25,(220,52,140,170),'prob-triangle-q11.png')
c(prob,58,(210,380,140,330),'prob-polygon-q60.png')
c(seq,13,(78,58,155,115),'sequence-triangle-q29.png')
c(seq,13,(328,290,165,95),'sequence-triangle-q30.png')
