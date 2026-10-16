import bpy, os, json, bmesh
from mathutils import Vector

print('BLENDER_VERSION', bpy.app.version_string, bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash, bytes) else bpy.app.build_hash)
repo=next(r for r in bpy.context.preferences.extensions.repos if r.module=='user_default')
repo.use_custom_directory=True
repo.custom_directory=os.path.join(os.environ['TEMP'],'motionboard-mpfb2-isolated','extensions','user_default')
print('MPFB_INSTALL',bpy.ops.extensions.package_install_files(filepath=os.path.join(os.environ['TEMP'],'motionboard-mpfb2-isolated','add-on-mpfb-v2.0.18.zip'),repo='user_default',enable_on_install=True))
print('MPFB_ENABLED', 'bl_ext.user_default.mpfb' in bpy.context.preferences.addons)
# Keep this run's generated files tidy; this is scoped to the isolated Blender process.
bpy.context.preferences.filepaths.save_version=0
# Clean factory scene.
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
# From scratch, deliberately using MPFB's built-in child anchor (not a final age-matched character).
for key,value in {
    'MPFB_NH_add_phenotype': True,
    'MPFB_NH_phenotype_age': 'child',
    'MPFB_NH_phenotype_gender': 'male',
    'MPFB_NH_phenotype_race': 'universal',
    'MPFB_NH_phenotype_muscle': 'minmuscle',
    'MPFB_NH_phenotype_weight': 'minweight',
    'MPFB_NH_phenotype_height': 'minheight',
    'MPFB_NH_phenotype_proportions': 'min',
    'MPFB_NH_phenotype_influence': 1.0,
    'MPFB_NH_scale_factor': 'METER',
}.items():
    if hasattr(scene,key): setattr(scene,key,value)
    else: print('SCENE_PROP_MISSING',key)
print('CREATE_OP',bpy.ops.mpfb.create_human())
body=bpy.context.view_layer.objects.active
assert body is not None and body.type=='MESH', 'MPFB did not produce an active mesh'
body.name='MPFB2 Child Anchor Base Mesh (feasibility only)'
body.data.name='MPFB2 hm08 child-anchor base mesh'
# Add MPFB built-in standard rig for a basic compatibility inspection.
rig_result='not attempted'
try:
    setattr(scene,'MPFB_ADR_standard_rig','default')
    rig_result=str(bpy.ops.mpfb.add_standard_rig())
except Exception as e:
    rig_result='FAILED: '+repr(e)
print('RIG_RESULT',rig_result)
# Inventory scene and mesh health.
mesh=body.data
verts=len(mesh.vertices); edges=len(mesh.edges); faces=len(mesh.polygons)
lo=[min(v.co[i] for v in mesh.vertices) for i in range(3)]
hi=[max(v.co[i] for v in mesh.vertices) for i in range(3)]
bm=bmesh.new(); bm.from_mesh(mesh)
nonmanifold=sum(1 for e in bm.edges if not e.is_manifold)
boundary=sum(1 for e in bm.edges if e.is_boundary)
wire=sum(1 for e in bm.edges if e.is_wire)
zero_area=sum(1 for f in bm.faces if f.calc_area() <= 1e-12)
bm.free()
shape_keys=[] if mesh.shape_keys is None else [b.name for b in mesh.shape_keys.key_blocks]
armatures=[o for o in scene.objects if o.type=='ARMATURE']
vg=len(body.vertex_groups)
summary={'blender_version':bpy.app.version_string,'mpfb_version':'2.0.18','created_mesh':body.name,'vertices':verts,'edges':edges,'faces':faces,'dimensions':body.dimensions[:],'bbox_min':lo,'bbox_max':hi,'shape_keys_count':len(shape_keys),'shape_keys_sample':shape_keys[:12],'vertex_groups':vg,'armatures':[a.name for a in armatures],'rig_result':rig_result,'nonmanifold_edges':nonmanifold,'boundary_edges':boundary,'wire_edges':wire,'zero_area_faces':zero_area,'material_slots':len(mesh.materials),'mesh_objects':[o.name for o in scene.objects if o.type=='MESH']}
print('MESH_REPORT_JSON',json.dumps(summary,default=list))
# neutral preview, simple studio setup, mesh only.
for o in list(scene.objects):
    if o.type!='MESH': o.hide_render=True
