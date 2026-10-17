import bpy,os
from mathutils import Vector
OUT=os.path.dirname(__file__)
bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT,"quaternius-male-imported.blend"))
scene=bpy.context.scene
# Reuse existing area lights, reset world and render setup.
scene.render.engine="CYCLES"; scene.cycles.samples=24
scene.render.resolution_x=1100; scene.render.resolution_y=1350; scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"; scene.view_settings.view_transform="AgX"
def render(name,target,pos,scale):
 d=bpy.data.cameras.new("FeatureCamera"); c=bpy.data.objects.new("FeatureCamera",d); scene.collection.objects.link(c)
 c.location=pos; c.rotation_euler=(Vector(target)-c.location).to_track_quat("-Z","Y").to_euler(); d.type="ORTHO"; d.ortho_scale=scale; scene.camera=c
 ld=bpy.data.lights.new("FeatureFill","AREA"); ld.energy=1400; ld.shape="DISK"; ld.size=0.7
 light=bpy.data.objects.new("FeatureFill",ld); scene.collection.objects.link(light); light.location=pos
 light.rotation_euler=(Vector(target)-light.location).to_track_quat("-Z","Y").to_euler()
 scene.render.filepath=os.path.join(OUT,name+".png"); bpy.ops.render.render(write_still=True)
 bpy.data.objects.remove(c,do_unlink=True); bpy.data.objects.remove(light,do_unlink=True)
render("male-hand-closeup",(0.83,0.02,1.455),(0.83,-2.1,1.455),0.36)
render("male-shoe-closeup",(0.11,-0.06,0.05),(0.35,-2.0,0.16),0.32)

