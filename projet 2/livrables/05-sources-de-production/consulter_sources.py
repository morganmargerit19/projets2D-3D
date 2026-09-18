"""Copies de consultation seulement; les sources originales ne sont jamais écrites."""
from pathlib import Path
import subprocess
import fitz
from PIL import Image, ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
DEST=HERE/'consultation';DEST.mkdir(exist_ok=True)
for p in sorted(ROOT.glob('*.pdf')):
    doc=fitz.open(p);texts=[]
    for i,page in enumerate(doc):
        texts.append(page.get_text())
        page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(DEST/f'{p.stem}-{i+1}.png')
    (DEST/(p.stem+'.txt')).write_text('\n'.join(texts))
for p in sorted(ROOT.glob('*.HEIC')):
    dest=DEST/(p.stem+'.jpg')
    temporary=DEST/(p.stem+'.conversion.jpg')
    if temporary.exists():temporary.unlink()
    subprocess.run(['heif-convert',str(p),str(temporary)],check=True,capture_output=True)
    with Image.open(temporary) as image:
        image=ImageOps.exif_transpose(image).convert('RGB');image.thumbnail((3000,3000))
        image.save(DEST/(p.stem+'.validated.jpg'),quality=88,optimize=True)
    with Image.open(DEST/(p.stem+'.validated.jpg')) as check:check.verify()
    (DEST/(p.stem+'.validated.jpg')).replace(dest)
    temporary.unlink()
print('24 pages PDF et 10 HEIC convertis. Originaux intacts.')
