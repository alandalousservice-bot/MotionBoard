# MB-003C — Semi-realistic schoolboy redesign verification

**Date:** 2026-10-16 (Africa/Algiers)  
**Branch:** `mb-003c/semi-realistic-character`  
**Base / START_HEAD:** `mb-003b/character-prototype` — `b568fa3595b6acaf176a0e670acbc9c964869e8a`  
**Status:** **PARTIAL — NO-GO.** A new editable exploratory model and GLB were produced, but the model fails core visual, clothing, deformation, and optimization requirements. It is explicitly marked rejected and is not an approved character.

## Decision

The requested semi-realistic redesign was **not achieved**. The new procedural Blender pass changed several proportions, reduced the eye size, revised footwear geometry, and added individual finger chains. The result still reads as a primitive-derived cartoon/toy. It also retains a visible shorts opening, has awkward finger/thumb joins, and exceeds the geometry and object-count targets. This is evidence that this primitive-based procedural pipeline is not adequate for the requested art direction. Do not use this model in the gallery or start educational animation production from it.

The MB-003B v0.1.0 source and GLB remain intact. Product Owner visual approval remains pending. A character artist or a suitably licensed sculpted character workflow is needed before another character prototype can pass the visual gate.

## Before / after comparison

| Area | v0.1.0 baseline | v0.2.0 exploration | Result |
| --- | --- | --- | --- |
| Silhouette | Exaggerated wide torso/shoulders and large head | Slightly narrower torso, but oversized simple forms remain | Fail: still toy-like, not natural child anatomy |
| Face | Large protruding eyes, bulb ears, simple cap | Smaller eyes/ears and swept lock shapes | Fail: facial volumes and hair remain primitive-looking |
| Hands | Fused hand shapes, no controllable digits | Five digits modeled as segment capsules with finger chains | Fail: segments appear disconnected/sausage-like; thumb connection and grip pose need a proper hand model and rig |
| Shorts | Triangular front/rear gaps | Increased garment overlap and finer voxel remesh | Fail: front/rear crotch opening is still visible |
| Shoes | Ellipsoid shoe uppers and soles | Beveled box sole and upper plus laces | Fail: still blocky and lacks convincing shoe shaping |
| Complexity | 114,332 estimated triangles, 47 mesh objects | 160,196 estimated triangles, 75 mesh objects | Fail: worse than the provisional budget |

The v0.1.0 baseline preview is [`schoolboy-front.png`](../assets/previews/schoolboy-front.png). The new Blender front, face, hand/grip, shoe, and shorts-gap renders are in [`assets/previews/v0.2.0/`](../assets/previews/v0.2.0/), including [`schoolboy-front.png`](../assets/previews/v0.2.0/schoolboy-front.png), [`schoolboy-face-closeup.png`](../assets/previews/v0.2.0/schoolboy-face-closeup.png), [`schoolboy-hand-grip-test.png`](../assets/previews/v0.2.0/schoolboy-hand-grip-test.png), [`schoolboy-shoe-closeup.png`](../assets/previews/v0.2.0/schoolboy-shoe-closeup.png), and both `schoolboy-shorts-*-gap-check.png` renders. These are real Blender renders, not illustration substitutes.

## Modeling approach and provenance

- Blender 5.2.2 LTS, Windows x64, ran in background mode using the locally installed Store package runtime.
- New reproducible script: [`build_schoolboy_v020.py`](../production/blender/build_schoolboy_v020.py).
- Reproduction from the repository root: `production/blender/run_store_blender_v020.ps1`; use `-SkipPreviews` to rebuild the `.blend`, GLB, and report without rerendering previews. With a regular Blender install, run `blender --background --python production/blender/build_schoolboy_v020.py -- --output-root .`.
- The model uses original Blender-generated meshes, curves, and materials. No downloaded character, texture, commercial brand, club logo, or third-party character-authoring asset was used. This avoids uncertain asset redistribution rights; the project's asset license still needs an owner decision before release.
- Preview outputs are isolated under `assets/previews/v0.2.0/`. Version 0.1.0 files were not overwritten. Its original build report is preserved at `production/blender/schoolboy-build-report.json`.
- Machine-readable v0.2.0 statistics and rejected quality gates: [`schoolboy-v020-build-report.json`](../production/blender/schoolboy-v020-build-report.json).

## Rig and deformation checks

The original main body rig names remain, and the armature is versioned as `motionboard-humanoid-v0.2`. It has **48 bones**: the prior 20-bone torso/arm/leg/root set plus 28 finger bones (three segments for index, middle, ring, and pinky, and two thumb segments on each hand). GLB contains one skin and 48 joints.

