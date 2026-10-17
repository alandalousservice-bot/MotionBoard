import bpy, json, math, os
from mathutils import Vector

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..",".."))
OUT=os.path.join(ROOT,"production","blender","mb005a")
ASSET=os.path.join(ROOT,"assets","test-only","quaternius-universal-base-characters")
SRC=os.environ.get("MOTIONBOARD_QUATERNIUS_SOURCE_DIR",os.path.join(ASSET,"source","Base Characters","Godot - UE"))
MALE=os.path.join(SRC,"Superhero_Male_FullBody.gltf")
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=MALE)
objs=list(bpy.context.scene.objects)
rig=next(o for o in objs if o.type=="ARMATURE")
# The delivered glTF has two normal-map URI typos. Repoint only the imported image datablocks
# to the identically named files in the archive; the source glTF and extracted textures stay unmodified.
for image in bpy.data.images:
    if image.source=="FILE" and image.filepath and not os.path.exists(bpy.path.abspath(image.filepath)):
        corrected=image.filepath.replace("_png.png",".png")
        if corrected != image.filepath and os.path.exists(bpy.path.abspath(corrected)):
            image.filepath=corrected
            image.reload()
for image in bpy.data.images:
    if image.source=="FILE" and image.size[0]>0:
        try: image.pack()
        except Exception: pass
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,"quaternius-male-imported.blend"))
bpy.ops.object.select_all(action="DESELECT")
for o in objs: o.select_set(True)
bpy.context.view_layer.objects.active=rig
glb=os.path.join(ASSET,"quaternius-male-standard-test.glb")
bpy.ops.export_scene.gltf(filepath=glb,export_format="GLB",use_selection=True,export_animations=True)
print("FINALIZED_GLBSIZE="+str(os.path.getsize(glb)))
print("PACKED_IMAGES="+json.dumps([i.name for i in bpy.data.images if i.packed_file]))

