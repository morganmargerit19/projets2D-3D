"""Produit les exports de travail à partir de releves.json, jamais des SKP déguisés."""
from pathlib import Path
import json, math, csv
import numpy as np
import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color, white

HERE=Path(__file__).resolve().parent; OUT=HERE.parent
DATA=json.loads((HERE/'releves.json').read_text()); DS=DATA['datasets']
COLORS=['#546D71','#A87843','#4C7865','#8B6474']

def dxf_export(is3d):
    doc=ezdxf.new('R2010');doc.units=6;doc.header['$INSUNITS']=6
    doc.header['$MEASUREMENT']=1
    ms=doc.modelspace()
    for j,d in enumerate(DS):
        layer=f'{j+1:02}_'+d['name'].replace(' ','_');doc.layers.new(layer,dxfattribs={'color':j+2})
        pts=np.array(d['points']);offset=np.array(d['offset_display']);pts=pts+offset
        if not is3d:pts[:,2]=0
        ms.add_polyline3d(pts.tolist(),dxfattribs={'layer':layer}) if is3d else ms.add_lwpolyline(pts[:,:2],dxfattribs={'layer':layer})
        base=(float(pts[:,0].min()),float(pts[:,1].max()+1.3),0)
        ms.add_text(d['name']+' - NON RACCORDE',dxfattribs={'height':.32,'layer':layer,'insert':base})
        for i,p in enumerate(pts[:-1] if d['closed'] else pts):
            if i and np.linalg.norm(pts[i]-pts[i-1])<.02:continue
            ms.add_text(f'P{i:02}',dxfattribs={'height':.13,'layer':layer,'insert':tuple(p+np.array([.08,.08,0]))})
        if not is3d:
            for i,(a,b,row) in enumerate(zip(pts[:-1],pts[1:],d['sides_plan'])):
                if row['length']<1:continue
                v=b-a;v=v[:2]/np.linalg.norm(v[:2]);n=np.array([-v[1],v[0]])
                midpoint=(a[:2]+b[:2])/2+n*.3
                dim=ms.add_aligned_dim(p1=a[:2],p2=b[:2],distance=.3,dimstyle='EZDXF',override={'dimtxt':.16,'dimasz':.07,'dimdec':2,'dimtad':1,'dimexo':.03,'dimexe':.05,'dimclrd':j+2,'dimclre':j+2},dxfattribs={'layer':layer});dim.render()
    ms.add_text('RELEVES INDEPENDANTS - DISPOSITION ECLATEE NON TOPOGRAPHIQUE - METRES',dxfattribs={'height':.5,'insert':(0,35,0)})
    p=OUT/('02-modele-3d/Releves_3D_non_raccordes.dxf' if is3d else '01-plan-2d/Releves_2D_non_raccordes.dxf')
    doc.saveas(p)
    re=ezdxf.readfile(p);audit=re.audit();assert not audit.errors,(p,audit.errors)

