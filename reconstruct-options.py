from pathlib import Path
import pdfplumber,re,collections,json
p=r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf'
with pdfplumber.open(p) as pdf: pages=[{'text':pg.extract_text(layout=False) or '', 'words':pg.extract_words(x_tolerance=1,y_tolerance=2)} for pg in pdf.pages]
full='\n'.join(pg['text'] for pg in pages); offsets=[]; off=0
for pg in pages: offsets.append((off,off+len(pg['text'])));off+=len(pg['text'])+1
marks=list(re.finditer(r'(?im)^\s*Câu\s*(\d+)\s*[.]',full)); entries=[]
for idx,m in enumerate(marks):
 end=marks[idx+1].start() if idx+1<len(marks) else len(full); block=full[m.start():end]; sm=re.search(r'(?i)Lờ\s*i\s*giải',block); pre=block[:sm.start()] if sm else block
 om=re.search(r'(?is)(?:^|\n)\s*A\s*[.]\s*(.*?)\s+B\s*[.]\s*(.*?)\s+C\s*[.]\s*(.*?)\s+D\s*[.]\s*([^\n]*)(?:\n|$)',pre)
 if om:
  pos=m.start()+om.start(); pi=next((k for k,(a,b) in enumerate(offsets) if a<=pos<=b),None);entries.append({'n':idx+1,'pi':pi,'pos':pos})
by=collections.defaultdict(list)
for e in entries:by[e['pi']].append(e)
def row_candidate(words):
 labs=[]
 for w in words:
  if w['text']!='A.' or not 80<=w['x0']<=110:continue
  y=w['top']; found=[]
  for tag,xlo,xhi in [('B.',195,230),('C.',310,350),('D.',425,460)]:
   z=next((x for x in words if x['text']==tag and xlo<=x['x0']<=xhi and abs(x['top']-y)<2),None);found.append(z)
  if all(found):labs.append(y)
 return sorted(set(labs))
def words_text(ws):return ' '.join(w['text'] for w in sorted(ws,key=lambda a:a['x0']) if w['text']!='.').strip()
def value(words,y,xlo,xhi):
 ws=[w for w in words if xlo<=w['x0']<xhi and y-13<=w['top']<=y+21 and w['text'] not in ['A.','B.','C.','D.']]
 rows=[]
 for w in sorted(ws,key=lambda a:(a['top'],a['x0'])):
  if not rows or abs(rows[-1][0]-w['top'])>3:rows.append([w['top'],[w]])
  else:rows[-1][1].append(w)
 texts=[words_text(x[1]) for x in rows];texts=[x for x in texts if x]
 if len(texts)>=2:
  k=max(1,len(texts)//2);return ' '.join(texts[:k])+'/'+ ' '.join(texts[k:])
 return texts[0] if texts else ''
res={}; ranges=[(103,205),(224,318),(338,431),(451,590)]
for pi,es in by.items():
 ys=row_candidate(pages[pi]['words']);es=sorted(es,key=lambda e:e['pos'])
 if len(ys)!=len(es):
  print('MISMATCH',pi+1,[e['n'] for e in es],ys)
 for e,y in zip(es,ys):res[e['n']]=[value(pages[pi]['words'],y,*rg) for rg in ranges]
Path('work/reconstructed-options.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
for n,v in res.items(): print(n, v)
