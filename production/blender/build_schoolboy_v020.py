"""Build MotionBoard's original canonical schoolboy character in Blender.

This creates a static, editable and rigged prototype. It deliberately does not
author educational animation clips. Run with Blender 5.2 LTS or compatible:
  blender --background --python production/blender/build_schoolboy.py
Optional output root: -- --output-root D:/path/to/MotionBoard
"""

from __future__ import annotations

import json
import math
import os
import struct
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def output_root_from_args() -> Path:
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if "--output-root" in args:
        return Path(args[args.index("--output-root") + 1]).resolve()
    # Script is stored at <repo>/production/blender/build_schoolboy.py.
    return Path(__file__).resolve().parents[2]


def skip_previews_from_args() -> bool:
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return "--skip-previews" in args


ROOT = output_root_from_args()
BLENDER_DIR = ROOT / "production" / "blender"
CHAR_DIR = ROOT / "assets" / "characters"
PREVIEW_DIR = ROOT / "assets" / "previews" / "v0.2.0"
for folder in (BLENDER_DIR, CHAR_DIR, PREVIEW_DIR):
    folder.mkdir(parents=True, exist_ok=True)

BLEND_PATH = BLENDER_DIR / "schoolboy-v0.2.0.blend"
GLB_PATH = CHAR_DIR / "schoolboy-v0.2.0.glb"
REPORT_PATH = BLENDER_DIR / "schoolboy-v020-build-report.json"


def deselect_all():
    bpy.ops.object.select_all(action="DESELECT")


