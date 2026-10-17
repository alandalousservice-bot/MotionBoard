"""Build a non-final, editable MPFB2 anatomy/face prototype for MB-006.

This operates on the committed MPFB2 hm08 child-anchor base. It uses local,
smooth vertex deformations and retains the MPFB mesh, shape keys, modifiers,
vertex groups, and rig. It is not a validated age model or an approved asset.
"""

import bpy
import json
import math
import os
from mathutils import Vector


ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", ".."))
BASE = os.path.join(REPO, "production", "blender", "mpfb2-feasibility",
                    "mpfb2-child-anchor-feasibility.blend")
OUT = ROOT
BLENDER_PROFILE = os.environ.get("BLENDER_USER_CONFIG", "")

if not os.path.isfile(BASE):
    raise FileNotFoundError(BASE)

bpy.ops.wm.open_mainfile(filepath=BASE)
bpy.context.preferences.filepaths.save_version = 0
scene = bpy.context.scene
body = next(obj for obj in scene.objects if obj.type == "MESH")
rig = next(obj for obj in scene.objects if obj.type == "ARMATURE")

body.name = "MB006 MPFB2 child anatomy prototype — draft"
body.data.name = "MB006 editable MPFB2 hm08 child-anchor mesh"
body["prototype_status"] = "DRAFT — technical and visual approval pending"
body["base_source"] = "MPFB2 2.0.18 bundled hm08 child anchor; CC0 core assets"
body["age_claim"] = "Approximate school-age appearance only; not age-validated"
body["proportion_reference"] = (
    "NIST/CPSC AnthroKids 1977, one anonymized 96–107 month record used as context; "
    "not a medical norm or Algerian template"
)
body["face_status"] = "Neutral base face with local cheek/jaw prototype edits; no facial rig"

if not body.data.shape_keys or not body.vertex_groups.get("body"):
    raise RuntimeError("Expected editable MPFB2 shape keys and body vertex group")

# Vertex-group weights limit changes to the visible base body, leaving helper
# geometry and the imported rig-control helpers untouched.
body_group = body.vertex_groups["body"].index
groups = {group.name: group.index for group in body.vertex_groups}

def group_weight(vertex, index):
    for assignment in vertex.groups:
        if assignment.group == index:
            return assignment.weight
    return 0.0

def gaussian(value, center, sigma):
    return math.exp(-0.5 * ((value - center) / sigma) ** 2)

def smooth_profile(z, center, sigma, amplitude):
    return amplitude * gaussian(z, center, sigma)

def transform_local(co, body_weight):
    """Small proportional edits in MPFB base-mesh coordinates."""
    x, y, z = co.x, co.y, co.z
    w = min(1.0, body_weight)

    # Child torso silhouette: modestly broaden the shoulder/chest transition,
    # then soften the waist and pelvis instead of applying one body-wide scale.
    shoulder = smooth_profile(z, 1.315, 0.070, 0.075)
    chest = smooth_profile(z, 1.135, 0.105, 0.025)
    waist = smooth_profile(z, 0.990, 0.085, -0.045)
    pelvis = smooth_profile(z, 0.785, 0.100, -0.035)
    x *= 1.0 + w * (shoulder + chest + waist + pelvis)

    # Slightly strengthen the child neck transition without moving the head.
    neck = smooth_profile(z, 1.390, 0.055, 0.035)
    y_center = -0.015
    y = y_center + (y - y_center) * (1.0 + w * neck)

    # Local face correction: broaden the cheek zone gently and taper the lower
    # jaw a little. No eye enlargement, smile, or cartoon facial exaggeration.
    head_weight = group_weight_for_current_vertex
    if head_weight > 0.1 and y < -0.045:
        cheek = smooth_profile(z, 1.535, 0.040, 0.025)
        jaw = smooth_profile(z, 1.455, 0.035, -0.020)
        x *= 1.0 + min(1.0, head_weight) * (cheek + jaw)
        nose = smooth_profile(z, 1.525, 0.022, 0.012)
        if abs(x) < 0.020:
            y -= nose

    return Vector((x, y, z))

head_index = groups.get("head")
if head_index is None:
    raise RuntimeError("MPFB2 base is missing the head deformation group")

shape_keys = body.data.shape_keys.key_blocks
base_key = shape_keys.get("Basis")
prototype_key = body.shape_key_add(name="MB006_LocalAnatomy_Prototype", from_mix=False)
prototype_key.relative_key = base_key

for index, vertex in enumerate(body.data.vertices):
    body_weight = group_weight(vertex, body_group)
    head_weight = group_weight(vertex, head_index)
    group_weight_for_current_vertex = head_weight
    base_coordinate = base_key.data[index].co.copy()
    prototype_key.data[index].co = transform_local(base_coordinate, body_weight)
prototype_key.value = 1.0

