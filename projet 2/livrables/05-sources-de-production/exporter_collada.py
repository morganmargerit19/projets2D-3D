"""Blender 4.5: export reel COLLADA 1.4.1, metre, Z_UP, groupes editables.
Releves independants: aucune implantation physique inventee.
blender -b --python exporter_collada.py
"""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
H=Path(__file__).resolve().parent;O=H.parent
D=json.loads((H/'releves.json').read_text())['datasets']

def material(name,c):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);return m

def mesh(name,verts,faces,edges,group,mat):
 m=bpy.data.meshes.new(name);m.from_pydata(verts,edges,faces);m.update()
 ob=bpy.data.objects.new(name,m);bpy.context.collection.objects.link(ob);ob.parent=group
 if mat:ob.data.materials.append(mat)
 return ob

def label(txt,loc,size,group):
 cu=bpy.data.curves.new(txt,'FONT');cu.body=txt;cu.size=size;cu.align_x='LEFT';cu.resolution_u=3;cu.materials.append(ink)
 ob=bpy.data.objects.new(txt,cu);bpy.context.collection.objects.link(ob);ob.location=loc;ob.parent=group
 bpy.context.view_layer.objects.active=ob;ob.select_set(True);bpy.ops.object.convert(target='MESH');ob.select_set(False)
 return ob

def line(name,a,b,group,mat,width=.009):
 a=Vector(a);b=Vector(b);v=b-a
 if v.length<.0001:return
 n=Vector((-v.y,v.x,0)).normalized()*width/2
 mesh(name,[a+n,b+n,b-n,a-n],[(0,1,2,3)],[],group,mat)

reports=[]
for dim in (2,3):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
 colors=[(.22,.4,.43),(.7,.5,.3),(.38,.61,.49),(.61,.38,.51)]
 ink=material('Annotations_NON_METRIQUES',(.12,.16,.18))
 for j,d in enumerate(D):
  root=bpy.data.objects.new(f'{j+1:02}_{d["name"]}_REPERE_LOCAL_NON_RACCORDE',None);bpy.context.collection.objects.link(root)
  root.location=d['offset_display'];root['SOURCE']=d['source'];root['UNITE']='metre';root['STATUT']='NON_RACCORDE'
  verts=[(p[0],p[1],p[2] if dim==3 else 0) for p in d['points']]
  mat=material(d['name']+'_surface_INTERPOLEE' if dim==3 else d['name']+'_projection',colors[j])
  # Exact points and edges, including source micro-segments, unmodified.
  edges=[(k,k+1) for k in range(len(verts)-1) if (Vector(verts[k+1])-Vector(verts[k])).length>.00001]
  mesh('CONTOUR_SOURCE_'+d['name'],verts,[],edges,root,ink)
  if d['closed']:
   keep=[]
   for k,p in enumerate(verts[:-1]):
    if not keep or (Vector(p[:2])-Vector(verts[keep[-1]][:2])).length>.000001:keep.append(k)
   poly=[Vector((verts[k][0],verts[k][1],0)) for k in keep]
   lookup={tuple(p):keep[k] for k,p in enumerate(poly)}
   faces=[]
   for tri in tessellate_polygon([poly]):
    f=tuple(keep[v] if isinstance(v,int) else lookup[tuple(v)] for v in tri)
    a,b,c=[Vector(verts[k]) for k in f]
    faces.append(f if (b-a).cross(c-a).z>=0 else tuple(reversed(f)))
   surf=mesh(('SURFACE_INTERPOLEE_NON_TERRAIN_' if dim==3 else 'SURFACE_PROJETEE_')+d['name'],verts,faces,[],root,mat)
   surf['INTERPOLATION']='Sommets de bord uniquement; ni terrain leve, ni marches.'
  # Plan annotations are mesh glyphs, hence portable and editable in COLLADA, not native dimensions.
  if dim==2:
   ymin=min(p[1] for p in verts);ymax=max(p[1] for p in verts);xmin=min(p[0] for p in verts)
   label(d['name'].upper(),(xmin,ymax+1,0),.25,root)
   label('REPERE LOCAL - NON RACCORDE',(xmin,ymax+.6,0),.16,root)
   if d['closed']:label(f'Surface projetee : {d["area_projected"]:.2f} m2',(xmin,ymin-1.2,0),.18,root)
   else:label('Releve ouvert : aucune surface de batiment',(xmin,ymin-1.2,0),.16,root)
   # each long segment dimension offset on its exterior side
   area=sum(verts[k][0]*verts[k+1][1]-verts[k+1][0]*verts[k][1] for k in range(len(verts)-1))
   for k,(a,b) in enumerate(zip(verts,verts[1:])):
    a=Vector(a);b=Vector(b);v=b-a;l=v.length
    if l<.7:continue
    n=Vector((v.y,-v.x,0)).normalized()*(1 if area>0 else -1)*.32
    aa=a+n;bb=b+n;mid=(aa+bb)/2
    line('Cote_ligne',aa,bb,root,ink,.005)
    line('Rappel',a,aa+n*.2,root,ink,.003);line('Rappel',b,bb+n*.2,root,ink,.003)
    ob=label(f'{l:.2f} m',mid+n*.25,.13,root)
    angle=math.atan2(v.y,v.x)
    if angle>math.pi/2:angle-=math.pi
    if angle<-math.pi/2:angle+=math.pi
    ob.rotation_euler.z=angle
  else:
   # planar ribbons alongside exact boundary aid visibility in importers that omit pure lines.
   for k,(a,b) in enumerate(zip(verts,verts[1:])):line('REPERE_VISUEL_5mm_NON_BORDURE',a,b,root,ink,.005)
 # header
 root=bpy.data.objects.new('00_NOTICE_NON_GEOMETRIQUE',None);bpy.context.collection.objects.link(root)
 label('NOKOD GARDENS - RELEVES '+str(dim)+'D',(0,34,0),.55,root)
 label('Metres 1:1 | 4 reperes locaux | disposition eclatee de travail',(0,33.2,0),.27,root)
 label('Les translations de presentation ne sont PAS une implantation du site.',(0,32.6,0),.23,root)
 if dim==3:label('Surfaces interpolees entre points de bord : pas de terrain ni marches restitues.',(0,32,0),.2,root)
 camd=bpy.data.cameras.new('Plan_general' if dim==2 else 'Axonometrie_releves');cam=bpy.data.objects.new(camd.name,camd);bpy.context.collection.objects.link(cam)
 cam.location=(18,12,65) if dim==2 else (50,-35,48);target=Vector((18,12,0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();camd.type='ORTHO';camd.ortho_scale=64;sc.camera=cam
 out=O/('01-plan-2d' if dim==2 else '02-modele-3d')/('NOKOD_Projet_2_Plan_2D.dae' if dim==2 else 'NOKOD_Projet_2_Modele_3D.dae')
 bpy.ops.wm.collada_export(filepath=str(out),apply_modifiers=True,selected=False,triangulate=True,use_object_instantiation=True,include_children=True,include_armatures=False,include_shapekeys=False,export_mesh_type=0)
 reports.append({'file':str(out.relative_to(O)),'vertices':sum(len(o.data.vertices) for o in sc.objects if o.type=='MESH'),'mesh_objects':sum(o.type=='MESH' for o in sc.objects),'native_sketchup_tested':False})
(H/'export-collada.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
print(json.dumps(reports))
