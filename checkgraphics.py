import pdfplumber
for path in [r'C:\Users\ADMIN\Downloads\30-bai-tap-cap-so-cong-va-cap-so-nhan-nang-cao-nguyen-dinh-sy.pdf',r'C:\Users\ADMIN\Downloads\bai-tap-trac-nghiem-to-hop-va-xac-suat-nang-cao-co-loi-giai-chi-tiet.pdf']:
 with pdfplumber.open(path) as pdf:
  print(path.split('\\')[-1], 'pages',len(pdf.pages),'graphics',sum(len(p.rects)+len(p.curves)+len(p.lines) for p in pdf.pages),'max-per-page',max(len(p.rects)+len(p.curves)+len(p.lines) for p in pdf.pages))
