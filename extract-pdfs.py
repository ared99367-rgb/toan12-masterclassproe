from pathlib import Path
import pdfplumber, json
specs=[('seq',Path(r'C:\Users\ADMIN\Downloads\30-bai-tap-cap-so-cong-va-cap-so-nhan-nang-cao-nguyen-dinh-sy.pdf')),('prob',Path(r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf'))]
out=Path('work/pdf-text'); out.mkdir(parents=True,exist_ok=True)
for name,path in specs:
 with pdfplumber.open(path) as pdf:
  pages=[]
  for i,page in enumerate(pdf.pages,1):
   txt=page.extract_text(layout=False) or ''
   pages.append({'page':i,'width':page.width,'height':page.height,'images':len(page.images),'text':txt})
   (out/f'{name}-page-{i:03}.txt').write_text(txt,encoding='utf-8')
  (out/f'{name}-manifest.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
(Path('work/pdf-text/summary.txt')).write_text('\n'.join(f"{n}: {len(json.loads((out/f'{n}-manifest.json').read_text(encoding='utf-8')))} pages" for n,_ in specs),encoding='utf-8')
