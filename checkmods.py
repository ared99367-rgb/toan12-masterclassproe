from importlib.util import find_spec
for m in ['PIL','pypdfium2','wand','fitz','pdf2image','cairosvg']:
 print(m, bool(find_spec(m)))
