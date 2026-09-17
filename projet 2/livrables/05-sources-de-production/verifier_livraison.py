"""Contrôles locaux; ne certifie pas l'exécution SketchUp ou le raccordement physique."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
import ezdxf,fitz
from PIL import Image
HERE=Path(__file__).resolve().parent;OUT=HERE.parent;ROOT=OUT.parent;REPO=ROOT.parent
original=json.loads((HERE/'manifest-original.json').read_text());D=json.loads((HERE/'releves.json').read_text())
checked=[]
for row in original:
    p=ROOT/row['file'];raw=p.read_bytes();assert len(raw)==row['bytes'];assert hashlib.sha256(raw).hexdigest()==row['sha256']
    base=subprocess.check_output(['git','show','0144802a4c3423310ed457b8e053e17aa3202567:'+row['file']],cwd=REPO)
    assert raw==base
    checked.append(row['file'])
assert len(checked)==19
checks=[]
for dim in [2,3]:
    path=OUT/('01-plan-2d' if dim==2 else '02-modele-3d')/f'Releves_{dim}D_non_raccordes.dxf'
    doc=ezdxf.readfile(path);assert not doc.audit().errors;assert doc.units==6
    polys=list(doc.modelspace().query('LWPOLYLINE' if dim==2 else 'POLYLINE'));assert len(polys)==4
    for d,poly in zip(D['datasets'],polys):
        expected=np.array(d['points'])+np.array(d['offset_display'])
        if dim==2:
            expected=expected[:,:2];actual=np.array([(x,y) for x,y,*_ in poly.get_points()]);assert poly.dxf.elevation==0
        else:actual=np.array([tuple(v.dxf.location) for v in poly.vertices])
        error=float(np.max(abs(expected-actual)));assert error<1e-9
        checks.append(dict(export=f'DXF {dim}D',zone=d['name'],erreur_serialisation_m=error))
pdf=fitz.open(OUT/'01-plan-2d/NOKOD_Projet_2_Releves_2D_CONTROLE.pdf');assert len(pdf)==4
for page in pdf:
    assert abs(page.rect.width-420/25.4*72)<.01 and abs(page.rect.height-297/25.4*72)<.01
pngs=sorted((OUT/'04-controles-et-notice/controle-geometrie').glob('*.png'));assert len(pngs)==5
for p in pngs:
    with Image.open(p) as im:assert im.size==(1600,1200)
consultation=HERE/'consultation'
photos=sorted(consultation.glob('IMG*.jpg'));assert len(photos)==10
for p in photos:
    with Image.open(p) as im:assert max(im.size)==3000;im.verify()
pages=sorted(consultation.glob('*.png'));assert len(pages)==24
for p in pages:
    with Image.open(p) as im:im.verify()
result=dict(originaux_conserves_identiques_git=checked,controles_exports=checks,pdf={'pages':4,'format_mm':[420,297],'echelles':[75,75,75,30]},photos_consultation_decodees=10,pages_consultation_decodees=24,vues_techniques=5,rendus_photorealistes_finaux=0,skp_presents=[str(p.relative_to(OUT)) for p in OUT.rglob('*.skp')],sketchup_execute=False,raccordement_physique_valide=False)
(OUT/'04-controles-et-notice/verification-locale.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
print('19 originaux identiques au commit de depart. 2 DXF rouverts, correspondance exacte aux donnees communes. PDF A3 et 5 controles techniques verifies. SKP et maquette de site non valides.')