Blender rendered a neutral stance, a representative shoulder/elbow and hip/knee/ankle test pose, and a curled-hand pose. The body/limb test pose rendered, but this was only a visual spot check. Finger chains are not approved for grasping: the rendered curled pose shows visibly separated capsule segments and a poorly integrated thumb. No complete deformation suite or natural hand-pose review passed. Clothing intersections were **not cleared**; the shorts gap check fails from both front and rear. There are no facial controls, and no animation clips were authored.

## Geometry and GLB

Measured from the generated source and parsed export:

- Height: 1.428 m
- Vertices: 80,416
- Estimated triangles: **160,196** (provisional target 30,000–60,000)
- Blender mesh objects / exported glTF meshes: **75** (provisional target favors minimizing; this is higher than the 47-object baseline)
- Material slots: 74; exported unique glTF materials: 12
- GLB size: 4,957,868 bytes in the recorded build report (about 4.73 MiB)
- Skin joints: 48; animation clips: 0
- No external textures

The build script checked the GLB v2 header and declared length, JSON chunk, glTF asset version, mesh presence, skin presence, joint count, and zero animation clips. These structural checks passed. They do not establish visual quality or valid movement.

## Viewer verification

**Browser:** Codex in-app Chromium, local Vite at `http://127.0.0.1:4175/?testAsset=schoolboy-v020`, desktop viewport approximately 864 × 650 CSS pixels.

| Check | Result | Evidence / notes |
| --- | --- | --- |
| v0.2.0 GLB loads and renders | PASS | Actual browser screenshot showed the loaded character in the WebGL scene. |
| Face-forward orientation, materials, flag | PASS with visual caveat | Character faced the initial camera; white/green/red uniform and small flag badge were visible. Flag detail is small at this viewport. |
| Camera orbit | PASS | Dragged over the canvas; character visibly rotated to a three-quarter view. |
| Zoom | PASS | Scrolled over canvas; model scale changed. |
| Camera reset | PASS | Activated reset control after orbit/zoom; the camera returned to its start position. |
| Asset switching | PASS | Switched from v0.2.0 to the v0.1.0 test asset and back; one viewer canvas remained present. |
| Browser console | PASS with warning | No error-level entries. `THREE.Clock` deprecation warning appeared on viewer loads. |
| Skeleton deformation in browser | NOT TESTED | The GLB has no clips. Blender preview poses are not a browser animation test. |
| Playback / loop / speed / clip selection | NOT APPLICABLE | No animation clips were authored; controls were disabled. |
| Shorts gaps and hand deformations | FAIL | Blender inspection previews show a crotch opening and poor finger/thumb joins. |

The browser accessibility snapshot included fallback text saying the 3D viewer could not run even though a screenshot showed the WebGL model. This mismatch should be investigated separately; it is recorded as an accessibility/state-reporting limitation, not as a rendering pass/fail contradiction.

## Repository checks

- `npm run typecheck` — **PASS**.
- `npm test` — **PASS**, 6 files / 16 tests.
- `npm run build` — **PASS**, Vite production build completed. Existing warning: the minified Viewer chunk is 564.72 kB (150.22 kB gzip), over Vite's 500 kB warning threshold.
- No automated test certifies character appearance, clothing coverage, or rig quality.

## Known defects and blockers

1. Art direction fails: head, hands, torso, face, and hair still use simple primitive-derived volumes and do not meet the semi-realistic target.
2. Shorts remain open at the crotch in front/rear renders. This is a critical garment coverage failure.
3. Finger segment joins, thumb integration, and the grip pose are not natural or production-ready.
4. Shoes remain blocky; the close-up does not meet the natural athletic-shoe requirement.
5. Triangle count is 160,196 and mesh count is 75, both above the provisional performance targets; GLB is about 4.73 MiB.
6. Viewer has a non-fatal `THREE.Clock` deprecation warning and an accessibility snapshot/fallback mismatch.
7. The character is static, has no face controls, and has no educational or other animation clips.
8. No visual approval or asset-level distribution license has been granted.

## Final recommendation

**NO-GO for use, approval, or animation production.** Treat v0.2.0 as a rejected technical/art-direction exploration only. Keep MB-003B v0.1.0 as the preserved comparison baseline. The next step is a professionally sculpted/retopologized character and reviewed hand/clothing construction, followed by fresh fit, rig-deformation, optimization, browser, and Product Owner visual review. Do not start walking, running, jumping, or other motor-skill production until explicit character and rig approval.
