"""Extraction reproductible des tracés vectoriels PDF, sans données brutes MOASURE.
XY = déduction depuis le tracé et son calibrage documenté; Z = tableau PDF arrondi.
Les translations d'exposition ne sont PAS un raccordement physique.
"""
from pathlib import Path
import json, re, math, csv, hashlib
import fitz
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE.parent
NAMES = ['Bordure maison', 'Terrasse de droite', 'Terrasse de gauche', 'Zone escalier']
OFFSETS = [[0,0,0],[25,0,0],[0,20,0],[25,20,0]]

def rows(page):
    text = page.get_text()
    pat = r'(\d+)\s+\(([+\-]?\d+,\d+)m\),\s*(\d+,\d+)m,\s*\(([+\-]?\d+,\d+)m\)'
    return [dict(side=int(a), z0=float(b.replace(',','.')), length=float(c.replace(',','.')), z1=float(d.replace(',','.'))) for a,b,c,d in re.findall(pat,text)]

def main():
    datasets=[]; controls=[]
    for name,offset in zip(NAMES,OFFSETS):
        doc=fitz.open(ROOT/(name+'.pdf')); page=doc[0]
        ds=page.get_drawings()
        path=max([d for d in ds if d['type']=='s' and d['color']==(0.,0.,0.)],key=lambda d:len(d['items']))
        # Barre noire encadrante: le filet extérieur de 1 pt ne fait pas partie de la longueur.
        bar=next(d['rect'] for d in ds if d['type']=='f' and d['fill']==(0.,0.,0.) and d['rect'].y0>1080 and d['rect'].width>100)
        bar_m=1.6 if name=='Zone escalier' else 4.0
        points_per_m_bar=(bar.width-2)/bar_m
        points_per_m=points_per_m_bar
        xy=np.array([[it[2].x,it[2].y] for it in path['items'] if it[0]=='l'])
        xy=(xy-xy[0])/points_per_m; xy[:,1]*=-1
        plan=rows(doc[1]); space=rows(doc[3])
        if len(xy)==len(plan): xy=np.vstack([xy,xy[0]]) # dernière fermeture en pointillé, escalier
        assert len(xy)==len(plan)+1, (name,len(xy),len(plan))
        refs={'Terrasse de droite':(34.49,34.53,37.89,37.96),'Terrasse de gauche':(47.54,47.64,46.18,46.45),'Zone escalier':(15.68,17.14,8.59,10.85),'Bordure maison':(20.78,20.84,None,50.17)}[name]
        # Calibrage du DOCUMENT, pas ajustement entre relevés: intersection des
        # intervalles d'arrondi de toutes les cotes, du parcours et de l'aire.
        # Les barres graphiques de droite et escalier ont un écart systématique.
        pixels=xy*points_per_m_bar
        distances=np.linalg.norm(np.diff(pixels,axis=0),axis=1)
        lengths=np.array([r['length'] for r in plan])
        lower=max(distances/(lengths+.005)); upper=min(distances[lengths>.005]/(lengths[lengths>.005]-.005))
        lower=max(lower,distances.sum()/(refs[0]+.005)); upper=min(upper,distances.sum()/(refs[0]-.005))
        if refs[2] is not None:
            area_pixels=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(pixels,np.roll(pixels,-1,axis=0))))/2
            lower=max(lower,math.sqrt(area_pixels/(refs[2]+.005)));upper=min(upper,math.sqrt(area_pixels/(refs[2]-.005)))
        assert lower<=upper,(name,lower,upper)
        points_per_m=points_per_m_bar if lower<=points_per_m_bar<=upper else (lower+upper)/2
        xy=pixels/points_per_m
        z=np.array([plan[0]['z0']]+[r['z1'] for r in plan])
        points=np.column_stack([xy,z])
        closed=name!='Bordure maison'
        assert not closed or np.linalg.norm(xy[-1]-xy[0])<1e-4
        diffs=np.diff(points,axis=0); lengths2=np.linalg.norm(diffs[:,:2],axis=1); lengths3=np.linalg.norm(diffs,axis=1)
        area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(xy, np.roll(xy,-1,axis=0))))/2 if closed else None
        for i,(a,b,l2,l3) in enumerate(zip(plan,space,lengths2,lengths3)):
            for dim,ref,val,pg in [('longueur_XY',a['length'],l2,2),('longueur_3D',b['length'],l3,4)]:
                controls.append(dict(zone=name,element=f'C{i+1:02}',grandeur=dim,source=f'{name}.pdf p.{pg}',reference=ref,modele=round(float(val),6),ecart=round(float(val-ref),6),incertitude='Cotes et Z arrondis au cm; precision instrumentale inconnue; XY derive du PDF'))
        for dim,ref,val in [('parcours_XY',refs[0],sum(lengths2)),('parcours_3D',refs[1],sum(lengths3)),('surface_projetee',refs[2],area)]:
            if val is not None: controls.append(dict(zone=name,element='total',grandeur=dim,source=f'{name}.pdf p.1 ou 3',reference=ref,modele=round(float(val),6),ecart=round(float(val-ref),6),incertitude='Arrondi publication; precision du releve non fournie'))
        d=dict(name=name,source=name+'.pdf',pages=len(doc),points=points.tolist(),closed=closed,points_per_m=points_per_m,points_per_m_bar=points_per_m_bar,calibration_interval=[lower,upper],calibration_note='Calibrage isotrope du PDF par intersection des arrondis; dimensions utilisees au calibrage ne constituent pas une validation independante.',offset_display=offset,rotation_display_degrees=0,physical_transform=None,area_projected=area,area_reference=refs[2],surface_moasure_p5=refs[3],sides_plan=plan,sides_3d=space,perimeter_xy=float(sum(lengths2)),perimeter_3d=float(sum(lengths3)),xy_status='deduit_du_trace_vectoriel_PDF',z_status='cote_relative_locale_arrondie_au_cm',assembly_status='NON_RACCORDE')
        datasets.append(d)
        print(name, 'points',len(points),'surface',area,'perimetre',sum(lengths2),'ecart cote XY max',max(abs(lengths2-np.array([r['length'] for r in plan]))))
    payload=dict(status='BASE_PARTIELLE_NON_RACCORDEE_NON_CONTRACTUELLE',units='metre',scale='1:1',north=None,physical_common_origin=None,display_note='Disposition eclatee de consultation; aucun lien topographique entre groupes.',datasets=datasets)
    (HERE/'releves.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
    with (OUT/'04-controles-et-notice/controles-dimensionnels.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(controls[0]));w.writeheader();w.writerows(controls)
    with (HERE/'points-reconstruits.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['releve','point','X_deduit_m','Y_deduit_m','Z_local_cote_m','source_XY','source_Z'])
        for d in datasets:
            for i,p in enumerate(d['points']):w.writerow([d['name'],f'P{i:02}',*p,d['source']+' p.1-2 (trace calibre par barre et intervalles des cotes)',d['source']+' p.2'])
    return payload

if __name__=='__main__': main()
