from pathlib import Path
paths=[]
for r in range(9):
 y=25+38*r;x0=210-20*r
 for c in range(8-r): paths.append(f'<path d="M{x0+40*c} {y}h40"/>')
for r in range(8):
 y=25+38*r;x0=210-20*r
 for c in range(9-r):
  x=x0+40*c;paths.append(f'<path d="M{x} {y}l-20 38"/>')
  if c<8-r: paths.append(f'<path d="M{x} {y}l20 38"/>')
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 370" role="img" aria-label="Lưới tam giác đều chia thành 64 tam giác đơn vị với 45 đỉnh lưới"><rect width="420" height="370" fill="white"/><g stroke="#2563eb" stroke-width="2" fill="none">'+''.join(paths)+'</g><g fill="#ef4444" stroke="#111827" stroke-width="1">'
for r in range(9):
 for c in range(9-r): svg+=f'<circle cx="{210-20*r+40*c}" cy="{25+38*r}" r="4"/>'
svg+='</g></svg>'
Path('outputs/quiz-assets/prob-triangle-q11.svg').write_text(svg,encoding='utf-8')
