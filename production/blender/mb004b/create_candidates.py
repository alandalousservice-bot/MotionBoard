import bpy, json, math, os
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__))
BASE=os.path.abspath(os.path.join(ROOT,'..','mpfb2-feasibility','mpfb2-child-anchor-feasibility.blend'))
OUT=os.path.join(ROOT,'candidates'); os.makedirs(OUT,exist_ok=True)
DATA=[
 {'label':'7-year-band reference vector','age_band_months':'84-95','sample_stature_m':1.278,'head_height_ratio':0.1495,'sitting_height_ratio':0.5469,'shoulder_breadth_ratio':0.2457,'upper_arm_ratio':0.2081,'elbow_hand_ratio':0.2613,'hand_length_ratio':0.1072,'foot_length_ratio':0.1557},
 {'label':'8-year-band reference vector','age_band_months':'96-107','sample_stature_m':1.292,'head_height_ratio':0.1440,'sitting_height_ratio':0.5333,'shoulder_breadth_ratio':0.2446,'upper_arm_ratio':0.2051,'elbow_hand_ratio':0.2655,'hand_length_ratio':0.1068,'foot_length_ratio':0.1563},
 {'label':'9-year-band reference vector','age_band_months':'108-119','sample_stature_m':1.394,'head_height_ratio':0.1399,'sitting_height_ratio':0.5287,'shoulder_breadth_ratio':0.2346,'upper_arm_ratio':0.2052,'elbow_hand_ratio':0.2690,'hand_length_ratio':0.1098,'foot_length_ratio':0.1600},
]
BASE_H=1.0053783655166626
BASE_SHOULDER_RATIO=0.2450 # sizing reference only, not measured from MPFB torso landmarks
BASE_FOOT_RATIO=0.1560      # sizing reference only, not measured from MPFB foot landmarks

def clean():
 bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
 for datablocks in (bpy.data.meshes,bpy.data.armatures,bpy.data.cameras,bpy.data.lights,bpy.data.curves):
  for d in list(datablocks):
   if d.users==0: datablocks.remove(d)

def load_candidate(d,index):
 bpy.ops.wm.open_mainfile(filepath=BASE)
 mesh=next(o for o in bpy.context.scene.objects if o.type=='MESH')
 rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
 # The records are displayed as bounded exploration variants. Uniform stature and tiny
 # whole-axis factors show the sensitivity of a single MPFB mesh; they are not local anatomy morphs.
 sz=d['sample_stature_m']/BASE_H
 sx=d['shoulder_breadth_ratio']/BASE_SHOULDER_RATIO
 sy=d['foot_length_ratio']/BASE_FOOT_RATIO
 rig.scale=(sx*sz,sy*sz,sz)
 mesh.scale=(1,1,1)
 for obj in (mesh,rig): obj.name=f"MB004B {index:02d} {d['age_band_months']} {obj.type.lower()} — exploratory only"
 mesh.data.name=f"MB004B sample {index:02d} child anchor mesh — exploratory only"
 mesh['proportion_status']='EXPLORATORY SCALE PROBE; not an age-validated child mesh'
 mesh['reference_source']='NIST/CPSC AnthroKids 1977 individual sample; anonymized representative ratio vector'
 mesh['reference_age_band_months']=d['age_band_months']
 mesh['reference_measurements_json']=json.dumps(d,ensure_ascii=False)
 mesh['nonuniform_global_scale']=[sx*sz,sy*sz,sz]
 mesh['approval']='pending artist and Product Owner review'
 return mesh,rig

# Individual editable sources.
for i,d in enumerate(DATA,1):
 mesh,rig=load_candidate(d,i)
 out=os.path.join(OUT,f'mb004b-candidate-{i:02d}-{d["age_band_months"].split("-")[0]}m-exploratory.blend')
 bpy.context.preferences.filepaths.save_version=0
 bpy.ops.wm.save_as_mainfile(filepath=out)
 print('CANDIDATE_SOURCE',out,os.path.getsize(out))

