import pypdfium2 as pdfium
from PIL import Image
from pathlib import Path
out=Path('outputs/quiz-assets')
prob=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf')
seq=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\30-bai-tap-cap-so-cong-va-cap-so-nhan-nang-cao-nguyen-dinh-sy.pdf')
def pageim(doc,n): return doc[n-1].render(scale=1.8).to_pil()
def crop(doc,n,b):
 im=pageim(doc,n); x,y,w,h=b; return im.crop((x*2,y*2,(x+w)*2,(y+h)*2))
crop(prob,25,(220,52,140,168)).save(out/'prob-triangle-q11.png',optimize=True)
crop(seq,13,(82,58,135,120)).save(out/'sequence-triangle-q29.png',optimize=True)
crop(seq,13,(330,305,160,83)).save(out/'sequence-triangle-q30.png',optimize=True)
figs=[crop(prob,58,b) for b in [(232,228,100,63),(226,412,106,80),(225,575,112,132)]]+[crop(prob,59,(238,55,105,96))]
w=max(x.width for x in figs); h=sum(x.height for x in figs)+18*(len(figs)-1)
canvas=Image.new('RGB',(w,h),'white'); y=0
for im in figs:
 canvas.paste(im,((w-im.width)//2,y)); y+=im.height+18
canvas.save(out/'prob-polygon-q60.png',optimize=True)
