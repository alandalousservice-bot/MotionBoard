# MB-005A — Candidate evaluation

**Repository:** alandalousservice-bot/MotionBoard  
**Branch:** mb-005a/character-candidate-evaluation  
**Base:** mb-004b/child-proportion-rig-validation at dd5059075f30a4491cdde33e5501714766a93012  
**Evaluation date:** 2026-10-17 (Africa/Algiers)  
**Blender:** 5.2.2 LTS, Windows x64, build d13f752e3b9c  
**Result:** **PARTIAL.** One CC0 candidate was acquired, imported, rendered, measured, pose-tested, exported and loaded in the actual MotionBoard browser viewer. It is not a viable canonical schoolboy starting point. The three Sketchfab downloads require sign-in; their actual package contents remain uninspected.  
**Customization decision:** **NO-GO.** No candidate is cleared for final customization. Product Owner visual approval remains pending. No educational animation was started.

## Decision

Quaternius’ public Standard male model is the only candidate we could download without login or payment and inspect in Blender. It is a muscular adult-proportioned superhero body in dark briefs, bald and barefoot. Its rig and geometry load and render in MotionBoard, but it has zero animation clips. Its age, face, hair, clothing, footwear and silhouette differ substantially from the supplied reference. Adapting it would require a character artist to reshape the anatomy and build the complete school sports uniform, hair and shoes.

**Candidate selection:** None. Listing text and triangle counts are insufficient to choose a child character. Future screening must begin with visual suitability against the approved reference (apparent age, face, hair, proportions, silhouette and overall style) using a reviewable public preview. Do not download or technically evaluate a candidate that fails this visual gate. A visually promising preview still requires authorized access and exact-file licensing checks before acquisition.

## Candidate access and license review

The listing observations below were visible on each model’s public page. A listing license label is not equivalent to an inspection of package contents; no Sketchfab package was downloaded or hashed.