def activate(obj):
    deselect_all()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def material(name, color, roughness=0.72, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat


SKIN = material("Skin • warm peach", (0.72, 0.39, 0.24), 0.74)
SHIRT = material("Uniform • soft white", (0.91, 0.94, 0.91), 0.78)
GREEN = material("Uniform • Algeria green", (0.02, 0.34, 0.20), 0.68)
RED = material("Uniform • Algeria red", (0.76, 0.055, 0.075), 0.67)
SHORTS = material("Uniform • white shorts", (0.86, 0.90, 0.87), 0.8)
HAIR = material("Hair • dark chestnut", (0.105, 0.045, 0.025), 0.83)
EYE_WHITE = material("Eyes • warm white", (0.96, 0.97, 0.91), 0.36)
IRIS = material("Eyes • hazel", (0.24, 0.105, 0.035), 0.4)
PUPIL = material("Eyes • pupil", (0.018, 0.012, 0.009), 0.28)
HIGHLIGHT = material("Eyes • glint", (1.0, 0.99, 0.92), 0.2)
SHOE = material("Shoes • white leather", (0.91, 0.93, 0.91), 0.52)
SOLE = material("Shoes • green sole", (0.10, 0.29, 0.22), 0.72)
LACE = material("Shoes • laces", (0.98, 0.97, 0.88), 0.58)
GROUND = material("Preview • warm neutral floor", (0.66, 0.73, 0.68), 0.91)


def add_ellipsoid(name, location, scale, mat=None, segments=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=rings, radius=1.0, location=location
    )
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj


def add_capsule_piece(name, start, end, radius_x, radius_y=None, mat=None):
    a, b = Vector(start), Vector(end)
    axis = b - a
    obj = add_ellipsoid(
        name,
        (a + b) * 0.5,
        (radius_x, radius_y if radius_y is not None else radius_x, axis.length * 0.5 + radius_x),
        mat,
        segments=20,
        rings=14,
    )
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(axis.normalized())
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    return obj


def create_mesh(name, vertices, faces, mat):
    mesh = bpy.data.meshes.new(name + " • mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.materials.append(mat)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    for poly in mesh.polygons:
        poly.use_smooth = True
    return obj


def join_meshes(objects, name):
    activate(objects[0])
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = name
    return obj


def capsule_surface(name, start, end, radius_start, radius_end, mat, sides=20):
    """A tapered, rounded-looking garment sleeve around a limb axis."""
    a, b = Vector(start), Vector(end)
    axis = (b - a).normalized()
    guide = Vector((0, 1, 0)) if abs(axis.dot(Vector((0, 1, 0)))) < 0.9 else Vector((1, 0, 0))
    u = axis.cross(guide).normalized()
    v = axis.cross(u).normalized()
    verts, faces = [], []
    for t, radius in ((0.0, radius_start * 0.72), (0.13, radius_start), (0.82, radius_end), (1.0, radius_end * 0.72)):
        center = a.lerp(b, t)
        for i in range(sides):
            angle = 2 * math.pi * i / sides
            point = center + u * (math.cos(angle) * radius) + v * (math.sin(angle) * radius * 0.84)
            verts.append(tuple(point))
    for ring in range(3):
        for i in range(sides):
            j = (i + 1) % sides
            faces.append((ring * sides + i, ring * sides + j, (ring + 1) * sides + j, (ring + 1) * sides + i))
    faces.extend([tuple(range(sides - 1, -1, -1)), tuple(range(3 * sides, 4 * sides))])
    return create_mesh(name, verts, faces, mat)


def torso_shell(name, profile, mat, sides=40):
    verts, faces = [], []
    for z, rx, ry, center_y in profile:
        for i in range(sides):
            angle = 2 * math.pi * i / sides
            verts.append((rx * math.cos(angle), center_y + ry * math.sin(angle), z))
    for ring in range(len(profile) - 1):
        for i in range(sides):
            j = (i + 1) % sides
            faces.append((ring * sides + i, ring * sides + j, (ring + 1) * sides + j, (ring + 1) * sides + i))
    faces.extend([tuple(range(sides - 1, -1, -1)), tuple((len(profile) - 1) * sides + i for i in range(sides))])
    obj = create_mesh(name, verts, faces, mat)
    solid = obj.modifiers.new("Fabric thickness", "SOLIDIFY")
    solid.thickness = 0.012
    solid.offset = 0.0
    bevel = obj.modifiers.new("Soft cloth edges", "BEVEL")
    bevel.width = 0.009
    bevel.segments = 2
    return obj


def curve_line(name, points, bevel, mat, cyclic=False):
    curve = bpy.data.curves.new(name + " • curve", "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 12
    curve.bevel_depth = bevel
    curve.bevel_resolution = 3
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for p, co in zip(spline.points, points):
        p.co = (*co, 1.0)
    spline.use_cyclic_u = cyclic
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def flat_polygon(name, points_xz, y, mat):
    verts = [(x, y, z) for x, z in points_xz]
    faces = [tuple(range(len(verts)))]
    return create_mesh(name, verts, faces, mat)


def make_star(name, center_x, center_z, radius, y, mat):
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * 0.44
        points.append((center_x + math.cos(angle) * r, center_z + math.sin(angle) * r))
    return flat_polygon(name, points, y, mat)


def create_flag():
    """Flat, raised fabric badge, with screen-left hoist green and correct emblem."""
    cx, cz, w, h, y = 0.0, 0.935, 0.144, 0.088, 0.159
    base = flat_polygon(
        "Algerian flag • white field",
        [(cx - w / 2, cz - h / 2), (cx + w / 2, cz - h / 2), (cx + w / 2, cz + h / 2), (cx - w / 2, cz + h / 2)],
        y,
        SHIRT,
    )
    base.data.materials.append(GREEN)
    # Front view is from +Y: +X appears at viewer-left, the hoist side.
    x0, x1 = cx, cx + w / 2
    green_mesh = flat_polygon("Algerian flag • green hoist", [(x0, cz - h / 2), (x1, cz - h / 2), (x1, cz + h / 2), (x0, cz + h / 2)], y + 0.0015, GREEN)
    # A crescent made as one filled concave polygon; its tips open toward fly side.
    radius_outer, radius_inner = 0.029, 0.024
    crescent = []
    for deg in range(-112, 113, 8):
        a = math.radians(deg)
        crescent.append((cx + radius_outer * math.cos(a), cz + radius_outer * math.sin(a)))
    for deg in range(112, -113, -8):
        a = math.radians(deg)
        crescent.append((cx - 0.014 + radius_inner * math.cos(a), cz + radius_inner * math.sin(a)))
    red_crescent = flat_polygon("Algerian flag • red crescent", crescent, y + 0.003, RED)
    star = make_star("Algerian flag • five-point star", cx - 0.030, cz, 0.014, y + 0.004, RED)
    return [base, green_mesh, red_crescent, star]


def create_armature():
    arm_data = bpy.data.armatures.new("MotionBoard humanoid • v0.2")
    arm = bpy.data.objects.new("MotionBoard Schoolboy Rig • v0.2", arm_data)
    bpy.context.collection.objects.link(arm)
    activate(arm)
    bpy.ops.object.mode_set(mode="EDIT")
    bones = {}

    def bone(name, head, tail, parent=None, connected=False):
        b = arm_data.edit_bones.new(name)
        b.head, b.tail = head, tail
        if parent:
            b.parent = bones[parent]
            b.use_connect = connected
        bones[name] = b

    bone("root", (0, 0, 0.0), (0, 0, 0.12))
    bone("pelvis", (0, 0, 0.49), (0, 0, 0.65), "root")
    bone("spine", (0, 0, 0.65), (0, 0, 0.85), "pelvis", True)
    bone("chest", (0, 0, 0.85), (0, 0, 1.025), "spine", True)
    bone("neck", (0, 0, 1.025), (0, 0, 1.12), "chest", True)
    bone("head", (0, 0, 1.12), (0, 0, 1.37), "neck", True)
    for side, sign in (("L", 1), ("R", -1)):
        bone(f"clavicle.{side}", (0.12 * sign, 0, 1.01), (0.245 * sign, 0, 1.015), "chest")
        bone(f"upper_arm.{side}", (0.245 * sign, 0, 1.015), (0.355 * sign, 0, 0.81), f"clavicle.{side}", True)
        bone(f"forearm.{side}", (0.355 * sign, 0, 0.81), (0.345 * sign, 0.015, 0.60), f"upper_arm.{side}", True)
        bone(f"hand.{side}", (0.345 * sign, 0.015, 0.60), (0.345 * sign, 0.055, 0.515), f"forearm.{side}", True)
        # Finger bones extend the stable v0.1 arm/leg contract without renaming it.
        # Four fingers are 3-segment chains; thumbs are 2-segment opposed chains.
        for digit, offset in (("index", -0.045), ("middle", -0.015), ("ring", 0.015), ("pinky", 0.045)):
            start = (0.345 * sign + offset, 0.055, 0.515)
            for segment, (dz, dx) in enumerate(((0.035, 0.002), (0.029, 0.002), (0.023, 0.001)), start=1):
                end = (start[0] + dx * sign, start[1] + 0.006, start[2] - dz)
                name = f"{digit}.{segment:02d}.{side}"
                bone(name, start, end, f"hand.{side}" if segment == 1 else f"{digit}.{segment-1:02d}.{side}", segment > 1)
                start = end
        thumb_start = (0.29 * sign, 0.045, 0.555)
        for segment, (dx, dz) in enumerate(((0.035, 0.026), (0.029, 0.022)), start=1):
            thumb_end = (thumb_start[0] - dx * sign, thumb_start[1] + 0.009, thumb_start[2] - dz)
            name = f"thumb.{segment:02d}.{side}"
            bone(name, thumb_start, thumb_end, f"hand.{side}" if segment == 1 else f"thumb.{segment-1:02d}.{side}", segment > 1)
            thumb_start = thumb_end
        bone(f"thigh.{side}", (0.105 * sign, 0, 0.59), (0.105 * sign, 0, 0.32), "pelvis")
        bone(f"shin.{side}", (0.105 * sign, 0, 0.32), (0.105 * sign, 0, 0.105), f"thigh.{side}", True)
        bone(f"foot.{side}", (0.105 * sign, 0, 0.105), (0.105 * sign, 0.16, 0.055), f"shin.{side}", True)
    bpy.ops.object.mode_set(mode="OBJECT")
    arm.show_in_front = True
    arm.data.display_type = "OCTAHEDRAL"
    return arm


def point_segment_distance(point, start, end):
    ab = end - start
    denominator = ab.length_squared
    if denominator < 1e-10:
        return (point - start).length
    t = max(0.0, min(1.0, (point - start).dot(ab) / denominator))
    return (point - (start + t * ab)).length


def bones_for_weights(arm):
    result = []
    for bone in arm.data.bones:
        if bone.name == "root":
            continue
        result.append((bone.name, bone.head_local.copy(), bone.tail_local.copy()))
    return result


def only_bones(arm, names):
    available = {name: (name, head, tail) for name, head, tail in bones_for_weights(arm)}
    return [available[name] for name in names]


def skin_mesh(obj, arm, segments=None, max_influences=4):
    if obj.type != "MESH":
        return
    segments = segments or bones_for_weights(arm)
    groups = {name: obj.vertex_groups.new(name=name) for name, _, _ in segments}
    arm_from_world = arm.matrix_world.inverted()
    for vertex in obj.data.vertices:
        # Blender joined/remeshed meshes can keep a non-zero object origin.
        # Evaluate weights in the armature's local coordinates, not raw mesh
        # coordinates, or the bind pose looks fine while articulation collapses.
        point = arm_from_world @ obj.matrix_world @ vertex.co
        distances = [(point_segment_distance(point, head, tail), name) for name, head, tail in segments]
        distances.sort(key=lambda item: item[0])
        chosen = distances[:max_influences]
        minimum = chosen[0][0]
        values = [(math.exp(-((distance - minimum) / 0.075)), name) for distance, name in chosen]
        total = sum(value for value, _ in values)
        for value, name in values:
            weight = value / total
            if weight > 0.025:
                groups[name].add([vertex.index], weight, "REPLACE")
    modifier = obj.modifiers.new("Canonical humanoid skin", "ARMATURE")
    modifier.object = arm
    modifier.use_deform_preserve_volume = True
    obj.parent = arm
    obj.matrix_parent_inverse = arm.matrix_world.inverted()


def skin_fused_body(obj, arm):
    """Region-aware weights keep the fused torso from following an arm or leg."""
    names = [b.name for b in arm.data.bones if b.name != "root"]
    groups = {name: obj.vertex_groups.new(name=name) for name in names}
    arm_from_world = arm.matrix_world.inverted()
    for vertex in obj.data.vertices:
        p = arm_from_world @ obj.matrix_world @ vertex.co
        x, z = p.x, p.z
        ax = abs(x)
        side = "L" if x >= 0 else "R"

        # Vertical torso chain (pelvis -> spine -> chest -> neck -> head).
        if z >= 1.155:
            weights = {"head": 1.0}
        elif z >= 1.035:
            t = max(0.0, min(1.0, (z - 1.035) / 0.12))
            weights = {"chest": 1.0 - t, "neck": t}
        elif z >= 0.86:
            t = max(0.0, min(1.0, (z - 0.86) / 0.175))
            weights = {"spine": 1.0 - t, "chest": t}
        elif z >= 0.63:
            t = max(0.0, min(1.0, (z - 0.63) / 0.23))
            weights = {"pelvis": 1.0 - t, "spine": t}
        else:
            weights = {"pelvis": 1.0}

        # Arms are tested before legs because hands overlap the shorts' height.
        # Shoulder vertices blend into chest; distal arm vertices use only their
        # own arm chain and must never inherit thigh/shin weights.
        arm_region = 0.43 < z < 1.11 and ax > 0.205
        if arm_region:
            lateral = max(0.0, min(1.0, (ax - 0.205) / 0.095))
            if z >= 0.94:
                arm_weights = {f"clavicle.{side}": 0.22, f"upper_arm.{side}": 0.78}
            elif z >= 0.80:
                t = max(0.0, min(1.0, (z - 0.80) / 0.14))
                arm_weights = {f"forearm.{side}": 1.0 - t, f"upper_arm.{side}": t}
            elif z >= 0.60:
                t = max(0.0, min(1.0, (z - 0.60) / 0.20))
                arm_weights = {f"forearm.{side}": 1.0 - t, f"upper_arm.{side}": t}
            else:
                arm_weights = {f"hand.{side}": 0.65, f"forearm.{side}": 0.35}
            weights = {key: value * (1.0 - lateral) for key, value in weights.items()}
            for key, value in arm_weights.items():
                weights[key] = weights.get(key, 0.0) + value * lateral

        # Legs own lower-body vertices not classified as an arm/hand.
        elif z < 0.66 and ax > 0.055:
            lateral = max(0.0, min(1.0, (ax - 0.045) / 0.075))
            if z >= 0.34:
                leg_weights = {f"thigh.{side}": 1.0}
            elif z >= 0.16:
                t = max(0.0, min(1.0, (z - 0.16) / 0.18))
                leg_weights = {f"shin.{side}": 1.0 - t, f"thigh.{side}": t}
            else:
                # The whole foot volume stays with the shoe/foot bone so ankle
                # flexion cannot pull a skin patch through the footwear.
                leg_weights = {f"foot.{side}": 1.0}
            weights = {key: value * (1.0 - lateral) for key, value in weights.items()}
            for key, value in leg_weights.items():
                weights[key] = weights.get(key, 0.0) + value * lateral

        total = sum(weights.values())
        for name, weight in weights.items():
            if weight > 0.015:
                groups[name].add([vertex.index], weight / total, "REPLACE")
    modifier = obj.modifiers.new("Canonical humanoid skin", "ARMATURE")
    modifier.object = arm
    modifier.use_deform_preserve_volume = True
    obj.parent = arm
    obj.matrix_parent_inverse = arm.matrix_world.inverted()


def skin_to_single_bone(obj, arm, bone_name):
    if obj.type == "CURVE":
        activate(obj)
        bpy.ops.object.convert(target="MESH")
        obj = bpy.context.object
    vg = obj.vertex_groups.new(name=bone_name)
    if obj.type == "MESH":
        vg.add([v.index for v in obj.data.vertices], 1.0, "REPLACE")
        modifier = obj.modifiers.new("Canonical humanoid skin", "ARMATURE")
        modifier.object = arm
        modifier.use_deform_preserve_volume = True
        obj.parent = arm
        obj.matrix_parent_inverse = arm.matrix_world.inverted()


def create_body(arm):
    parts = []
    # Soft continuous base anatomy. Voxel remeshing fuses adjoining forms into
    # one sculpt-like body instead of leaving a collection of visible primitives.
    parts.append(add_ellipsoid("body_core", (0, 0, 0.81), (0.205, 0.126, 0.29), SKIN, 40, 28))
    parts.append(add_ellipsoid("pelvis_core", (0, 0, 0.60), (0.190, 0.126, 0.18), SKIN, 40, 28))
    parts.append(add_ellipsoid("neck_core", (0, 0, 1.065), (0.085, 0.085, 0.13), SKIN))
    parts.append(add_ellipsoid("head_core", (0, 0, 1.235), (0.166, 0.157, 0.195), SKIN, 32, 24))
    for side, sign in (("L", 1), ("R", -1)):
        parts.append(add_ellipsoid(f"ear_{side}", (0.158 * sign, 0.002, 1.23), (0.030, 0.040, 0.047), SKIN))
        # Limb segment volumes are fused into the main body surface.
        parts.append(add_capsule_piece(f"upper_arm_{side}", (0.24 * sign, 0, 1.01), (0.355 * sign, 0, 0.81), 0.073, 0.073, SKIN))
        parts.append(add_capsule_piece(f"forearm_{side}", (0.355 * sign, 0, 0.81), (0.345 * sign, 0.015, 0.60), 0.060, 0.060, SKIN))
        parts.append(add_ellipsoid(f"palm_{side}", (0.345 * sign, 0.04, 0.545), (0.064, 0.042, 0.073), SKIN))
        parts.append(add_ellipsoid(f"thigh_{side}", (0.105 * sign, 0, 0.46), (0.097, 0.091, 0.19), SKIN))
        parts.append(add_capsule_piece(f"shin_{side}", (0.105 * sign, 0, 0.35), (0.105 * sign, 0, 0.105), 0.068, 0.071, SKIN))
        parts.append(add_ellipsoid(f"foot_base_{side}", (0.105 * sign, 0.045, 0.09), (0.076, 0.13, 0.062), SKIN))
    body = join_meshes(parts, "Schoolboy • fused body")
    remesh = body.modifiers.new("Fuse anatomy into continuous surface", "REMESH")
    remesh.mode = "VOXEL"
    remesh.voxel_size = 0.008
    remesh.use_smooth_shade = True
    activate(body)
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    smooth = body.modifiers.new("Gentle sculpt polish", "SMOOTH")
    smooth.factor = 0.35
    smooth.iterations = 3
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    for p in body.data.polygons:
        p.use_smooth = True
    skin_fused_body(body, arm)
    # Individually weighted, rounded finger segments preserve articulation while
    # overlapping slightly at joints to avoid gaps in neutral and curled poses.
    digit_objects = []
    for side, sign in (("L", 1), ("R", -1)):
        for digit, offset in (("index", -0.045), ("middle", -0.015), ("ring", 0.015), ("pinky", 0.045)):
            start = (0.345 * sign + offset, 0.055, 0.515)
            for segment, (dz, dx, radius) in enumerate(((0.035, 0.002, 0.011), (0.029, 0.002, 0.0095), (0.023, 0.001, 0.008)), start=1):
                end = (start[0] + dx * sign, start[1] + 0.006, start[2] - dz)
                part = add_capsule_piece(f"Finger {digit} {segment} • {side}", start, end, radius, radius, SKIN,)
                skin_to_single_bone(part, arm, f"{digit}.{segment:02d}.{side}")
                digit_objects.append(part)
                start = end
        start = (0.29 * sign, 0.045, 0.555)
        for segment, (dx, dz, radius) in enumerate(((0.035, 0.026, 0.014), (0.029, 0.022, 0.011)), start=1):
            end = (start[0] - dx * sign, start[1] + 0.009, start[2] - dz)
            part = add_capsule_piece(f"Finger thumb {segment} • {side}", start, end, radius, radius, SKIN)
            skin_to_single_bone(part, arm, f"thumb.{segment:02d}.{side}")
            digit_objects.append(part)
            start = end
    return [body, *digit_objects]


def create_shirt(arm):
    profile = [
        (1.115, 0.158, 0.101, 0),
        (1.092, 0.192, 0.120, 0),
        (1.045, 0.242, 0.136, 0),
        (0.975, 0.250, 0.143, 0),
        (0.865, 0.236, 0.136, 0),
        (0.755, 0.212, 0.123, 0),
        (0.674, 0.198, 0.112, 0),
    ]
    shirt = torso_shell("School PE shirt • white", profile, SHIRT)
    torso_weights = only_bones(arm, ["pelvis", "spine", "chest", "neck"])
    skin_mesh(shirt, arm, torso_weights, max_influences=2)
    objects = [shirt]
    # Short fitted sleeves terminate above the elbows; exposed forearms remain clear.
    for side, sign in (("L", 1), ("R", -1)):
        sleeve = capsule_surface(
            f"Shirt sleeve • {side}",
            (0.218 * sign, 0, 1.034),
            (0.315 * sign, 0, 0.92),
            0.102,
            0.088,
            SHIRT,
        )
        sleeve_weights = only_bones(arm, [f"clavicle.{side}", f"upper_arm.{side}"])
        skin_mesh(sleeve, arm, sleeve_weights, max_influences=2)
        objects.append(sleeve)
        # Two slim color accents on the sleeve edge, outside of the flag badge.
        cuff = curve_line(
            f"Sleeve green cuff • {side}",
            [(0.28 * sign, 0.064, 0.928), (0.305 * sign, 0.063, 0.915), (0.33 * sign, 0.05, 0.902)],
            0.006,
            GREEN,
        )
        skin_to_single_bone(cuff, arm, f"upper_arm.{side}")
        objects.append(cuff)
    # A narrow green collar and hem piping provide restrained national colors.
    collar_pts = [(0.116 * math.cos(2 * math.pi * i / 48), 0.115 * math.sin(2 * math.pi * i / 48), 1.105) for i in range(48)]
    collar = curve_line("Shirt • green collar piping", collar_pts, 0.009, GREEN, cyclic=True)
    skin_to_single_bone(collar, arm, "chest")
    objects.append(collar)
    hem_pts = [(0.204 * math.cos(2 * math.pi * i / 64), 0.116 * math.sin(2 * math.pi * i / 64), 0.678) for i in range(64)]
    hem = curve_line("Shirt • green hem piping", hem_pts, 0.006, GREEN, cyclic=True)
    skin_to_single_bone(hem, arm, "spine")
    objects.append(hem)
    flag = create_flag()
    for obj in flag:
        skin_to_single_bone(obj, arm, "chest")
    objects.extend(flag)
    # Fine red side accents, placed on the flank to avoid competing with the flag.
    for side, sign in (("L", 1), ("R", -1)):
        accent = curve_line(
            f"Shirt • red side accent {side}",
            [(0.255 * sign, 0.012, 0.985), (0.26 * sign, 0.014, 0.90), (0.235 * sign, 0.012, 0.79)],
            0.004,
            RED,
        )
        skin_to_single_bone(accent, arm, "chest")
        objects.append(accent)
    return objects


def create_shorts(arm):
    # The overlap is deliberately generous at pelvis and crotch: voxel union
    # produces one continuous garment shell with no triangular openings.
    pieces = [add_ellipsoid("Shorts • continuous waist and seat", (0, 0, 0.602), (0.224, 0.146, 0.142), SHORTS, 40, 28)]
    for side, sign in (("L", 1), ("R", -1)):
        pieces.append(add_ellipsoid(f"Shorts • leg {side}", (0.105 * sign, 0.005, 0.478), (0.119, 0.140, 0.146), SHORTS, 36, 24))
    shorts = join_meshes(pieces, "School PE shorts • white")
    remesh = shorts.modifiers.new("Smooth joined shorts shape", "REMESH")
    remesh.mode = "VOXEL"
    remesh.voxel_size = 0.006
    remesh.use_smooth_shade = True
    activate(shorts)
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    smooth = shorts.modifiers.new("Soft cloth surface", "SMOOTH")
    smooth.factor = 0.25
    smooth.iterations = 2
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    for p in shorts.data.polygons:
        p.use_smooth = True
    shorts_weights = only_bones(arm, ["pelvis", "thigh.L", "thigh.R"])
    skin_mesh(shorts, arm, shorts_weights, max_influences=2)
    result = [shorts]
    waistband = curve_line(
        "Shorts • green waistband stripe",
        [(0.218 * math.cos(2 * math.pi * i / 64), 0.139 * math.sin(2 * math.pi * i / 64), 0.682) for i in range(64)],
        0.012,
        GREEN,
        cyclic=True,
    )
    skin_to_single_bone(waistband, arm, "pelvis")
    result.append(waistband)
    for side, sign in (("L", 1), ("R", -1)):
        piping = curve_line(
            f"Shorts • red piping {side}",
            [(0.20 * sign, 0.062, 0.66), (0.22 * sign, 0.089, 0.56), (0.215 * sign, 0.09, 0.43)],
            0.0045,
            RED,
        )
        skin_to_single_bone(piping, arm, f"thigh.{side}")
        result.append(piping)
    return result


def create_face_and_hair(arm):
    objs = []
    for side, sign in (("L", 1), ("R", -1)):
        x = 0.063 * sign
        # Layered eyes with irises and small highlights, all on the forward (+Y) face.
        parts = [
            add_ellipsoid(f"Eye white {side}", (x, 0.145, 1.274), (0.032, 0.015, 0.039), EYE_WHITE, 28, 20),
            add_ellipsoid(f"Hazel iris {side}", (x - 0.005 * sign, 0.159, 1.274), (0.015, 0.008, 0.020), IRIS, 24, 16),
            add_ellipsoid(f"Pupil {side}", (x - 0.006 * sign, 0.166, 1.274), (0.008, 0.005, 0.013), PUPIL, 20, 12),
            add_ellipsoid(f"Eye glint {side}", (x - 0.012 * sign, 0.181, 1.286), (0.006, 0.004, 0.008), HIGHLIGHT, 12, 8),
        ]
        objs.extend(parts)
        for part in parts:
            skin_to_single_bone(part, arm, "head")
        brow = curve_line(
            f"Soft brow {side}",
            [(x - 0.035, 0.158, 1.33), (x, 0.171, 1.343), (x + 0.034, 0.158, 1.335)],
            0.0065,
            HAIR,
        )
        skin_to_single_bone(brow, arm, "head")
        objs.append(brow)
    nose = add_ellipsoid("Small soft nose", (0, 0.163, 1.218), (0.025, 0.024, 0.028), SKIN, 20, 14)
    skin_to_single_bone(nose, arm, "head")
    objs.append(nose)
    smile_pts = [(-0.042, 0.151, 1.174), (-0.024, 0.166, 1.161), (0, 0.169, 1.158), (0.024, 0.166, 1.161), (0.042, 0.151, 1.174)]
    smile = curve_line("Friendly curved smile", smile_pts, 0.0037, HAIR)
    skin_to_single_bone(smile, arm, "head")
    objs.append(smile)
    # A sculpt-like hair cap with a gently irregular front fringe.
    # A cap plus three swept low-relief locks creates a less spherical silhouette.
    hair = add_ellipsoid("Hair • shaped short cap", (0, -0.006, 1.365), (0.166, 0.151, 0.074), HAIR, 40, 28)
    skin_to_single_bone(hair, arm, "head")
    objs.append(hair)
    for i, (x, z, w) in enumerate(((-0.085, 1.324, 0.052), (-0.025, 1.316, 0.060), (0.045, 1.322, 0.055), (0.100, 1.331, 0.035))):
        lock = add_capsule_piece(f"Hair • swept fringe lock {i+1}", (x, 0.094, z + 0.024), (x + 0.016, 0.133, z - 0.012), w * 0.43, w * 0.43, HAIR,)
        skin_to_single_bone(lock, arm, "head")
        objs.append(lock)
    return objs


def create_shoes(arm):
    result = []
    for side, sign in (("L", 1), ("R", -1)):
        # Rounded-box sole and distinct toe box / heel volume read as a trainer.
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.105 * sign, 0.050, 0.039))
        sole = bpy.context.object
        sole.name = f"Trainer • sculpted sole • {side}"
        sole.dimensions = (0.165, 0.305, 0.055)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        sole_bevel = sole.modifiers.new("Rounded athletic sole", "BEVEL")
        sole_bevel.width = 0.025
        sole_bevel.segments = 5
        sole.modifiers.new("Weighted sole normals", "WEIGHTED_NORMAL")
        sole.data.materials.append(SOLE)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.105 * sign, 0.060, 0.112))
        upper = bpy.context.object
        upper.name = f"Trainer • anatomical upper • {side}"
        upper.dimensions = (0.143, 0.260, 0.105)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        upper_bevel = upper.modifiers.new("Soft toe and heel shaping", "BEVEL")
        upper_bevel.width = 0.045
        upper_bevel.segments = 6
        upper.modifiers.new("Weighted upper normals", "WEIGHTED_NORMAL")
        skin_to_single_bone(sole, arm, f"foot.{side}")
        skin_to_single_bone(upper, arm, f"foot.{side}")
        result.extend([sole, upper])
        accent = curve_line(
            f"Trainer red side stitch • {side}",
            [(0.165 * sign, 0.082, 0.11), (0.174 * sign, 0.03, 0.12), (0.16 * sign, -0.018, 0.12)],
            0.005,
            RED,
        )
        skin_to_single_bone(accent, arm, f"foot.{side}")
        result.append(accent)
        for lace_index in range(3):
            y = 0.025 + lace_index * 0.032
            lace = curve_line(
                f"Trainer lace {lace_index+1} • {side}",
                [(0.105 * sign - 0.028, y, 0.158), (0.105 * sign, y + 0.009, 0.165), (0.105 * sign + 0.028, y, 0.158)],
                0.0032,
                LACE,
            )
            skin_to_single_bone(lace, arm, f"foot.{side}")
            result.append(lace)
    return result


