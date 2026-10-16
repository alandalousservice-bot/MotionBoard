import bpy,bmesh,json,math,os
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__))
blend=os.path.join(ROOT,'candidates','mb004b-candidate-02-96m-exploratory.blend')
bpy.ops.wm.open_mainfile(filepath=blend)
mesh=next(o for o in bpy.context.scene.objects if o.type=='MESH')
rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
# Classify boundary loops by their centroid into spatial zones and report counts.
bm=bmesh.new();bm.from_mesh(mesh.data);bound=[e for e in bm.edges if e.is_boundary]
zmin=min(v.co.z for v in bm.verts);zmax=max(v.co.z for v in bm.verts);zspan=max(zmax-zmin,1e-9)
adj={v:set() for e in bound for v in e.verts}
for e in bound:
 a,b=e.verts;adj[a].add(b);adj[b].add(a)
seen=set();loops=[]
for v in adj:
 if v in seen: continue
 stack=[v];seen.add(v);vs=[]
 while stack:
  x=stack.pop();vs.append(x)
  for y in adj[x]:
   if y not in seen:seen.add(y);stack.append(y)
 coords=[v.co for v in vs]; cx=sum(c.x for c in coords)/len(coords);cy=sum(c.y for c in coords)/len(coords);cz=sum(c.z for c in coords)/len(coords)
 ec=sum(1 for e in bound if e.verts[0] in vs and e.verts[1] in vs)
 zf=(cz-zmin)/zspan
 if zf<.09: zone='foot/toe';
 elif zf<.36: zone='ankle/lower-leg';
 elif zf<.49: zone='pelvis/thigh';
 elif zf<.70: zone='torso/arm-root';
 elif zf<.84: zone='arm/shoulder';
 else: zone='head/face'
 loops.append({'zone':zone,'edges':ec,'vertices':len(vs),'center':[round(cx,4),round(cy,4),round(cz,4)]})
bm.free()
# Weight audit: high influence count and weight discarded by top-four normalization.
vg={g.index:g.name for g in mesh.vertex_groups};counts={};discard=[]
for v in mesh.data.vertices:
 weights=sorted([g.weight for g in v.groups if g.weight>1e-8],reverse=True)
 counts[len(weights)]=counts.get(len(weights),0)+1
 if len(weights)>4: discard.append(sum(weights[4:])/sum(weights))
# measure evaluator changes for isolated major joint probes
pose_tests=[('shoulder','upperarm02.L',1,0.45),('elbow','lowerarm02.L',0,0.65),('wrist','wrist.L',1,0.35),('hip','upperleg02.L',1,0.35),('knee','lowerleg02.L',0,0.55),('ankle','foot.L',1,0.35),('finger','finger2-1.L',0,0.50),('thumb','finger1-1.L',0,0.45)]
scene=bpy.context.scene;scene.frame_set(1)
for pb in rig.pose.bones: pb.rotation_mode='XYZ';pb.rotation_euler=(0,0,0)
# Clone the same geometry and explicitly retain only the four strongest weights per
# vertex, matching the glTF skin limit, then compare it to Blender's full-weight skin.
trim_mesh=mesh.copy();trim_mesh.data=mesh.data.copy();scene.collection.objects.link(trim_mesh)
trim_mesh.name='MB004B top-four joint influence comparison only'
for v in trim_mesh.data.vertices:
 entries=sorted([(g.group,g.weight) for g in v.groups],key=lambda x:x[1],reverse=True)
 keep=entries[:4];total=sum(w for _,w in keep)
 for group in list(trim_mesh.vertex_groups):
  if all(group.index!=idx for idx,_ in keep):
   try: group.remove([v.index])
   except RuntimeError: pass
 if total>0:
  for idx,w in keep: trim_mesh.vertex_groups[idx].add([v.index],w/total,'REPLACE')
def evaluated_coords(obj):
 bpy.context.view_layer.update();ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();out=[ev.matrix_world@v.co for v in me.vertices];ev.to_mesh_clear();return out
rest=evaluated_coords(mesh);trim_rest=evaluated_coords(trim_mesh);pose_results=[]
for label,bone,axis,angle in pose_tests:
 for pb in rig.pose.bones:pb.rotation_euler=(0,0,0)
 pb=rig.pose.bones.get(bone)
 if pb is None: pose_results.append({'joint':label,'bone':bone,'result':'MISSING'});continue
 pb.rotation_euler[axis]=angle
 posed=evaluated_coords(mesh);trimposed=evaluated_coords(trim_mesh);disp=[(a-b).length for a,b in zip(posed,rest)]; trim_error=[(a-b).length for a,b in zip(posed,trimposed)]
 pose_results.append({'joint':label,'bone':bone,'radians':angle,'max_vertex_displacement_m':round(max(disp),6),'changed_vertices_gt_1mm':sum(d>0.001 for d in disp),'top_four_skinning_max_vertex_difference_m':round(max(trim_error),6),'top_four_skinning_mean_vertex_difference_m':round(sum(trim_error)/len(trim_error),6),'result':'PASS' if max(disp)>0.001 else 'FAIL'})