# Stretch only the distal fingers by a few percent from the existing wrist
# anchors. This is a preliminary proportion adjustment, not a grasping test.
for side, sign in (("L", 1.0), ("R", -1.0)):
    finger_indices = [
        idx for name, idx in groups.items()
        if name.startswith("finger") and name.endswith("." + side)
    ]
    if not finger_indices:
        continue
    wrist = rig.data.bones.get("wrist." + side)
    if wrist is None:
        continue
    # The source armature and mesh share a bind-space basis. This point is used
    # only as a local radial pivot for the modest digit extension.
    pivot = wrist.head_local.copy()
    for vertex in body.data.vertices:
        finger_weight = max((group_weight(vertex, idx) for idx in finger_indices), default=0.0)
        body_weight = group_weight(vertex, body_group)
        if finger_weight <= 0.05 or body_weight <= 0.05:
            continue
        key_point = prototype_key.data[vertex.index].co
        key_point.x = pivot.x + (key_point.x - pivot.x) * (1.0 + 0.035 * finger_weight)
        key_point.y = pivot.y + (key_point.y - pivot.y) * (1.0 + 0.035 * finger_weight)

# Foot-length adjustment is localized to the existing foot/toe weights.
for side in ("L", "R"):
    foot_indices = [
        idx for name, idx in groups.items()
        if (name == "foot." + side or (name.startswith("toe") and name.endswith("." + side)))
    ]
    for vertex in body.data.vertices:
        foot_weight = max((group_weight(vertex, idx) for idx in foot_indices), default=0.0)
        if foot_weight <= 0.05 or group_weight(vertex, body_group) <= 0.05:
            continue
        key_point = prototype_key.data[vertex.index].co
        # MPFB's front is local -Y. Extend the forefoot/toe contour slightly.
        key_point.y = -0.045 + (key_point.y + 0.045) * (1.0 + 0.025 * foot_weight)

# Use one existing 8-year reference-vector stature only to set scene scale for
# visual comparison. Scaling the mesh object and armature together compounds
# the deformation; keep mesh object scale at 1 and scale the armature only.
# This is not evidence of age suitability and does not alter body proportions.
target_stature_m = 1.292
current_stature_m = float(body.dimensions.z)
stature_scale = target_stature_m / current_stature_m
body.scale = (1.0, 1.0, 1.0)
rig.scale = (stature_scale,) * 3
body["scene_scale_context_m"] = target_stature_m
body["age_claim"] = "No age suitability claim; stature is scene-scale context only"
body["context_scale_factor"] = stature_scale

# The appearance material is intentionally simple, with no external texture
# or additional licensed asset pack.
skin = bpy.data.materials.get("MB006 temporary skin evaluation material")
if skin is None:
    skin = bpy.data.materials.new("MB006 temporary skin evaluation material")
skin.diffuse_color = (0.49, 0.285, 0.205, 1.0)
skin.use_nodes = True
bsdf = skin.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0.49, 0.285, 0.205, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.60
    if "Subsurface Weight" in bsdf.inputs:
        bsdf.inputs["Subsurface Weight"].default_value = 0.035
body.data.materials.clear()
body.data.materials.append(skin)

# Neutral studio render setup. The same orthographic composition is used for
# the body views; the close-up differs only by its framing target and scale.
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1000
scene.render.resolution_y = 1400
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = "AgX"
scene.render.film_transparent = False
scene.render.filepath = os.path.join(OUT, "mb006-front.png")

world = bpy.data.worlds.get("MB006 neutral studio") or bpy.data.worlds.new("MB006 neutral studio")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.16, 0.18, 0.20, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.42

setup = bpy.data.collections.get("MB006 Render Setup") or bpy.data.collections.new("MB006 Render Setup")
if setup.name not in [collection.name for collection in scene.collection.children]:
    scene.collection.children.link(setup)

def add_area(name, location, power, size, target):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = power
    data.shape = "DISK"
    data.size = size
    obj = bpy.data.objects.new(name, data)
    setup.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()
    return obj

def add_camera(name, location, target, ortho_scale):
    data = bpy.data.cameras.new(name)
    data.type = "ORTHO"
    data.ortho_scale = ortho_scale
    obj = bpy.data.objects.new(name, data)
    setup.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()
    return obj

depsgraph = bpy.context.evaluated_depsgraph_get()
evaluated = body.evaluated_get(depsgraph)
evaluated_mesh = evaluated.to_mesh()
world_vertices = [evaluated.matrix_world @ vertex.co for vertex in evaluated_mesh.vertices]
bounds_min = Vector(tuple(min(point[i] for point in world_vertices) for i in range(3)))
bounds_max = Vector(tuple(max(point[i] for point in world_vertices) for i in range(3)))
evaluated.to_mesh_clear()
height = bounds_max.z - bounds_min.z
center = Vector(((bounds_min.x + bounds_max.x) * 0.5,
                 (bounds_min.y + bounds_max.y) * 0.5,
                 (bounds_min.z + bounds_max.z) * 0.5))