def create_character():
    arm = create_armature()
    objs = [arm]
    objs.extend(create_body(arm))
    objs.extend(create_shirt(arm))
    objs.extend(create_shorts(arm))
    objs.extend(create_face_and_hair(arm))
    objs.extend(create_shoes(arm))
    arm["asset_id"] = "schoolboy-primary"
    arm["asset_version"] = "0.2.0"
    arm["rig_version"] = "motionboard-humanoid-v0.2"
    arm["status"] = "draft-visual-review-pending"
    arm["forward_axis"] = "+Y"
    arm["up_axis"] = "+Z"
    arm["production_note"] = "Original Blender procedural prototype; no external meshes, textures, or animation clips."
    for obj in objs:
        if obj != arm:
            obj["asset_id"] = "schoolboy-primary"
    return arm, objs


def create_preview_stage():
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.008))
    floor = bpy.context.object
    floor.name = "Preview only • neutral ground"
    floor.data.materials.append(GROUND)
    floor["exclude_from_glb"] = True
    return floor


def create_camera(name, location, target, ortho=1.88):
    data = bpy.data.cameras.new(name)
    camera = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(camera)
    camera.location = location
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()
    data.type = "ORTHO"
    data.ortho_scale = ortho
    bpy.context.scene.camera = camera
    return camera


