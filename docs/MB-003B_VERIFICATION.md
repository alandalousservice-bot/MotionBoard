# MB-003B — Canonical schoolboy character prototype

**Date:** 2026-10-16 (Africa/Algiers)  
**Branch:** `mb-003b/character-prototype`  
**Base / START_HEAD:** `mb-003a/animated-glb-validation` — `5848f1702d09e637e2ae3067b7d2408d3db99ed3`  
**Status:** PASS as a technical character prototype; visual/Product Owner approval remains pending.

## Outcome

Blender produced an original, editable, rigged cartoon schoolboy source file, a binary glTF export, and five real render previews. The character loaded in the local MotionBoard viewer with its face toward the default camera, visible white/green/red uniform and flag badge, and no browser errors. The asset is intentionally static: no educational or other animation clips were authored. The prototype remains a draft and must receive Product Owner visual/rig review before animation production.

## Blender environment and reproduction

- Installed package: Blender Foundation Store package `5.2.2.0`.
- Blender build: **Blender 5.2.2 LTS**, Windows x64, build hash `d13f752e3b9c`, build date 2026-09-15.
- Store executable: `C:\Program Files\WindowsApps\BlenderFoundation.Blender_5.2.2.0_x64__ppwjx1n5r4v9t\Blender\blender.exe`.
- Windows denied direct process execution from the protected `WindowsApps` directory. The app execution alias launched the GUI but discarded CLI arguments. Background mode was verified by copying the installed runtime and supporting `blender.crt`, `blender.shared`, DLLs and `5.2` data directory to `%TEMP%\motionboard-blender-runtime`; Blender's Python API printed `BPY_OK 5.2.2 LTS` and exited successfully.
- Reproducible Store-package command from repository root: `production/blender/run_store_blender.ps1`. Add `-SkipPreviews` to regenerate the source/export/report without rerendering existing preview files. With a conventional install, run `blender --background --python production/blender/build_schoolboy.py`.
- Full output log: `%TEMP%\motionboard-schoolboy-build.log`.

## Produced files

- Editable Blender source: [`schoolboy-v0.1.0.blend`](../production/blender/schoolboy-v0.1.0.blend) (2,298,175 bytes; SHA-256 `d7db05aa41573e831e6f77e0fb9ff9562d9a6eaab509dde3722be45d2e90e55f`).
- Reproducible source: [`build_schoolboy.py`](../production/blender/build_schoolboy.py).
- Store-runtime wrapper: [`run_store_blender.ps1`](../production/blender/run_store_blender.ps1).
- Build statistics and GLB parser results: [`schoolboy-build-report.json`](../production/blender/schoolboy-build-report.json).
- Exported character: [`schoolboy-v0.1.0.glb`](../assets/characters/schoolboy-v0.1.0.glb) (3,416,500 bytes; SHA-256 `00fd57cae635320141396ed364fc627f571726d5cadcf03badc0f0b3570fd3f5`).
- Blender renders: [`front`](../assets/previews/schoolboy-front.png), [`side`](../assets/previews/schoolboy-side.png), [`rear`](../assets/previews/schoolboy-rear.png), [`three-quarter`](../assets/previews/schoolboy-three-quarter.png), and [`rig articulation test`](../assets/previews/schoolboy-rig-test.png).

All five renders were produced by Blender 5.2.2 with the same neutral studio lighting and background. The articulation image uses a shoulder/elbow pose on the left arm and hip/knee/ankle pose on the right leg; the other previews show the neutral pose.

## Character, rig, geometry, and export