| Candidate | Listing details | License shown | Download result | Technical status |
| --- | --- | --- | --- | --- |
| [Canino3d, Free Stylized Cartoon Game Boy Character Rigged](https://sketchfab.com/3d-models/free-stylized-cartoon-game-boy-character-rigged-92b4b22d14194be191c0df00f6e62b3d) | Listing says rigged and “Skeleton More than 100 Face Blendshape”; 66.1k triangles / 31.2k vertices. Visual suitability has not been approved. | CC BY 4.0 shown on listing. | Official download control opens “Log in to Sketchfab.” **ACCESS REQUIRED.** | No package inspection. Listing viewer reported that the model was too heavy for the preview device. Page comments mention Blender import/deformation issues; anecdotal only. Not ranked or selected. |
| [giyas3dartist, Cartoon Asian Boy](https://sketchfab.com/3d-models/cartoon-asian-boy-db62a970abc549f58f8be3f53ac96f94) | Description says “rigged in blender”; 62.4k triangles / 36k vertices. Visual suitability has not been approved. | CC BY 4.0 shown on listing. | Official download control opens Sketchfab login. **ACCESS REQUIRED.** | No package or rig inspection. Listing viewer reported model too heavy; actual age proportions unverified. Not ranked or selected. |
| [Sunny, 3D Character Young Boy](https://sketchfab.com/3d-models/3d-character-young-boy-60dfa6ac87e84e7dae8dba220526946d) | 17.4k triangles / 8.9k vertices. Listing points to a separate “3D Character Young Boy - Rigged” link. Visual suitability has not been approved. | CC BY 4.0 shown for the listing. | Official download control opens Sketchfab login. **ACCESS REQUIRED.** | No package inspection. The listed edition’s skeleton status is unverified. The separate rigged edition was not treated as the same file. Not ranked or selected. |
| [Quaternius, Universal Base Characters](https://quaternius.com/packs/universalbasecharacters.html) / [itch.io listing](https://quaternius.itch.io/universal-base-characters) | Adult muscular superhero styling, bald, in briefs and barefoot. Fails the required child visual target. | CC0 1.0 Universal. Modification and commercial use are allowed; attribution is not required. Credit is retained here for provenance without implying endorsement. | Public itch.io “No thanks, just take me to the downloads” route yielded the Standard archive without sign-in or payment. | Fully inspected below as a technical test only. Rejected as canonical character; do not adapt it into a child. |

The three Sketchfab listing pages show CC BY 4.0, but their exact downloadable editions remain unverified because the official controls require login. No short links, hidden endpoints or download protections were bypassed. Sunny’s separately linked rigged edition was not substituted for its listed model. Quaternius’ priced Source edition was not confused with the free Standard archive.

License references: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) and [Creative Commons CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). The CC0 deed allows copying, modifying, distributing and commercial use; it also says CC does not verify the copyright status of each work. No endorsement is implied.

## Quaternius Standard provenance

- **Creator/product:** Quaternius, Universal Base Characters, Standard edition.
- **Official sources:** [pack page](https://quaternius.com/packs/universalbasecharacters.html), linked [itch.io download page](https://quaternius.itch.io/universal-base-characters).
- **Route:** Download Now → “No thanks, just take me to the downloads” → Standard ZIP. The page listed Standard at 122 MB and Source at 600 MB; Source was listed as included only when paying $19.99 USD or more.
- **Downloaded archive:** 128,968,391 bytes, SHA-256: FDBF1804C90DFC1EA03E992BFF7DA2DFD1A79318E13270A660180F9308455F40. Downloaded 2026-10-16 from the public no-payment route.
- **Male source in archive:** Base Characters/Godot - UE/Superhero_Male_FullBody.gltf, 30,989 bytes, SHA-256: E7FCEA214ECF8855AFBF910B50DE6F9C7D1DECFB71CA28BAD8A4481452DAFEB4. Its external binary is 720,076 bytes, SHA-256: 459003F9745853AE562A85506A2B94DD56515C1F37728F9FA3D2CE1A3E4CD92F.
- **Source subset:** original Standard male/female glTF, binaries and textures needed for import are in [the test asset source folder](../assets/test-only/quaternius-universal-base-characters/source/Base%20Characters/Godot%20-%20UE/). The full 122 MB ZIP is not committed.
- **Formats and rig:** Standard contains glTF 2.0 and FBX exports; the male glTF contains one skin and 65 joints, including five named finger chains per hand. The Standard ZIP has no .blend file. The creator describes .blend files as part of the separate Source edition, which was not obtained.
- **Animations:** zero in source and exported male model; static T-pose.
- **Import/export caveat:** the male glTF references two missing normal-map filenames: T_Eye_Normal_png.png and T_Hair_1_Normal_png.png; the archive contains T_Eye_Normal.png and T_Hair_1_Normal.png. Blender initially logged missing-image warnings. The finalizer redirects only imported image datablocks to those source files and packs them into the .blend and GLB. It does not change retained source glTF or textures. Blender’s exporter also warned that multiple image nodes feed a texture and the resulting glTF sampler uses the first node. Recheck material fidelity before production.
- **Editable test file:** [imported Blender file](../production/blender/mb005a/quaternius-male-imported.blend), 15,565,682 bytes, SHA-256 93EAA51982FC2DADC331DABBE496401C554897B6A0639858885E5464BE839D20. Images are packed. This is an imported derivative, not the creator’s original .blend.
- **Browser test GLB:** [male Standard test GLB](../assets/test-only/quaternius-universal-base-characters/quaternius-male-standard-test.glb), 15,548,260 bytes, SHA-256 1A8DC2664169FAE222FCA3BA1A7C442B7C7050B2A0FF9B255BB3E2D6F8B484D3. It has zero clips.

## Blender inspection

Measurements are ratios of this generic model, not medical measurements or age norms. The model has no age setting. The body is in T-pose; anatomical landmarks are approximations from mesh bounds and rig bones.

### Male dimensions

Main skinned mesh bounds are approximately 1.859 × 0.291 × 1.820 model units. A separate helper object expands overall bounds and is excluded from body height below.

| Measure | Model-space value | % of 1.810 body height | Method / caveat |
| --- | ---: | ---: | --- |
| Body height | 1.810 | 100% | Main skinned body mesh bounds |
| Head estimate | 0.210 | 11.6% | Mesh top to Head-bone start; not a facial landmark |
| Shoulder span | 0.424 | 23.4% | Distance between upper-arm bone heads |
| Upper arm | 0.251 | 13.9% | Bone length |
| Forearm | 0.244 | 13.5% | Bone length |
| Shoulder to middle fingertip | 0.739 | 40.8% | Upper arm + forearm + wrist-to-fingertip bone distance |
| Wrist to middle fingertip | 0.244 | 13.5% | Bone endpoints; neutral hand silhouette is narrow |
| Torso proxy | 0.549 | 30.3% | Hip-bone head to base of neck; not an anthropometric torso measure |
| Thigh | 0.429 | 23.7% | Bone length |
| Lower leg | 0.459 | 25.3% | Bone length |
| Hip to floor | 0.971 | 53.7% | Hip-bone height above body mesh bottom |
| Foot | 0.238 | 13.1% | Foot and ball bone lengths; candidate has bare feet |

### Geometry and rig results

| Check | Result |
| --- | --- |
| Male Blender meshes | 4 objects: eyebrows (646 vertices / 984 tris), eyes (556 / 768), skinned body (7,281 / 12,566), unweighted Icosphere helper (42 / 80); total 8,525 vertices / 14,398 triangles. |
| Female sibling | 5 Blender mesh objects; 8,928 vertices / 15,220 triangles; one 65-bone rig; zero clips. It is also adult-proportioned and not a schoolboy candidate. |
| Materials / images | 3 materials; source male glTF lists 7 image URIs. Two normal-map URI typos noted above. |
| Skeleton | One armature, 65 bones; all marked deform. Includes spine/head, upper/lower arms, wrists, thighs, calves, feet/ball and five digit chains per hand. |
| Main-body weights | Maximum 4 influences per vertex: 1 influence=1,057 vertices; 2=4,335; 3=876; 4=1,013. The 42-vertex helper has no weights. No main-body vertex exceeded glTF’s four-influence baseline. |
| Actions | Zero source actions / animation clips; zero after GLB export. |
| Topology scan | No zero-area faces or loose edges found. Boundary edges: body 1,988; eyes 316; eyebrows 280; helper 0. The author’s intended surface boundaries were not classified; an artist must inspect seams/open edges before production. No production-topology approval is claimed. |
| Extra object | Unweighted 42-vertex Icosphere object, not visibly apparent in the browser. Its purpose was not established; it needs artist review. |
| Articulation pose | A Blender diagnostic pose rotated shoulder, elbow, wrist, hip, knee and ankle/foot controls and rendered a comparison. This confirms response to one moderate test pose, not full range, contact, weights, finger curls or grasping. |

### Actual Blender renders

These are Blender 5.2.2 renders of imported geometry, not AI-generated pictures. They show the source model without added hair, clothes, shoes, flag or educational movement.

#### Male Standard

| Front | Side | Rear | Three-quarter |
| --- | --- | --- | --- |
| ![Male front](../production/blender/mb005a/male-front.png) | ![Male side](../production/blender/mb005a/male-side.png) | ![Male rear](../production/blender/mb005a/male-rear.png) | ![Male three-quarter](../production/blender/mb005a/male-three-quarter.png) |

| Face | Hand | Bare foot (no shoe mesh) | Diagnostic articulation pose |
| --- | --- | --- | --- |
| ![Male face close-up](../production/blender/mb005a/male-face-closeup.png) | ![Male hand close-up](../production/blender/mb005a/male-hand-closeup.png) | ![Male bare foot](../production/blender/mb005a/male-shoe-closeup.png) | ![Male articulation pose](../production/blender/mb005a/male-articulation-pose.png) |

Neutral hand geometry does not clearly separate the five digits from the inspected angle. Rig bones exist, but approved hand anatomy/grasp capability is not established.

#### Female sibling from the same Standard pack

| Front | Side | Rear | Three-quarter |
| --- | --- | --- | --- |
| ![Female front](../production/blender/mb005a/female-front.png) | ![Female side](../production/blender/mb005a/female-side.png) | ![Female rear](../production/blender/mb005a/female-rear.png) | ![Female three-quarter](../production/blender/mb005a/female-three-quarter.png) |

| Face | Hand | Foot | Diagnostic articulation pose |
| --- | --- | --- | --- |
| ![Female face](../production/blender/mb005a/female-face-closeup.png) | ![Female hand](../production/blender/mb005a/female-hand-closeup.png) | ![Female foot](../production/blender/mb005a/female-shoe-closeup.png) | ![Female articulation pose](../production/blender/mb005a/female-articulation-pose.png) |

## MotionBoard browser test

- **App / route:** local Vite viewer at http://127.0.0.1:4176/?testAsset=quaternius-male.
- **Browser / viewport:** ChatGPT in-app browser on Windows, 1,200 × 660 CSS pixels.
- **Load, render, materials — PASS:** model visibly rendered as 3D with materials; viewer identified quaternius-male-standard-test.glb. It showed no selectable clips.
- **Camera orbit — PASS:** canvas drag changed view from front three-quarter to rear.
- **Zoom — PASS:** wheel input visibly changed model scale.
- **Reset — PASS:** reset control returned camera to saved default view.
- **Asset switch — PASS for visible transition:** switched to existing RobotExpressive.glb test model and back; both loaded, and no stale Robot geometry remained after return. This is not a heap/resource-leak measurement.
- **Animation selection/playback — NOT TESTED for this candidate:** zero clips, so playback, pause, restart, loop and speed options were disabled/unavailable.
- **Browser deformation — PARTIAL:** GLB renders and has a skeleton; the viewer cannot animate it because it has no clip. Joint/deformation approval is still open.
- **Resource disposal/memory leaks — NOT TESTED:** no GPU heap or resource-count instrumentation was run.
- **Console:** one existing warning captured: THREE.Clock deprecation. No candidate-specific browser error observed. The AX tree exposed a WebGL fallback message despite a visibly working and interactive WebGL canvas; investigate this discrepancy separately.
- **Arabic RTL:** Arabic RTL labels, loaded filename and zero-clip message remained visible in the desktop viewer; this was qualitative, not a full screen-reader/mobile test.
- **Evidence:** Blender renders embedded above. Live browser was exercised; browser screenshot was not saved as a repository file.

## Reproduction and validation

1. Install Blender 5.2.2 LTS.
2. Download the Standard ZIP from the official [itch.io pack page](https://quaternius.itch.io/universal-base-characters), choose the visible no-payment option, then extract.
3. Point the inspection script at the extracted “Base Characters/Godot - UE” directory and run:

    $env:MOTIONBOARD_QUATERNIUS_SOURCE_DIR = 'C:\path\to\Universal Base Characters[Standard]\Base Characters\Godot - UE'
    $blender = 'C:\path\to\blender.exe'
    & $blender --background --factory-startup --python production/blender/mb005a/inspect_quaternius.py
    & $blender --background --factory-startup --python production/blender/mb005a/finalize_quaternius.py

4. Regenerate the two feature close-ups from the packed Blender file:

    & $blender --background --factory-startup --python production/blender/mb005a/render_features.py

5. Run the browser viewer:

    npm install
    npm run dev -- --port 4176

   Open http://127.0.0.1:4176/?testAsset=quaternius-male.

6. Project checks:

    npm run typecheck
    npm run validate
    npm test
    npm run build

Blender ran with isolated config/scripts/datafiles under %TEMP%\motionboard-mb005a-blender-isolated. Unrelated user Blender settings were not modified.

## Recommendation and blockers

No candidate is recommended or selected. Quaternius Standard male is retained solely as a CC0 viewer/GLB technical test; its adult appearance is disqualifying for MotionBoard and it must not be reshaped into a child. The three Sketchfab listings remain unranked because their preview suitability has not been confirmed against the target reference and their downloadable packages were not accessed.

**Next action:** visually screen available character previews against the reference first. Advance only candidates that clearly read as an age-appropriate schoolboy and match the target style, face and silhouette closely enough to justify further work. Then verify authorized access and exact-file license terms before downloading; only after those gates pass should technical inspection begin.

**Blockers:** visual screening/selection of a suitable candidate; authorized access and exact-file provenance/license review for any candidate advanced; qualified character-artist review of proportions, topology and rig; and separate Product Owner visual approval. Do not begin final customization or movement production until these gates are cleared. No SPEX TECH files/services were accessed or modified, and no educational animation was created.