def create_studio():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 48
    scene.render.resolution_x = 1100
    scene.render.resolution_y = 1100
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.resolution_percentage = 80
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.world.color = (0.62, 0.69, 0.65)
    world = scene.world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.64, 0.70, 0.67, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.55
    lamps = [
        ("Key softbox", (3.2, 4.0, 5.0), 520, 3.5, (1.0, 0.88, 0.74)),
        ("Fill softbox", (-3.0, 2.0, 2.8), 290, 3.0, (0.72, 0.86, 1.0)),
        ("Rim softbox", (-2.5, -2.4, 3.6), 430, 2.6, (0.76, 1.0, 0.88)),
    ]
    for name, location, power, size, color in lamps:
        data = bpy.data.lights.new(name, "AREA")
        data.energy = power
        data.shape = "DISK"
        data.size = size
        data.color = color
        obj = bpy.data.objects.new(name, data)
        bpy.context.collection.objects.link(obj)
        obj.location = location
        obj.rotation_euler = (Vector((0, 0, 0.75)) - obj.location).to_track_quat("-Z", "Y").to_euler()
        obj["exclude_from_glb"] = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(PREVIEW_DIR / "schoolboy-front.png")
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.resolution_percentage = 80
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 80
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 32
    scene.render.resolution_percentage = 75
    scene.render.resolution_x = 1100
    scene.render.resolution_y = 1100
    scene.world.color = (0.65, 0.70, 0.67)
    return scene


