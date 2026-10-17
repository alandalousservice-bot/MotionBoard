import bpy, json, math, os
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = os.path.join(ROOT, "production", "blender", "mb005a")
ASSET_ROOT = os.path.join(ROOT, "assets", "test-only", "quaternius-universal-base-characters")
os.makedirs(OUT, exist_ok=True)
os.makedirs(ASSET_ROOT, exist_ok=True)
SOURCE_DIR = os.environ.get(
    "MOTIONBOARD_QUATERNIUS_SOURCE_DIR",
    os.path.join(ASSET_ROOT, "source", "Base Characters", "Godot - UE"),
)
MODELS = {
    "male": os.path.join(SOURCE_DIR, "Superhero_Male_FullBody.gltf"),
    "female": os.path.join(SOURCE_DIR, "Superhero_Female_FullBody.gltf"),
}

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

def cam(scene, target, position, scale):
    d = bpy.data.cameras.new("EvidenceCamera")
    o = bpy.data.objects.new("EvidenceCamera", d)
    scene.collection.objects.link(o)
    o.location = position
    o.rotation_euler = (Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
    d.type = "ORTHO"
    d.ortho_scale = scale
    scene.camera = o
    return o

def lights(scene, c, e):
    w = bpy.data.worlds.new("EvidenceWorld") if not bpy.data.worlds else bpy.data.worlds[0]
    scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.24,0.27,0.31,1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.7
    for n,power,pos,size in [("Key",950,(c.x-e,c.y-e,c.z+e*1.3),e*.7),("Fill",500,(c.x+e,c.y-e*.2,c.z+e*.6),e*.8),("Rim",750,(c.x,c.y+e,c.z+e),e*.6)]:
        d=bpy.data.lights.new(n,"AREA"); d.energy=power; d.shape="DISK"; d.size=size
        o=bpy.data.objects.new(n,d); scene.collection.objects.link(o); o.location=pos
        o.rotation_euler=(Vector(c)-o.location).to_track_quat("-Z","Y").to_euler()

def stats(objects):
    meshes=[o for o in objects if o.type=="MESH"]; rigs=[o for o in objects if o.type=="ARMATURE"]
    verts=sum(len(o.data.vertices) for o in meshes)
    tris=sum(sum(max(0,len(p.vertices)-2) for p in o.data.polygons) for o in meshes)
    mats=sorted({m.name for o in meshes for m in o.data.materials if m})
    points=[o.matrix_world@Vector(co) for o in meshes for co in o.bound_box]
    mn=[min(v[i] for v in points) for i in range(3)]; mx=[max(v[i] for v in points) for i in range(3)]
    hist={}
    for o in meshes:
        for v in o.data.vertices:
            n=sum(1 for g in v.groups if g.weight>1e-6)
            hist[str(n)]=hist.get(str(n),0)+1
    rig=rigs[0] if rigs else None
    images=[{"name":i.name,"pixels":list(i.size),"filepath":i.filepath} for i in bpy.data.images]
    return {"meshes":[o.name for o in meshes],"mesh_count":len(meshes),"vertices":verts,"triangles":tris,
      "materials":mats,"material_count":len(mats),"armature_count":len(rigs),
      "bones":[b.name for b in rig.data.bones] if rig else [],
      "deform_bones":[b.name for b in rig.data.bones if b.use_deform] if rig else [],
      "vertex_influence_count_histogram":hist,"texture_images":images,
      "bounds_min":mn,"bounds_max":mx,"dimensions":[mx[i]-mn[i] for i in range(3)],
      "animation_actions":[a.name for a in bpy.data.actions]}

def articulation(rig):
    if not rig: return []
    aliases=["upperarm_l","lowerarm_l","hand_l","thigh_l","calf_l","foot_l","upperarm_r","lowerarm_r","thigh_r","calf_r"]
    changed=[]
    for bone in rig.pose.bones:
        lname=bone.name.lower()
        match=next((a for a in aliases if a in lname),None)
        if match:
            angle=25 if "upper" in match or "thigh" in match or "hand" in match or "foot" in match else -35
            bone.rotation_mode="XYZ"; bone.rotation_euler[0]=math.radians(angle)
            changed.append({"bone":bone.name,"x_degrees":angle})
    bpy.context.view_layer.update()
    return changed

def render_candidate(label, imported):
    scene=bpy.context.scene; result=stats(imported)
    mn=Vector(result["bounds_min"]); mx=Vector(result["bounds_max"]); c=(mn+mx)*.5
    dims=Vector(result["dimensions"]); e=max(dims)
    lights(scene,c,e)
    scene.render.engine="CYCLES"; scene.cycles.samples=20
    scene.render.resolution_x=1100; scene.render.resolution_y=1350; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"; scene.view_settings.view_transform="AgX"
    front=mn.y-e*2.8; rear=mx.y+e*2.8; left=mn.x-e*2.8
    views={
      "front":(c,(c.x,front,c.z),e*1.2),
      "side":(c,(left,c.y,c.z),e*1.2),
      "rear":(c,(c.x,rear,c.z),e*1.2),
      "three-quarter":(c,(c.x-e*1.7,front+e*.5,c.z+e*.1),e*1.25),
      "face-closeup":((c.x,c.y,mx.z-dims.z*.13),(c.x,front,c.z+dims.z*.34),e*.36),
      "hand-closeup":((c.x,c.y,mn.z+dims.z*.56),(c.x,front,mn.z+dims.z*.56),e*.32),
      "shoe-closeup":((c.x,c.y,mn.z+dims.z*.06),(c.x,front,mn.z+dims.z*.06),e*.34)}
    for name,(target,pos,scale) in views.items():
        o=cam(scene,target,pos,scale); scene.render.filepath=os.path.join(OUT,f"{label}-{name}.png")
        bpy.ops.render.render(write_still=True); bpy.data.objects.remove(o,do_unlink=True)
    rigs=[o for o in imported if o.type=="ARMATURE"]
    if rigs:
        result["articulation_pose_bones_changed"]=articulation(rigs[0])
        o=cam(scene,c,(c.x-e*1.6,front+e*.5,c.z),e*1.3)
        scene.render.filepath=os.path.join(OUT,f"{label}-articulation-pose.png")
        bpy.ops.render.render(write_still=True); bpy.data.objects.remove(o,do_unlink=True)
        bpy.ops.object.select_all(action="DESELECT"); rigs[0].select_set(True); bpy.context.view_layer.objects.active=rigs[0]
        bpy.ops.object.mode_set(mode="POSE"); bpy.ops.pose.select_all(action="SELECT"); bpy.ops.pose.transforms_clear(); bpy.ops.object.mode_set(mode="OBJECT")
    result["blender_dimensions"]=list(dims)
    return result

def main():
    reports={}
    for label,path in MODELS.items():
        clear_scene(); bpy.ops.import_scene.gltf(filepath=path)
        imported=list(bpy.context.scene.objects)
        reports[label]=render_candidate(label,imported)
        if label=="male":
            bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,"quaternius-male-imported.blend"))
            bpy.ops.object.select_all(action="DESELECT")
            for o in imported: o.select_set(True)
            rigs=[o for o in imported if o.type=="ARMATURE"]
            meshes=[o for o in imported if o.type=="MESH"]
            bpy.context.view_layer.objects.active=rigs[0] if rigs else meshes[0]
            glb=os.path.join(ASSET_ROOT,"quaternius-male-standard-test.glb")
            bpy.ops.export_scene.gltf(filepath=glb,export_format="GLB",use_selection=True,export_animations=True)
            reports[label]["test_glb"]=glb
    with open(os.path.join(OUT,"quaternius-inspection-report.json"),"w",encoding="utf-8") as f: json.dump(reports,f,indent=2)
    print("MB005A_REPORT="+json.dumps(reports))

if __name__=="__main__": main()

