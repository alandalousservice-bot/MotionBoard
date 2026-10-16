# Animated glTF test assets

These are unmodified, licensed technical fixtures for MotionBoard's local GLB viewer. They are not MotionBoard characters, and none of their animation clips is pedagogically reviewed or approved. Each adjacent source/license notice is retained with the fixture.

## RobotExpressive.glb — primary visual/browser fixture

- Source: [three.js examples/models/gltf/RobotExpressive](https://github.com/mrdoob/three.js/tree/dev/examples/models/gltf/RobotExpressive)
- Binary: [RobotExpressive.glb](https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/models/gltf/RobotExpressive/RobotExpressive.glb)
- Creator: Tomás Laulhé, CC0 1.0 Universal; modifications by Don McCurdy (three facial-expression morph targets, FBX2GLTF conversion, duplicate material removal and metalness adjustment).
- Source credit/license notice: [RobotExpressive-SOURCE-README.md](RobotExpressive-SOURCE-README.md) (copy of the source README).
- Size: 463,988 bytes; SHA-256 `047f5e5fb3bb6d378bd1df16ca6137f2a596c99b3a1b5690b4020c05aaf6f319`.
- Skin/mesh: 2 skins; 14 meshes.
- Clips (duration): `Dance` 3.3333 s; `Death` 0.9583 s; `Idle` 3.3333 s; `Jump` 0.7083 s; `No` 1.6667 s; `Punch` 0.8333 s; `Running` 0.9583 s; `Sitting` 0.4167 s; `Standing` 0.4167 s; `ThumbsUp` 1.5833 s; `Walking` 0.9583 s; `WalkJump` 0.8333 s; `Wave` 1.8333 s; `Yes` 1.6667 s.

## Fox.glb — Khronos multi-clip fixture

- Source: [KhronosGroup/glTF-Sample-Assets/Models/Fox](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/Fox)
- Binary: [Fox.glb](https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/Fox/glTF-Binary/Fox.glb)
- Original model: PixelMannen, 2014 — CC0 1.0 Universal.
- Rigging and animation: tomkranis, 2014 — CC BY 4.0 International.
- glTF conversion: @AsoboStudio and @scurest, 2017 — CC BY 4.0 International.
- License: [Fox LICENSE.md](LICENSE.md); notice excludes logos/trademarks.
- Size: 162,852 bytes; SHA-256 `d97044e701822bac5a62696459b27d7b375aada5de8574ed4362edbba94771f7`.
- Skin/mesh: 1 skin; 1 mesh.
- Clips: `Survey` 3.4167 s; `Walk` 0.7083 s; `Run` 1.1583 s.

## RiggedSimple.glb — Khronos skinning fixture

- Source: [KhronosGroup/glTF-Sample-Assets/Models/RiggedSimple](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/RiggedSimple)
- Binary: [RiggedSimple.glb](https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/RiggedSimple/glTF-Binary/RiggedSimple.glb)
- Model/asset credit: Cesium, 2017 — CC BY 4.0 International.
- License: [RiggedSimple-LICENSE.md](RiggedSimple-LICENSE.md); notice excludes logos/trademarks.
- Size: 15,104 bytes; SHA-256 `3a79dabb67bb0cd598a18d08b954d9d357c27c30672f82ef5d3f4e7fe6ca3401`.
- Skin/mesh: 1 skin; 1 mesh.
- Clip: `animation_0` 2.0833 s (source clip unnamed; loader assigns this name).

Durations are the maximum key times from each clip's input accessors. They describe file data only, not movement quality. The files are unmodified and are retained with source/license attribution for reproducible technical tests.

## mb004b-rig-probe.glb — MotionBoard MPFB2 rig deformation probe

- Source workflow: MPFB2 2.0.18 built-in hm08 child-anchor mesh and standard rig, based on the editable MPFB2 feasibility source under `production/blender/mpfb2-feasibility/`.
- License/provenance: MPFB2's official asset license identifies its core human graphics assets as CC0 1.0; add-on code is GPL-3.0-or-later. This GLB contains a technical test mesh and a single scripted joint-articulation action authored for this feasibility check. It is not a final MotionBoard character or educational animation.
- Test clip: `MB004B_RIG_TEST_NOT_EDUCATIONAL`, frames 1–105 at 30 fps (approximately 3.47 s). It poses shoulder, elbow, wrist, hip, knee, ankle, finger and thumb one at a time. It exists only to check loading/skinning and is not pedagogically reviewed.
- Browser development route: `?testAsset=mpfb2-rig-probe` (development server only).