def render_preview(name, location, target, ortho=1.78, pose=None):
    scene = bpy.context.scene
    arm = bpy.data.objects.get("MotionBoard Schoolboy Rig • v0.2")
    if pose:
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode="POSE")
        for bone_name, rotation in pose.items():
            pb = arm.pose.bones.get(bone_name)
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = rotation
        bpy.ops.object.mode_set(mode="OBJECT")
    camera = create_camera("Preview camera • " + name, location, target, ortho)
    scene.render.filepath = str(PREVIEW_DIR / f"schoolboy-{name}.png")
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(camera, do_unlink=True)
    # Reset test pose after the rig-articulation still.
    if pose:
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode="POSE")
        for pb in arm.pose.bones:
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = (0, 0, 0)
        bpy.ops.object.mode_set(mode="OBJECT")


def export_glb(arm, objs):
    deselect_all()
    arm.select_set(True)
    for obj in objs:
        if obj != arm and obj.type in {"MESH", "CURVE"}:
            obj.select_set(True)
    bpy.context.view_layer.objects.active = arm
    # Blender's +Y authored front maps away from the viewer's default +Z
    # camera after the required Z-up -> Y-up glTF conversion. A root-only yaw
    # compensates for the viewer convention; the editable .blend stays +Y.
    original_rotation = arm.rotation_euler.copy()
    arm.rotation_mode = "XYZ"
    arm.rotation_euler.z += math.pi
    bpy.context.view_layer.update()
    try:
        bpy.ops.export_scene.gltf(
            filepath=str(GLB_PATH),
            export_format="GLB",
            use_selection=True,
            export_apply=True,
            export_animations=False,
            export_skins=True,
            export_yup=True,
            export_cameras=False,
            export_lights=False,
        )
    finally:
        arm.rotation_euler = original_rotation
        bpy.context.view_layer.update()