def draw_pdf():
    p=OUT/'01-plan-2d/NOKOD_Projet_2_Releves_2D_CONTROLE.pdf'
    c=canvas.Canvas(str(p),pagesize=(420*mm,297*mm));c.setTitle('NOKOD GARDENS - MARZET - Releves independants de controle')
    for j,d in enumerate(DS):
        col=HexColor(COLORS[j]);sc=30 if j==3 else 75
        pts=np.array(d['points']);xy=pts[:,:2];minxy=xy.min(axis=0);maxxy=xy.max(axis=0)
        factor=1000*mm/sc;low=np.array([20*mm,57*mm]);available=np.array([260*mm,182*mm]);dims=(maxxy-minxy)*factor
        origin=low+(available-dims)/2-minxy*factor
        pp=xy*factor+origin
        c.setFillColor(HexColor('#F7F7F2'));c.rect(0,0,420*mm,297*mm,fill=1,stroke=0)
        c.setFillColor(HexColor('#263B34'));c.setFont('Helvetica-Bold',12);c.drawString(18*mm,280*mm,'NOKOD GARDENS   /   DOSSIER MARZET')
        c.setFont('Helvetica-Bold',24);c.drawString(18*mm,265*mm,d['name'])
        c.setFont('Helvetica',10);c.drawString(18*mm,254*mm,'BASE DE CONTROLE - Releve independant, non raccorde au site')
        c.setStrokeColor(HexColor('#DDDFD7'));c.line(18*mm,248*mm,402*mm,248*mm)
        path=c.beginPath();path.moveTo(*pp[0])
        for point in pp[1:]:path.lineTo(*point)
        if d['closed']:path.close()
        c.setFillColor(Color(col.red,col.green,col.blue,alpha=.14));c.setStrokeColor(col);c.setLineWidth(1.2);c.drawPath(path,fill=int(d['closed']),stroke=1)
        signed=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(xy,np.roll(xy,-1,axis=0)))
        for i,(a,b,row) in enumerate(zip(pp[:-1],pp[1:],d['sides_plan'])):
            v=b-a;length=np.linalg.norm(v)
            if row['length']<.8 or length<1:continue
            v/=length;n=np.array([v[1],-v[0]])*(1 if signed>=0 or not d['closed'] else -1)
            mid=(a+b)/2+n*3*mm;angle=math.degrees(math.atan2(v[1],v[0]))
            if angle>90:angle-=180
            if angle<-90:angle+=180
            text=f'{row["length"]:.2f} m'
            c.saveState();c.translate(*mid);c.rotate(angle);c.setFillColor(HexColor('#F7F7F2'));w=c.stringWidth(text,'Helvetica',8);c.rect(-w/2-2,-2,w+4,10,fill=1,stroke=0);c.setFillColor(HexColor('#263B34'));c.setFont('Helvetica',8);c.drawCentredString(0,0,text);c.restoreState()
        # Points: aucune fausse altitude géographique, Z local uniquement.
        labeled=[]
        for i,a in enumerate(pp[:-1] if d['closed'] else pp):
            if i and np.linalg.norm(xy[i]-xy[i-1])<.12:continue
            c.setFillColor(col);c.circle(*a,1.5,fill=1,stroke=0)
            if any(np.linalg.norm(a-b)<7*mm for b in labeled):continue
            labeled.append(a)
            c.setFont('Helvetica',6.5);c.drawString(a[0]+3,a[1]+3,f'P{i:02}')
        x0,y0=pp[0];c.setStrokeColor(HexColor('#688579'));c.setFillColor(HexColor('#688579'));c.setFont('Helvetica',8)
        c.line(x0,y0,x0+12*mm,y0);c.line(x0,y0,x0,y0+12*mm);c.drawString(x0+13*mm,y0,'X');c.drawString(x0,y0+13*mm,'Y')
        tx=300*mm
        def line(text,y,bold=False,size=9):
            c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.setFillColor(HexColor('#263B34'));c.drawString(tx,y*mm,text)
        line('DONNEES LOCALES',238,True,11)
        line('Unites : metres | Geometrie : 1:1',231)
        line(f'Parcours XY : {d["perimeter_xy"]:.2f} m',224)
        line(('Aire projetee : '+f'{d["area_projected"]:.2f} m2') if d['closed'] else 'Trace ouvert : aucune aire affectee',217)
        line(f'Z local : {pts[:,2].min():+.2f} a {pts[:,2].max():+.2f} m',210)
        line('Origine : P00 du PDF, non localisee sur site',203,False,8)
        line('Nord non documente',196)
        line('Cote     XY (m)       Z debut / fin (m)',186,True,8)
        for i,row in enumerate(d['sides_plan']):
            line(f'C{i+1:02}      {row["length"]:5.2f}           {row["z0"]:+.2f} / {row["z1"]:+.2f}',180-i*4,False,8)
        line('XY deduits du trace vectoriel calibre.',54,False,8)
        line('Z cotes dans le PDF, arrondis au cm.',49,False,8)
        line('Aucun assemblage physique valide.',44,True,8)
        c.setStrokeColor(HexColor('#263B34'));c.setLineWidth(1)
        bx=22*mm;by=33*mm;c.line(bx,by,bx+factor,by)
        for x in [bx,bx+factor]:c.line(x,by-2*mm,x,by+2*mm)
        c.setFont('Helvetica',8);c.drawString(bx,by+4*mm,'1 metre')
        c.drawString(70*mm,33*mm,f'A3 paysage - 1:{sc} a 100 %, sans adaptation a la page')
        c.setFont('Helvetica',8);c.drawString(18*mm,21*mm,f'Source : {d["source"]}, p.1-2. Tableau : valeurs publiees. Dessin : reconstruction vectorielle.')
        c.drawString(18*mm,15*mm,'Ce document est une base partielle de restitution, pas un plan d implantation, de propriete ou d execution.')
        c.drawRightString(402*mm,15*mm,f'{j+1} / 4');c.showPage()
    c.save()

if __name__=='__main__':
    dxf_export(False);dxf_export(True);draw_pdf()
    print('2 DXF rouverts et controles; PDF 4 pages genere.')