# Comparative render scene: three identical-base probes, translated side-by-side.
bpy.ops.wm.open_mainfile(filepath=BASE)
base_mesh=next(o for o in bpy.context.scene.objects if o.type=='MESH')
base_rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
# drop lights/camera from source and keep shared mesh/rig data in copies
for o in list(bpy.context.scene.objects):
 if o.type in {'CAMERA','LIGHT'}: bpy.data.objects.remove(o,do_unlink=True)
objects=[]
for i,d in enumerate(DATA,1):
 if i==1: mesh,rig=base_mesh,base_rig
 else:
  mesh=base_mesh.copy(); mesh.data=base_mesh.data.copy(); bpy.context.scene.collection.objects.link(mesh)
  rig=base_rig.copy(); rig.data=base_rig.data.copy(); bpy.context.scene.collection.objects.link(rig); mesh.parent=rig
  for mod in mesh.modifiers:
   if mod.type=='ARMATURE': mod.object=rig
 sz=d['sample_stature_m']/BASE_H; sx=d['shoulder_breadth_ratio']/BASE_SHOULDER_RATIO; sy=d['foot_length_ratio']/BASE_FOOT_RATIO
 offset=(i-2)*0.88
 rig.scale=(sx*sz,sy*sz,sz); rig.location.x=offset
 mesh.scale=(1,1,1); mesh.location=(0,0,0)
 mesh.name=f"Candidate {i} {d['age_band_months']} months — exploratory"
 mesh['approval']='pending artist and Product Owner review'
 objects.append(mesh)
# light-neutral studio
scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1500; scene.render.resolution_y=900; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
scene.view_settings.view_transform='Standard'; scene.view_settings.look='Medium High Contrast'
world=bpy.data.worlds.new('MB004B neutral studio') if bpy.data.worlds.get('MB004B neutral studio') is None else bpy.data.worlds['MB004B neutral studio']
scene.world=world; world.color=(0.18,0.18,0.18)
for name,loc,power,size in [('Key',(0,-4,3.5),120,5),('Fill',(-3,-2,2),60,4),('Rim',(1,3,3),100,3)]:
 ld=bpy.data.lights.new(name,'AREA'); ld.energy=power; ld.shape='DISK'; ld.size=size; ob=bpy.data.objects.new(name,ld); scene.collection.objects.link(ob); ob.location=loc; ob.rotation_euler=(Vector((0,0,0.68))-ob.location).to_track_quat('-Z','Y').to_euler()
# Ground/camera-independent labels are intentionally omitted; report binds left-to-right order.

def render_view(view,loc):
 cd=bpy.data.cameras.new('MB004B '+view); cam=bpy.data.objects.new('MB004B '+view,cd);scene.collection.objects.link(cam);cam.location=loc;cam.rotation_euler=(Vector((0,0,0.69))-cam.location).to_track_quat('-Z','Y').to_euler(); cd.type='ORTHO'; cd.ortho_scale=6.0;scene.camera=cam
 scene.render.filepath=os.path.join(ROOT,f'mb004b-comparison-{view}.png');bpy.ops.render.render(write_still=True);bpy.data.objects.remove(cam,do_unlink=True)
for view,loc in [('front',(0,-7,0.69)),('side',(7,0,0.69)),('three-quarter',(5,-6,0.69))]: render_view(view,loc)
# Export the median-band candidate with the exact MPFB rig, no animation.
# Scaled mesh+armature are exported together; viewer check evaluates loading/materials/rig presence.
mesh=objects[1]; rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE' and abs(o.location.x)<0.001)
for o in bpy.context.selected_objects: o.select_set(False)
mesh.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=mesh
out=os.path.join(ROOT,'mb004b-candidate-02-test.glb')
bpy.ops.export_scene.gltf(filepath=out,export_format='GLB',use_selection=True,export_animations=False)
print('TEST_GLB',out,os.path.getsize(out))
with open(os.path.join(ROOT,'candidate-reference-vectors.json'),'w',encoding='utf8') as f: json.dump(DATA,f,ensure_ascii=False,indent=2)