def validate_glb():
    raw = GLB_PATH.read_bytes()
    magic, version, declared_length = struct.unpack_from("<4sII", raw, 0)
    assert magic == b"glTF" and version == 2 and declared_length == len(raw), "Invalid GLB header/length"
    chunk_length, chunk_type = struct.unpack_from("<II", raw, 12)
    assert chunk_type == 0x4E4F534A, "GLB JSON chunk missing"
    gltf = json.loads(raw[20 : 20 + chunk_length].decode("utf-8"))
    assert gltf.get("asset", {}).get("version") == "2.0", "Not a glTF 2.0 export"
    assert gltf.get("skins"), "Export has no humanoid skin"
    assert len(gltf.get("meshes", [])) > 0, "Export has no mesh data"
    assert len(gltf.get("animations", [])) == 0, "Prototype must not contain motion clips"
    return {
        "glb_bytes": len(raw),
        "mesh_count": len(gltf.get("meshes", [])),
        "node_count": len(gltf.get("nodes", [])),
        "skin_count": len(gltf.get("skins", [])),
        "animation_count": len(gltf.get("animations", [])),
        "joint_count": len(gltf["skins"][0].get("joints", [])),
        "materials": [m.get("name", "") for m in gltf.get("materials", [])],
        "accessor_count": len(gltf.get("accessors", [])),
    }


