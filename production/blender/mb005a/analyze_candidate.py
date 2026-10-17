import bpy,bmesh,json,math,os
from mathutils import Vector
p=os.path.join(os.path.dirname(__file__),"quaternius-male-imported.blend")
bpy.ops.wm.open_mainfile(filepath=p)
rig=next(o for o in bpy.context.scene.objects if o.type=="ARMATURE")
def point(name,end="head"):
 b=rig.data.bones[name]; local=b.head_local if end=="head" else b.tail_local
 return rig.matrix_world@local
height=1.81008 # body mesh bounds from import, not the 42-vertex helper mesh
landmarks={
 "body_height":height,
 "estimated_head_surface_height":1.81008-1.5998,
 "shoulder_span":2*abs(point("upperarm_l")[0]),
 "upper_arm":rig.data.bones["upperarm_l"].length,
 "forearm":rig.data.bones["lowerarm_l"].length,
 "hand_palm_bone":rig.data.bones["hand_l"].length,
 "thigh":rig.data.bones["thigh_l"].length,
 "lower_leg":rig.data.bones["calf_l"].length,
 "foot_plus_ball":rig.data.bones["foot_l"].length+rig.data.bones["ball_l"].length,
 "hip_height":point("thigh_l")[2],
 "neck_base_height":point("neck_01")[2]
}
landmarks["head_surface_estimate_over_height"]=landmarks["estimated_head_surface_height"]/height
landmarks["shoulder_span_over_height"]=landmarks["shoulder_span"]/height
landmarks["upperarm_over_height"]=landmarks["upper_arm"]/height
landmarks["forearm_over_height"]=landmarks["forearm"]/height
landmarks["thigh_over_height"]=landmarks["thigh"]/height
landmarks["lower_leg_over_height"]=landmarks["lower_leg"]/height
landmarks["foot_bones_over_height"]=landmarks["foot_plus_ball"]/height
meshes=[]
for o in bpy.context.scene.objects:
 if o.type!="MESH": continue
 bm=bmesh.new(); bm.from_mesh(o.data)
 boundary=sum(1 for e in bm.edges if e.is_boundary)
 nonmanifold=sum(1 for e in bm.edges if not e.is_manifold)
 loose=sum(1 for e in bm.edges if not e.link_faces)
 zero=sum(1 for f in bm.faces if f.calc_area()<=1e-12)
 bm.free()
 points=[o.matrix_world@v.co for v in o.data.vertices]
 mins=[min(v[i] for v in points) for i in range(3)]; maxs=[max(v[i] for v in points) for i in range(3)]
 hist={}
 for v in o.data.vertices:
  n=sum(1 for g in v.groups if g.weight>1e-6)
  hist[str(n)]=hist.get(str(n),0)+1
 meshes.append({"name":o.name,"vertices":len(o.data.vertices),"polygons":len(o.data.polygons),
  "triangles":sum(max(0,len(f.vertices)-2) for f in o.data.polygons),"boundary_edges":boundary,
  "nonmanifold_edges":nonmanifold,"loose_edges":loose,"zero_area_faces":zero,
  "dimensions":[round(maxs[i]-mins[i],5) for i in range(3)],"uv_layers":len(o.data.uv_layers),
  "hidden_viewport":o.hide_get(),"hide_viewport":o.hide_viewport,"hide_render":o.hide_render,"weight_histogram":hist})
print(json.dumps({"landmarks":landmarks,"meshes":meshes,"bones":len(rig.data.bones),"finger_bones":sum(1 for b in rig.data.bones if any(k in b.name.lower() for k in ["thumb","index","middle","ring","pinky"]))},indent=2))

