from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
out=Path('outputs/quiz-assets'); out.mkdir(parents=True,exist_ok=True)
prob=pdfium.PdfDocument(r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf')
def crop(doc,n,b):
 im=doc[n-1].render(scale=1.8).to_pil(); x,y,w,h=b; return im.crop((x*2,y*2,(x+w)*2,(y+h)*2))
crop(prob,6,(100,24,430,155)).save(out/'count-triangle-q9.png',optimize=True)
# Rebuild schematic figures cleanly as standalone SVG assets.
(out/'prob-triangle-q11.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 370" role="img" aria-label="Lưới tam giác đều cạnh chia thành 8 phần, gồm 64 tam giác đơn vị và 45 nút lưới"><rect width="420" height="370" fill="white"/><g stroke="#2563eb" stroke-width="2" fill="none">'''+''.join(f'<path d="M {40+20*r} {30+38*r} L {40+20*r+40*(8-r)} {30+38*r}"/>' for r in range(9))+''.join(f'<path d="M {40+20*r} {30+38*r} L {40+20*(r+1)} {30+38*(r+1)}"/>' for r in range(8) for _ in [0])+''.join(f'<path d="M {40+20*r+40*c} {30+38*r} L {40+20*(r+1)+40*c} {30+38*(r+1)}"/>' for r in range(8) for c in range(8-r))+''.join(f'<circle cx="{40+20*r+40*c}" cy="{30+38*r}" r="4" fill="#ef4444" stroke="#111827" stroke-width="1"/>' for r in range(9) for c in range(9-r))+'</g></svg>',encoding='utf-8')
(out/'sequence-triangle-q29.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 180" role="img" aria-label="Tam giác cân ABC với đường cao AH xuống đáy BC"><rect width="260" height="180" fill="white"/><g stroke="#334155" stroke-width="2" fill="none"><path d="M130 15 L35 155 L225 155 Z M130 15 L130 155"/><path d="M130 146 L139 146 L139 155"/></g><g fill="#0f172a" font-family="sans-serif" font-size="16"><text x="124" y="13">A</text><text x="17" y="169">B</text><text x="228" y="169">C</text><text x="134" y="171">H</text></g></svg>''',encoding='utf-8')
(out/'sequence-triangle-q30.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 190" role="img" aria-label="Tam giác ABC, tâm nội tiếp O và bán kính nội tiếp r"><rect width="280" height="190" fill="white"/><g stroke="#334155" stroke-width="2" fill="none"><path d="M140 18 L28 160 L255 160 Z M140 92 L140 160 M140 92 L140 160 M140 92 L28 160 M140 92 L255 160"/><path d="M140 152 L148 152 L148 160" stroke="#64748b"/></g><circle cx="140" cy="132" r="28" stroke="#0ea5e9" stroke-width="2" fill="none"/><g fill="#0f172a" font-family="sans-serif" font-size="16"><text x="134" y="15">A</text><text x="10" y="176">B</text><text x="258" y="176">C</text><text x="146" y="91">O</text><text x="152" y="149">r</text></g></svg>''',encoding='utf-8')
# Four construction cases from the solution to probability question 60, cropped separately and combined.
figs=[crop(prob,58,b) for b in [(232,228,100,67),(226,412,106,80),(225,575,112,125)]]+[crop(prob,59,(238,55,105,96))]
# Crop whitespace/text fragments from page edges by white-masking narrow outer bands on each panel.
clean=[]
for i,im in enumerate(figs):
 d=ImageDraw.Draw(im); d.rectangle((0,0,im.width,5),fill='white'); d.rectangle((0,im.height-6,im.width,im.height),fill='white')
 clean.append(im)
w=max(x.width for x in clean); h=sum(x.height for x in clean)+16*(len(clean)-1)
canvas=Image.new('RGB',(w,h),'white'); y=0
for im in clean: canvas.paste(im,((w-im.width)//2,y)); y+=im.height+16
canvas.save(out/'prob-polygon-q60.png',optimize=True)