def main():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for data in bpy.data.meshes:
        if data.users == 0:
            bpy.data.meshes.remove(data)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    arm, objs = create_character()
    floor = None
    if not skip_previews_from_args():
        floor = create_preview_stage()
        create_studio()
        # Mandatory real Blender renders from consistent studio lighting.
        render_preview("front", (0.0, 3.0, 0.88), (0, 0, 0.74), 1.72)
        render_preview("side", (3.0, 0.0, 0.88), (0, 0, 0.74), 1.72)
        render_preview("rear", (0.0, -3.0, 0.88), (0, 0, 0.74), 1.72)
        render_preview("three-quarter", (2.25, 2.65, 1.65), (0, 0, 0.75), 1.85)
        render_preview("face-closeup", (0.05, 1.45, 1.31), (0, 0, 1.30), 0.52)
        render_preview("hand-closeup", (0.58, 0.92, 0.54), (0.345, 0.05, 0.51), 0.38)
        render_preview("shoe-closeup", (0.20, 0.92, 0.18), (0.105, 0.05, 0.095), 0.42)
        render_preview("shorts-front-gap-check", (0, 2.1, 0.55), (0, 0, 0.54), 0.57)
        render_preview("shorts-rear-gap-check", (0, -2.1, 0.55), (0, 0, 0.54), 0.57)
        test_pose = {
            "upper_arm.L": (0.0, 0.0, -0.35),
            "forearm.L": (0.0, 0.0, -0.35),
            "thigh.R": (0.08, 0.0, 0.0),
            "shin.R": (-0.38, 0.0, 0.0),
            "foot.R": (0.08, 0.0, 0.0),
        }
        render_preview("rig-test", (2.25, 2.65, 1.6), (0, 0, 0.75), 1.85, test_pose)
        hand_pose = {"index.02.L": (0.0, 0.0, 0.30), "middle.02.L": (0.0, 0.0, 0.32), "ring.02.L": (0.0, 0.0, 0.32), "pinky.02.L": (0.0, 0.0, 0.28), "thumb.01.L": (0.0, 0.0, -0.35)}
        render_preview("hand-grip-test", (0.58, 0.92, 0.54), (0.345, 0.05, 0.51), 0.38, hand_pose)

    # Record visual and mesh facts before exporting; lights/floor are preview-only.
    mesh_objects = [o for o in objs if o.type == "MESH"]
    mesh_stats = {
        "mesh_objects": len(mesh_objects),
        "vertices": sum(len(o.data.vertices) for o in mesh_objects),
        "triangles": sum(sum(max(0, len(poly.vertices) - 2) for poly in o.data.polygons) for o in mesh_objects),
        "material_slots": sum(len(o.data.materials) for o in mesh_objects),
        "height_m": round(max((o.matrix_world @ v.co).z for o in mesh_objects for v in o.data.vertices) - min((o.matrix_world @ v.co).z for o in mesh_objects for v in o.data.vertices), 3),
        "texture_images": len([im for im in bpy.data.images if im.source == "FILE"]),
    }

    # Remove preview-only lights and floor before saving/exporting the delivery.
    for obj in list(bpy.context.scene.objects):
        if obj == floor or obj.type in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)
    bpy.context.scene.camera = None
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    export_glb(arm, objs)
    result = validate_glb()
    report = {
        "asset_id": "schoolboy-primary",
        "version": "0.2.0",
        "blender_version": bpy.app.version_string,
        "blend_file": BLEND_PATH.relative_to(ROOT).as_posix(),
        "blend_bytes": BLEND_PATH.stat().st_size,
        "glb_file": GLB_PATH.relative_to(ROOT).as_posix(),
        "rig_bones": [b.name for b in arm.data.bones],
        "mesh_statistics": mesh_stats,
        "glb_validation": result,
        "preview_files": [p.relative_to(ROOT).as_posix() for p in sorted(PREVIEW_DIR.glob("schoolboy-*.png"))],
        "animation_clips": [],
        "status": "rejected-procedural-exploration",
        "quality_gate": {
            "visual_direction": "FAIL: remains primitive-derived and toy-like; does not meet semi-realistic brief",
            "shorts_coverage": "FAIL: crotch opening remains visible in front/rear preview",
            "optimization": "FAIL: 160196 estimated triangles and 75 mesh objects exceed provisional targets",
            "finger_rig": "TECHNICAL DRAFT: 5 digits per hand represented; gripping pose requires rigging cleanup",
            "production_approval": "NOT APPROVED; do not use for MotionBoard or start animation production",
        },
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("MOTIONBOARD_BUILD_REPORT=" + json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