# Do not leave the comparison-only duplicate in the editable source or export.
bpy.data.objects.remove(trim_mesh,do_unlink=True)
# Build one named rig-test action for browser loading/playback; only technical articulation, no educational movement.
for pb in rig.pose.bones:pb.rotation_euler=(0,0,0);pb.keyframe_insert(data_path='rotation_euler',frame=1,group=pb.name)
pose_angles={'upperarm02.L':(0.0,0.45,0.0),'lowerarm02.L':(0.65,0.0,0.0),'wrist.L':(0.0,0.35,0.0),'upperleg02.L':(0.0,0.35,0.0),'lowerleg02.L':(0.55,0.0,0.0),'foot.L':(0.0,0.35,0.0),'finger2-1.L':(0.50,0.0,0.0),'finger2-2.L':(0.40,0.0,0.0),'finger1-1.L':(0.0,0.45,0.0)}
for index,(name,rot) in enumerate(pose_angles.items()):
 pb=rig.pose.bones.get(name)
 if not pb:continue
 start=1+index*12
 pb.rotation_euler=(0,0,0);pb.keyframe_insert(data_path='rotation_euler',frame=start,group=pb.name)
 pb.rotation_euler=rot;pb.keyframe_insert(data_path='rotation_euler',frame=start+4,group=pb.name)
 pb.rotation_euler=(0,0,0);pb.keyframe_insert(data_path='rotation_euler',frame=start+8,group=pb.name)
scene.frame_end=1+(len(pose_angles)-1)*12+8;scene.render.fps=30
if rig.animation_data and rig.animation_data.action:rig.animation_data.action.name='MB004B_RIG_TEST_NOT_EDUCATIONAL'
scene.frame_set(31)
# Render before/after pose for Blender evidence.
for o in list(scene.objects):
 if o.type in {'CAMERA','LIGHT'}: bpy.data.objects.remove(o,do_unlink=True)
scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard'
for name,loc,power,size in [('Key',(2,-4,3),100,3),('Fill',(-3,-2,1),45,3),('Rim',(1,3,2),60,2)]:
 ld=bpy.data.lights.new(name,'AREA');ld.energy=power;ld.shape='DISK';ld.size=size;ob=bpy.data.objects.new(name,ld);scene.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector((0,0,.65))-ob.location).to_track_quat('-Z','Y').to_euler()
camdat=bpy.data.cameras.new('Rig test camera');cam=bpy.data.objects.new('Rig test camera',camdat);scene.collection.objects.link(cam);cam.location=(3,-5,.68);cam.rotation_euler=(Vector((0,0,.68))-cam.location).to_track_quat('-Z','Y').to_euler();camdat.type='ORTHO';camdat.ortho_scale=2.1;scene.camera=cam
scene.frame_set(1);scene.render.filepath=os.path.join(ROOT,'mb004b-rig-test-rest.png');bpy.ops.render.render(write_still=True)
scene.frame_set(1+4*12+4);scene.render.filepath=os.path.join(ROOT,'mb004b-rig-test-pose.png');bpy.ops.render.render(write_still=True)
# Store editable rig test source.
poseblend=os.path.join(ROOT,'mb004b-candidate-02-rig-test.blend');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=poseblend)
# GLB include this one technical pose clip for viewer load/playback testing.
for o in bpy.context.selected_objects:o.select_set(False)
mesh.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=mesh
out=os.path.join(ROOT,'mb004b-candidate-02-test.glb')
source_clip=rig.animation_data.action.name if rig.animation_data and rig.animation_data.action else None
bpy.ops.export_scene.gltf(filepath=out,export_format='GLB',use_selection=True,export_animations=True)
# Reimport for clip and skeleton smoke check.
before=set(o.name for o in scene.objects);bpy.ops.import_scene.gltf(filepath=out);new=[o for o in scene.objects if o.name not in before]
clips=[]
if source_clip:
 a=bpy.data.actions.get(source_clip)
 if a: clips.append({'name':a.name,'frame_range':list(a.frame_range)})
report={'blender':bpy.app.version_string,'mesh':mesh.name,'boundary_edge_total':len(bound),'boundary_loop_total':len(loops),'boundary_loops_by_zone':{z:sum(1 for x in loops if x['zone']==z) for z in sorted({x['zone'] for x in loops})},'boundary_edges_by_zone':{z:sum(x['edges'] for x in loops if x['zone']==z) for z in sorted({x['zone'] for x in loops})},'largest_boundary_loops':sorted(loops,key=lambda x:x['edges'],reverse=True)[:20],'influence_vertices_by_count':counts,'vertices_over_four_influences':sum(discard!=0 for discard in discard),'maximum_dropped_weight_per_vertex':round(max(discard,default=0),6),'mean_dropped_weight_per_overlimit_vertex':round(sum(discard)/len(discard),6) if discard else 0,'pose_tests':pose_results,'glb_size_bytes':os.path.getsize(out),'glb_roundtrip_new_objects':[o.name for o in new],'clips':clips,'pose_test_source':os.path.basename(poseblend)}
with open(os.path.join(ROOT,'mb004b-rig-export-report.json'),'w',encoding='utf8') as f:json.dump(report,f,indent=2)
print('MB004B_REPORT',json.dumps(report))
