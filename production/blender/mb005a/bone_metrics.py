import bpy,json,os
from mathutils import Vector
p=r"D:\andalouse app\production\blender\mb005a\quaternius-male-imported.blend"
bpy.ops.wm.open_mainfile(filepath=p)
rig=next(o for o in bpy.context.scene.objects if o.type=="ARMATURE")
names=["root","pelvis","spine_01","spine_02","spine_03","neck_01","Head","clavicle_l","upperarm_l","lowerarm_l","hand_l","thigh_l","calf_l","foot_l","ball_l","clavicle_r","upperarm_r","lowerarm_r","hand_r","thigh_r","calf_r","foot_r","ball_r"]
data={}
for n in names:
 b=rig.data.bones.get(n)
 if b:
  h=rig.matrix_world@b.head_local; t=rig.matrix_world@b.tail_local
  data[n]={"head":[round(v,6) for v in h],"tail":[round(v,6) for v in t],"length":round(b.length,6)}
for side in ("l","r"):
 hand=rig.data.bones.get(f"hand_{side}")
 middle=rig.data.bones.get(f"middle_04_leaf_{side}")
 if hand and middle:
  wrist=rig.matrix_world@hand.head_local; fingertip=rig.matrix_world@middle.tail_local
  data[f"wrist_to_middle_fingertip_{side}"]={"distance":round((fingertip-wrist).length,6),"wrist":[round(v,6) for v in wrist],"tip":[round(v,6) for v in fingertip]}
meshdata={}
for o in bpy.context.scene.objects:
 if o.type=="MESH":
  pts=[o.matrix_world@v.co for v in o.data.vertices]
  mn=[min(v[i] for v in pts) for i in range(3)]; mx=[max(v[i] for v in pts) for i in range(3)]
  meshdata[o.name]={"vertices":len(o.data.vertices),"polygons":len(o.data.polygons),"dimensions":[round(mx[i]-mn[i],5) for i in range(3)],"bounds":[[round(v,5) for v in mn],[round(v,5) for v in mx]]}
print(json.dumps({"bones":data,"meshes":meshdata},indent=2))