body.hide_render=False
mat=bpy.data.materials.new('Neutral feasibility preview'); mat.diffuse_color=(0.52,0.56,0.60,1)
bs=mat.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(0.48,0.52,0.56,1); bs.inputs['Roughness'].default_value=0.78
body.data.materials.clear(); body.data.materials.append(mat)
# Camera helpers; assumes MPFB uses Z-up, front toward -Y.
center=Vector((0,0,(lo[2]+hi[2])/2))
world=bpy.data.worlds.new('Neutral preview world') if bpy.data.worlds.get('Neutral preview world') is None else bpy.data.worlds['Neutral preview world']
scene.world=world; world.color=(0.18,0.18,0.18)
scene.render.engine='BLENDER_EEVEE'; scene.render.resolution_x=900; scene.render.resolution_y=1100; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False
scene.view_settings.view_transform='Standard'; scene.view_settings.look='Medium High Contrast'; scene.display.shading.light='STUDIO'
# lights
for name,loc,power,size in [('Key',(3,-4,5),160,4),('Fill',(-4,-2,2),80,4),('Rim',(1,3,4),120,3)]:
    ld=bpy.data.lights.new(name,'AREA'); ld.energy=power; ld.shape='DISK'; ld.size=size
    ob=bpy.data.objects.new(name,ld); scene.collection.objects.link(ob); ob.location=loc; ob.rotation_euler=(Vector(center)-ob.location).to_track_quat('-Z','Y').to_euler()

def camera(name,loc):
    cd=bpy.data.cameras.new(name); cam=bpy.data.objects.new(name,cd); scene.collection.objects.link(cam); cam.location=loc; cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler(); cd.type='ORTHO'; cd.ortho_scale=(hi[2]-lo[2])*1.2; scene.camera=cam
    return cam
outdir=os.path.dirname(os.path.abspath(__file__))
# __file__ is repo script path; output assets are under sibling directory.
for view,loc in [('front',(0,-5,center.z)),('side',(5,0,center.z))]:
    c=camera('Preview '+view,loc); scene.render.filepath=os.path.join(outdir,'mpfb2-child-anchor-'+view+'.png'); bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(c,do_unlink=True)
# Remove helpers and save inspectable source. The mesh and attached rig (if generated) remain.
for o in list(scene.objects):
    if o.type in {'LIGHT','CAMERA'}: bpy.data.objects.remove(o,do_unlink=True)
scene.camera=None
blend=os.path.join(outdir,'mpfb2-child-anchor-feasibility.blend')
bpy.ops.wm.save_as_mainfile(filepath=blend)
# WebGL compatibility smoke test: export this feasibility-only mesh and rig as GLB.
arm=bpy.data.objects.get('MPFB2 Child Anchor Base Mesh (feasibility only).rig')
for o in list(bpy.context.selected_objects): o.select_set(False)
body.select_set(True)
if arm: arm.select_set(True)
glb=os.path.join(outdir,'mpfb2-child-anchor-feasibility.glb')
bpy.ops.export_scene.gltf(filepath=glb,export_format='GLB',use_selection=True,export_animations=False)
print('GLB_EXPORTED',glb,os.path.getsize(glb))
before=set(o.name for o in bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=glb)
new=[o for o in bpy.context.scene.objects if o.name not in before]
print('GLB_ROUNDTRIP',json.dumps({'objects':[o.name for o in new],'meshes':sum(o.type=='MESH' for o in new),'armatures':sum(o.type=='ARMATURE' for o in new)}))
with open(os.path.join(outdir,'mesh-report.json'),'w',encoding='utf-8') as f: json.dump(summary,f,indent=2,default=list)
