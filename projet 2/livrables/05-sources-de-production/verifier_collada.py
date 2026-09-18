import bpy,json,xml.etree.ElementTree as E
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;O=H.parent;D=json.loads((H/'releves.json').read_text())['datasets'];R=[]
for dim in (2,3):
 path=O/('01-plan-2d/NOKOD_Projet_2_Plan_2D.dae' if dim==2 else '02-modele-3d/NOKOD_Projet_2_Modele_3D.dae')
 tree=E.parse(path);ns={'c':'http://www.collada.org/2005/11/COLLADASchema'}
 assert tree.find('c:asset/c:unit',ns).get('meter')=='1'
 assert tree.find('c:asset/c:up_axis',ns).text=='Z_UP'
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 bpy.ops.wm.collada_import(filepath=str(path))
 r={'file':str(path.relative_to(O)),'unit_meter':1,'up_axis':'Z_UP','reimport':'Blender 4.5.3 COLLADA importer','sketchup_import_tested':False,'zones':[]}
 for j,d in enumerate(D):
  ob=next(x for x in bpy.context.scene.objects if x.name.startswith('CONTOUR_SOURCE_'+d['name']))
  points=[ob.matrix_world@v.co for v in ob.data.vertices];ref=[Vector((p[0]+d['offset_display'][0],p[1]+d['offset_display'][1],p[2] if dim==3 else 0)) for p in d['points']]
  err=max(min((p-q).length for q in points) for p in ref)
  assert err<.0001,(d['name'],err)
  r['zones'].append({'zone':d['name'],'contour_max_roundtrip_error_m':err,'source_points':len(ref),'imported_points':len(points)})
  if d['closed']:
   su=next(x for x in bpy.context.scene.objects if x.name.startswith(('SURFACE_PROJETEE_' if dim==2 else 'SURFACE_INTERPOLEE_NON_TERRAIN_')+d['name']))
   area=0
   for f in su.data.polygons:
    vs=[su.matrix_world@su.data.vertices[k].co for k in f.vertices];area+=abs(sum(a.x*b.y-b.x*a.y for a,b in zip(vs,vs[1:]+vs[:1])))/2
   assert abs(area-d['area_projected'])<.01
   r['zones'][-1]['area_projected_reimported_m2']=area
 if dim==2:
  zmax=max(abs((o.matrix_world@v.co).z) for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices)
  assert zmax<.0001;r['all_geometry_z_max']=zmax
 # Solid preview, not a final photorealistic render.
 sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='STUDIO';sc.display.shading.color_type='MATERIAL';sc.display.shading.show_shadows=True;sc.display.shading.show_cavity=True
 sc.display.shading.background_type='WORLD';sc.world.color=(1,1,1);sc.view_settings.view_transform='Standard'
 sc.render.resolution_x=1600;sc.render.resolution_y=1200;sc.render.resolution_percentage=100
 sc.camera=next(o for o in sc.objects if o.type=='CAMERA');sc.render.filepath=str(O/'04-controles-et-notice/controle-geometrie'/f'COLLADA_{dim}D_reimporte.png')
 bpy.ops.render.render(write_still=True)
 R.append(r)
(O/'04-controles-et-notice/verification-collada.json').write_text(json.dumps(R,ensure_ascii=False,indent=2));print(json.dumps(R))