- Original procedural model authored in the committed Blender Python script. No external mesh, texture, character asset, or rig add-on was used. The render stage is excluded from the GLB.
- Stylized child proportions, warm skin, expressive eyes and smile, white shirt/shorts/trainers, green/red trim, and a front-facing Algerian flag badge. The green hoist band is on the viewer-left of the front view; the red crescent and five-point star face outward.
- Height: **1.44 m**. No image textures; 13 unique glTF PBR materials.
- Source mesh objects: 47; vertices: 57,424; estimated triangles: 114,332; material slots: 48.
- GLB structure: glTF 2.0 binary; 47 meshes; 68 nodes; 1 skin with 20 joints; 256 accessors; zero animation clips. The Blender script checks the GLB header, JSON chunk, declared file length, glTF version, skin, meshes, and absence of motion clips.
- Rig hierarchy and names: `root`; `pelvis → spine → chest → neck → head`; `chest → clavicle.L → upper_arm.L → forearm.L → hand.L`; corresponding `.R` chain; `pelvis → thigh.L → shin.L → foot.L`; corresponding `.R` chain. Total: 20 deform bones including root.
- Blender source uses local +Y forward and +Z up. Export applies a documented 180° yaw at the armature root as a glTF viewer-facing correction; it restores the source armature transform after export. The actual viewer check confirms the face, not the back, is presented at the default camera.

### Provenance and rights

The character geometry and materials were generated from the project-owned script in this repository. No third-party model or texture is embedded. Blender is a GPL-licensed authoring tool; its software license is not used as a proxy for an asset license. No separate asset license has been assigned in this prototype. Record the project owner's chosen asset license and redistribution rights before public release. The authorship/visual direction and flag appearance still require owner review.

## Verification results

### Blender and rig checks

- Background execution and `bpy` API smoke check: **PASS**.
- Full build script: **PASS**, generated editable `.blend`, five renders, and GLB.
- GLB structural assertions (glTF 2.0 header/length, meshes, one skin, 20 joints, no clips): **PASS**.
- Representative shoulder elevation, elbow flexion, hip flexion, knee flexion, and ankle movement set in the non-educational rig test pose; balanced standing captured in neutral front view: **PASS as a prototype articulation check**. The rendered pose remains subject to technical artist review before production use.
- Visible floor penetration or detached limb in the final Blender rig preview: **not observed**. This is a visual spot check, not a full deformation suite.

### MotionBoard viewer

- Browser: Codex in-app Chromium; local Vite at `127.0.0.1:4174`; desktop viewport about 1280×720.
- Reproduction: `npm run dev -- --port 4174`, then open `http://127.0.0.1:4174/?testAsset=schoolboy`.
- GLB loading, skin/material rendering, viewer scale, front orientation, and flag visibility: **PASS**. Arabic RTL main landmark: `dir="rtl"`; one WebGL canvas remained mounted.
- Camera orbit button and camera reset were exercised: **PASS**.
- Browser console: zero error-level entries and no observed WebGL error. The installed runtime logs `THREE.Clock` deprecation warnings.
- The exported GLB has no animation clips, so viewer playback, pose deformation through browser animation playback, and clip selection are **NOT TESTED / NOT APPLICABLE**. Blender's real pose render is the evidence for articulation in this task.

### Project checks

- `npm run typecheck` — **PASS**.
- `npm run validate` — **PASS**, 5 Draft 2020-12 schema tests.
- `npm test` — **PASS**, 6 files / 16 tests.
- `npm run build` — **PASS**, with existing Vite warning for the 564.72 kB minified Viewer chunk (150.22 kB gzip).

## Known limitations and approval gate

- This is a first technical prototype, not an approved final character. Its smooth forms and accessories are deliberately stylized; hand/finger shapes, facial proportions, clothing seams, flag badge legibility at small viewport sizes, and deformation weights need human visual review and likely refinement.
- 47 mesh objects and 114k estimated triangles may be expensive on low-power mobile devices; profile draw calls and performance before release.
- No facial rig, expression controls, animation clips, or pedagogical movement exists. Do not start walking, running, jumping, or retargeting work from this report alone.
- Visual quality, identity, uniform design, and pedagogical suitability have **not** been approved. No qualified PE reviewer was involved or needed for this static character task.
- Asset-level license/redistribution decision remains pending project ownership review; no external model or texture is included.
- No SPEX TECH files or services were accessed or modified.

## Final recommendation

**GO to Product Owner visual and rig review. NO-GO for animation production until the character and rig are explicitly approved.** This report certifies that real Blender, GLB, rig, preview, and viewer artifacts were produced and technically inspected; it does not claim final visual approval.