face_target = Vector((center.x, center.y - 0.01, bounds_min.z + height * 0.885))

for obj in list(setup.objects):
    setup.objects.unlink(obj)
    if obj.type == "CAMERA":
        bpy.data.cameras.remove(obj.data)
    elif obj.type == "LIGHT":
        bpy.data.lights.remove(obj.data)

for name, location, power, size in (
    ("MB006 key", (2.6, -3.8, center.z + 2.0), 520, 3.2),
    ("MB006 fill", (-3.0, -2.6, center.z + 0.8), 250, 3.8),
    ("MB006 rim", (1.4, 2.6, center.z + 1.8), 420, 2.8),
):
    add_area(name, location, power, size, center)

views = [
    ("front", (center.x, center.y - 4.8, center.z), center, height * 1.18),
    ("side", (center.x + 4.8, center.y, center.z), center, height * 1.18),
    ("rear", (center.x, center.y + 4.8, center.z), center, height * 1.18),
    ("three-quarter", (center.x + 3.8, center.y - 3.8, center.z), center, height * 1.18),
    ("face-closeup", (face_target.x, face_target.y - 1.7, face_target.z), face_target, height * 0.31),
    ("full-body-neutral", (center.x, center.y - 4.8, center.z), center, height * 1.18),
]

render_paths = []
for view_name, location, target, scale in views:
    camera = add_camera("MB006 Camera " + view_name, location, target, scale)
    scene.camera = camera
    filepath = os.path.join(OUT, "mb006-" + view_name + ".png")
    scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    render_paths.append(filepath)
    setup.objects.unlink(camera)
    bpy.data.cameras.remove(camera.data)

# Preserve a clean render setup in the editable master after preview rendering.
scene.camera = None
for obj in list(setup.objects):
    setup.objects.unlink(obj)
    bpy.data.lights.remove(obj.data)

blend_path = os.path.join(OUT, "mb006-child-anatomy-prototype.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

report = {
    "status": "PARTIAL — editable anatomy/face prototype; visual approval pending",
    "blender_version": bpy.app.version_string,
    "base_file": os.path.relpath(BASE, REPO).replace("\\", "/"),
    "base_license": "MPFB2 bundled core geometry and targets, CC0; see MB-004A report",
    "mesh_vertices": len(body.data.vertices),
    "mesh_edges": len(body.data.edges),
    "mesh_faces": len(body.data.polygons),
    "modifiers_preserved": [modifier.type for modifier in body.modifiers],
    "shape_key": prototype_key.name,
    "local_change_parameters": {
        "shoulder_band_width_peak": 0.075,
        "upper_chest_width_peak": 0.025,
        "waist_width_peak": -0.045,
        "pelvis_width_peak": -0.035,
        "neck_depth_peak": 0.035,
        "cheek_width_peak": 0.025,
        "lower_jaw_width_peak": -0.020,
        "finger_extension": 0.035,
        "forefoot_length_extension": 0.025,
    },
    "scene_scale_context_m": target_stature_m,
    "baseline_scene_height_m": current_stature_m,
    "armature_uniform_context_scale": stature_scale,
    "age_suitability_claim": "None; one record is used only to set scene scale, not establish age suitability.",
    "evaluated_bounds_scene_units": {
        "min": list(bounds_min),
        "max": list(bounds_max),
        "height": height,
    },
    "reference_record": {
        "source": "NIST/CPSC AnthroKids 1977, MB-004B Candidate 02",
        "age_band_months": "96–107",
        "stature_m": 1.292,
        "head_stature": 0.1440,
        "sitting_height_stature": 0.5333,
        "shoulder_breadth_stature": 0.2446,
        "shoulder_elbow_stature": 0.2051,
        "elbow_hand_stature": 0.2655,
        "hand_stature": 0.1068,
        "foot_stature": 0.1563,
        "caveat": "One record used for context only; not a medical norm or Algerian child template.",
    },
    "renders": [os.path.basename(path) for path in render_paths],
    "known_limits": [
        "No age-specific or Algerian-specific age validation.",
        "No external hair, eyes, skin texture, clothing, footwear, or flag assets were added.",
        "The face is a neutral MPFB base with only small local cheek/jaw edits; professional sculpt review is required.",
        "No local edits were made to limb lengths or joint locations; those remain unvalidated for child proportions.",
        "Existing 784 boundary edges and four-influence deformation limitation remain; this task did not repair them.",
        "The standard MPFB rest pose is an A-pose and has not been signed off as a production neutral pose.",
        "Visual and rig approval remain pending Product Owner and character-artist review.",
    ],
}
with open(os.path.join(OUT, "mb006-prototype-report.json"), "w", encoding="utf-8") as handle:
    json.dump(report, handle, ensure_ascii=False, indent=2)
print("MB006_RESULT", json.dumps(report, ensure_ascii=False))
print("MB006_BLEND", blend_path, os.path.getsize(blend_path))
