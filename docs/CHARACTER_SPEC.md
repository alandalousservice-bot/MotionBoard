# Character and animation asset contract

No character asset is present yet. The following contract defines what a future approved production asset must provide.

## Visual target

- A consistent, friendly cartoon schoolboy suitable for Algerian primary-school pupils.
- White sports uniform with clear green and red details, without confusing them with the flag.
- Accurate Algerian flag: two vertical fields (green at hoist/left, white at fly/right), with a red crescent and red five-point star centered across the division. Validate orientation against an authoritative Algerian reference and avoid mirrored exports.
- Readable face and limb shapes, modest and practical sportswear, no unsafe or adult-coded styling, and clear silhouettes for movement instruction.
- Maintain the same face, body proportions, skin/material treatment, uniform, flag, and rig across all skills.

## Technical contract

- Delivery: glTF 2.0 binary `.glb`; editable source: `.blend` when source rights permit.
- Units: meters; character height target 1.25–1.55 m as an art-direction range for a stylized primary pupil, not a claim about any real child.
- Local axes: +Z up, +Y forward, +X character-left in the authored Blender convention. Confirm axis mapping in browser and document any conversion at export.
- Origin: ground plane centered between feet; neutral pose centered at origin.
- Rig: one stable humanoid skeleton and neutral A-pose. Every clip must target the same rig version, bone names, and rest pose.
- Mesh: deformation-safe topology around shoulders, elbows, hips, knees, ankles, and wrists; no detached parts unless intentionally attached and documented.
- Skinning: no visible holes, severe candy-wrapper twist, or limb collapse at the reviewed poses.
- Materials: glTF-compatible PBR; use explicit color-space handling and avoid unsupported Blender-only shader networks.
- Flag: geometry/material remains readable from front and three-quarter views and follows cloth/body deformation without mirrored symbols.
- Export: no cameras, lights, unused objects, or production-only helpers in the web GLB; consistent scale, applied transforms, optimized textures, named scenes and clips.
- Performance: establish budgets after target devices are known. Report GLB size, mesh/triangle count, texture dimensions, and material count with each release; do not invent a budget before profiling.

## Animation clip contract

- All clips include the same character rig and begin from the documented rig rest pose or have an explicit start-pose note.
- Clip names are exactly `walk_cycle`, `run_cycle`, and `jump_two_foot` for the first release. Do not use user-facing labels as clip identifiers.
- Time range starts at zero and contains no unintended empty frames. Metadata records frame rate and duration in seconds.
- Looping is true only for seamless cycles. Walk/run must have matching contact pose and root displacement at the seam. Jump is normally a one-shot and does not loop by default.
- Record whether root motion is in-place or traveling; document the authored forward direction and expected viewer treatment.
- Record technical-review and pedagogical-review statuses separately.

## Metadata schema

Use [the character schema](../schemas/character-asset.schema.json) for the character release and [the animation schema](../schemas/animation-asset.schema.json) for each motion item. Add human-readable Arabic and French labels/cues as content is authored and reviewed. Do not include fields about lesson plans, annual plans, or assessments.

Example shape only; this is not a real asset and must not be added as an approved catalog item:

```json
{
  "schemaVersion": "1.0.0",
  "id": "locomotion-walk",
  "clipName": "walk_cycle",
  "characterId": "schoolboy-primary",
  "characterVersion": "1.0.0",
  "skillFamily": "locomotion",
  "movement": "walking",
  "loop": true,
  "rootMotion": "in-place",
  "assetPath": "assets/animations/locomotion-walk-v1.0.0.glb",
  "review": {
    "technical": {"status": "pending"},
    "pedagogical": {"status": "pending"}
  },
  "license": {
    "status": "pending",
    "sources": []
  }
}
```

The example intentionally contains pending reviews and an empty provenance list. It is schema illustration only.
