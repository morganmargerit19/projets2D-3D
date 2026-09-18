"""A lancer avec Blender sur le .blend ENREGISTRE, pour controler la reouverture."""
import bpy,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'releves.json').read_text());results=[]
for d in data['datasets']:
    obj=bpy.data.objects['RELEVE_EXACT_'+d['name']];assert len(obj.data.vertices)==len(d['points'])
    diffs=[]
    for v,p in zip(obj.data.vertices,d['points']):
        diffs.extend(abs(v.co[k]-(p[k]+d['offset_display'][k])) for k in range(3))
    e=max(diffs);assert e<1e-5
    results.append(dict(releve=d['name'],sommets=len(obj.data.vertices),ecart_serialisation_m=e))
cameras=[o for o in bpy.data.objects if o.type=='CAMERA'];assert len(cameras)==5
for obj in bpy.data.objects:
    if obj.name.startswith('SURFACE_INTERPOLEE_'):
        assert obj.hide_render and obj.hide_get()
        assert all(p.normal.z>0 for p in obj.data.polygons)
result=dict(fichier=bpy.data.filepath,reouverture_blender=True,controle_sommets=results,cameras=len(cameras),surfaces_interpolees_masquees=True,sketchup_verifie=False)
(HERE.parent/'04-controles-et-notice/verification-blender.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
print(json.dumps(result,ensure_ascii=False))
