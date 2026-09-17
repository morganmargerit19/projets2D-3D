"""Blender 4.5.3: releves 3D locaux et vues TECHNIQUES, pas rendus paysagers finaux.
Utilisation: blender -b -t 4 --python construire_blender.py
"""
import bpy, json, math
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

HERE=Path(__file__).resolve().parent;OUT=HERE.parent
DATA=json.loads((HERE/'releves.json').read_text());DS=DATA['datasets']
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name != 'Collection' and c.users==0:bpy.data.collections.remove(c)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene['STATUT']='BASE PARTIELLE NON RACCORDEE. Aucun batiment, aucune marche ni terrain continu restitues.'
scene['DONNEES']='XY deduits des PDF; Z locaux. Translations des groupes = exposition, pas implantation.'
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24
scene.cycles.use_denoising=True
scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.world.color=(.65,.65,.65)
scene.view_settings.view_transform='Standard'
colors=[(.23,.37,.41,1),(.52,.28,.09,1),(.18,.4,.29,1),(.44,.22,.34,1)]

def mat(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=.75
    return m

def collection(name):
    c=bpy.data.collections.new(name);scene.collection.children.link(c);return c

def relink(obj,col):
    for c in list(obj.users_collection):c.objects.unlink(obj)
    col.objects.link(obj)

def tube(name,points,col,material,radius=.025):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=2
    s=cu.splines.new('POLY');s.points.add(len(points)-1)
    for p,q in zip(s.points,points):p.co=(*q,1)
    obj=bpy.data.objects.new(name,cu);col.objects.link(obj);obj.data.materials.append(material);return obj

presentation=collection('90_PRESENTATION_TECHNIQUE_pas_du_terrain')
white=mat('Fond de controle',(.92,.93,.90,1));gray=mat('Axes et projections',(.6,.65,.62,1))
sets=[];allpts=[]
for j,d in enumerate(DS):
    col=collection(f'{j+1:02}_{d["name"]}_NON_RACCORDE')
    m=mat(d['name'],colors[j]);offset=Vector(d['offset_display'])
    pts=[Vector(p)+offset for p in d['points']];allpts+=pts
    mesh=bpy.data.meshes.new(d['name']+'_sommets_source')
    mesh.from_pydata([tuple(p) for p in pts],[(i,i+1) for i in range(len(pts)-1)],[]);mesh.update()
    raw=bpy.data.objects.new('RELEVE_EXACT_'+d['name'],mesh);col.objects.link(raw)
    raw['SOURCE']=d['source'];raw['TRANSLATION_EXPOSITION']=d['offset_display'];raw['RACCORDEMENT']='AUCUN';raw['XY']='DEDUITS_PDF';raw['Z']='LOCAUX_COTES'
    tube('Representation_epaissie_non_metrique',pts,col,m)
    for i,p in enumerate(pts):
        if i and (p-pts[i-1]).length<.02:continue
        if d['closed'] and i==len(pts)-1:continue
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=.055,location=p)
        obj=bpy.context.object;obj.name=f'Point_P{i:02}';relink(obj,col);obj.data.materials.append(m)
        obj['Z_LOCAL']=d['points'][i][2]
    # Une surface d'interpolation facultative est fournie mais masquee: elle ne constitue pas un terrain mesure.
    if d['closed']:
        poly=[Vector((p[0],p[1],0)) for p in d['points'][:-1]]
        clean=[];idx=[]
        for i,p in enumerate(poly):
            if not clean or (p-clean[-1]).length>=.005:clean.append(p);idx.append(i)
        tris=tessellate_polygon([clean]);lookup={tuple(p):idx[k] for k,p in enumerate(clean)}
        faces=[tuple(idx[p] if isinstance(p,int) else lookup[tuple(p)] for p in tri) for tri in tris]
        faces=[f if (pts[f[1]]-pts[f[0]]).cross(pts[f[2]]-pts[f[0]]).z>0 else tuple(reversed(f)) for f in faces]
        mesh2=bpy.data.meshes.new('Interpolation_NON_VALIDEE');mesh2.from_pydata([tuple(p) for p in pts],[],faces);mesh2.update()
        surf=bpy.data.objects.new('SURFACE_INTERPOLEE_NON_LEVEE_'+d['name'],mesh2);col.objects.link(surf);surf.data.materials.append(m)
        surf.hide_render=True;surf.hide_set(True);surf['AVERTISSEMENT']='Triangulation illustrative des sommets. Pas de marches restituees. Ne pas assimiler au terrain, ni a la triangulation MOASURE.'
    # Axes locaux originaux, sans nord presume.
    tube('X_local',[offset,offset+Vector((1,0,0))],col,gray,.012)
    tube('Y_local',[offset,offset+Vector((0,1,0))],col,gray,.012)
    sets.append((col,pts))

bpy.ops.mesh.primitive_plane_add(size=200,location=(15,10,-1.25));floor=bpy.context.object;floor.name='Fond_de_studio_NON_TERRAIN';relink(floor,presentation);floor.data.materials.append(white)
ld=bpy.data.lights.new('Eclairage_controle','AREA');lo=bpy.data.objects.new('Eclairage_controle',ld);presentation.objects.link(lo);lo.location=(10,10,40);ld.energy=15000;ld.shape='DISK';ld.size=35
ld2=bpy.data.lights.new('Soleil_controle','SUN');lo2=bpy.data.objects.new('Soleil_controle',ld2);presentation.objects.link(lo2);lo2.rotation_euler=(.3,-.4,-.3);ld2.energy=1.7;ld2.angle=.2

def camera(name,pts,relative):
    mn=Vector(tuple(min(p[k] for p in pts) for k in range(3)));mx=Vector(tuple(max(p[k] for p in pts) for k in range(3)));target=(mn+mx)/2
    camd=bpy.data.cameras.new(name);cam=bpy.data.objects.new(name,camd);presentation.objects.link(cam)
    cam.location=target+Vector(relative);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();camd.type='ORTHO'
    inv=cam.rotation_euler.to_matrix().transposed();local=[inv@(p-target) for p in pts]
    w=max(p.x for p in local)-min(p.x for p in local);h=max(p.y for p in local)-min(p.y for p in local)
    camd.ortho_scale=max(w,h*4/3)*1.28
    return cam

cameras=[camera('01_Vue_eclatee_NON_IMPLANTATION',allpts,(12,-24,44))]
for j,(_,pts) in enumerate(sets):cameras.append(camera(f'{j+2:02}_{DS[j]["name"]}',pts,(10,-15,16)))
camdata=[]
targetdir=OUT/'04-controles-et-notice/controle-geometrie';targetdir.mkdir(exist_ok=True)
for i,cam in enumerate(cameras):
    scene.camera=cam
    for j,(col,_) in enumerate(sets):col.hide_render=i!=0 and j!=i-1
    scene.render.filepath=str(targetdir/f'{i+1:02}_controle_technique.png')
    bpy.ops.render.render(write_still=True)
    camdata.append(dict(name=cam.name,position=list(cam.location),rotation_euler=list(cam.rotation_euler),orthographic_scale=cam.data.ortho_scale,resolution=[1600,1200],type='controle technique non photorealiste'))
for col,_ in sets:col.hide_render=False
scene.camera=cameras[0]
(HERE/'cameras-controle.json').write_text(json.dumps(camdata,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'02-modele-3d/NOKOD_Projet_2_Releves_NON_RACCORDES.blend'))
print('Cinq controles techniques et scene Blender produits. Aucun rendu final photorealiste.')
