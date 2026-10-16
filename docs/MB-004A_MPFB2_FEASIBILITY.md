# MB-004A — MPFB2 installation and child base-mesh feasibility

**Date:** 2026-10-16 (Africa/Algiers)
**Branch:** `mb-004/reference-guided-character`
**Result:** **PARTIAL** — MPFB2 installed and created an editable human base mesh with its standard rig in Blender 5.2.2. The generic child age anchor is not verified for ages 7–9 or for the MotionBoard reference.

## Decision

MPFB2 is a viable Blender authoring tool for producing and editing a genuine human base mesh. The official MPFB2 add-on v2.0.18 ran in Blender 5.2.2 LTS, created the mesh, added its standard rig, and exported a GLB that Blender re-imported.

This is **not approval of the character pipeline or character design**. MPFB2 exposes a broad `child` age anchor (internally `0.1875`), not controls that identify a child as 7, 8, or 9 years old. The generated mesh is an unclothed generic base with no hair, skin asset, shoes, school uniform, Algerian-specific styling, or match to the supplied design. Its suitability for the intended age and reference remains unverified. Product Owner review and a character artist's proportion review remain necessary before final character production.

## Reference and prior limitation report

Reviewed [MB-004 production limitation](MB-004_PRODUCTION_LIMITATION.md) and the local image `C:\Users\ous\Downloads\a_clean_studio_rendered_character_design_model_sh.png` (SHA-256 `A02135D9A986A6C6E286961EE8FBB6342DE532A88DC82C661A541EDE9565A706`). The image is a visual sheet with front, side, rear, three-quarter and detail views; it is not source geometry. The creator and redistribution license are unknown, so the image was not copied into the repository or used as an asset.

## Installation and compatibility

- Blender: **5.2.2 LTS**, Windows x64, build hash `d13f752e3b9c` (build date 2026-09-15).
- MPFB2: **2.0.18**, from the [Blender Extensions MPFB listing](https://extensions.blender.org/add-ons/mpfb/), package `add-on-mpfb-v2.0.18.zip`.
- Package SHA-256: `C075B3E9B94B8E5556A5F03F4653602D02EA306DE08126E8F55ED6DEE28A2DAD`. This matches the digest in Blender Extensions' download URL. The installed package manifest declares minimum Blender `4.2.0` and `GPL-3.0-or-later` for add-on code.
- Compatibility: **PASS for installation, human creation, standard rig creation, render and GLB round trip in Blender 5.2.2**. The official [getting-started guide](https://static.makehumancommunity.org/mpfb/docs/getting_started.html) states Blender 4.2.0 or newer is required.
- MPFB ran without MakeHuman. No system asset pack or third-party pack was installed for this test. The [official instructions](https://static.makehumancommunity.org/mpfb/docs/getting_started.html) recommend the MakeHuman system assets for skin, eyes, teeth and similar assets, but they are not needed to create the bare base mesh.
- Add-on install, preferences, data and extensions were directed to a temporary isolated Blender profile under `%TEMP%\motionboard-mpfb2-isolated`; the downloaded package and test outputs are in that temporary profile or this repository. MPFB was not installed into the user's normal Blender profile.
- During the initial failed manual module load, MPFB wrote its own bootstrap configuration/log files under `%APPDATA%\Blender Foundation\Blender\5.2\mpfb` and created an empty data directory under `%APPDATA%\Blender Foundation\Blender\5.2\extensions\.user\user_default\mpfb`. These were not Blender preference files or settings for other add-ons. Their directory timestamps show they were created during this task. The shell's local action policy rejected removal of those exact generated folders, so they may need manual cleanup; all successful MPFB operations used the isolated profile.

## License and provenance

- Add-on source is GPL-3.0-or-later; see the [official MPFB code license](https://github.com/makehumancommunity/mpfb2/blob/v2.0.18/LICENSE.CODE.md) and the downloaded package manifest.
- The [official asset license](https://github.com/makehumancommunity/mpfb2/blob/v2.0.18/LICENSE.ASSETS.md) and [license overview](https://static.makehumancommunity.org/about/license.html) state the core MPFB/MakeHuman graphics assets are CC0. The test uses MPFB's bundled hm08 base mesh and built-in shape targets; it includes no separately downloaded asset pack.
- The official asset-pack catalogue identifies packs with different licenses, including CC0 and CC-BY. Check the individual asset/pack attribution and license before using any additional hair, clothes, shoes, or other contributed assets. For example, the catalogue marks the Shoes 02 pack CC-BY; no pack assets were used here. See [asset packs](https://static.makehumancommunity.org/assets/assetpacks.html).
- No MotionBoard final character, garment, shoe, or animation is claimed by these outputs. The generated mesh is a feasibility artifact whose provenance is MPFB2 v2.0.18 and its bundled core mesh/targets.

## Test results

| Check | Result | Evidence |
| --- | --- | --- |
| Official package installed in isolated profile | PASS | Blender Extensions package SHA matches download URL; MPFB reported build `20261010` and initialized. |
| Real editable human mesh created | PASS | `.blend` contains the MPFB hm08 human mesh, shape keys and editable Blender data. |
| Child age anchor applied | PASS, with scope limit | Generated shape keys contain `$ch`; MPFB source maps its `child` enum to age `0.1875`. This is not a 7–9-year-specific control. |
| Standard rig created | PASS | MPFB standard rig operator returned `FINISHED`; armature and vertex groups are in the `.blend`. |
| Mesh integrity inspected | PARTIAL | 19,158 vertices, 37,364 edges, 18,486 polygons, 15 shape keys, 291 vertex groups; 784 boundary edges, 0 wire edges and 0 zero-area faces. Boundary edges mean this test mesh is not closed/watertight; their suitability needs topology review before production. |
| GLB export | PASS with limitation | 6,634,028-byte GLB exported and re-imported in Blender. Exporter warned that vertices have more than four joint influences; glTF keeps the four highest weights and normalizes them. |
| Neutral previews | PASS | Front and side renders show the generated base mesh; they are not visual approval or a final-character presentation. |

The generated mesh dimensions at the selected meter scale are approximately `0.631 × 0.252 × 1.005 m`. This measurement does not establish that the body proportions are appropriate for a 7–9-year-old Algerian child. No skin/eye/hair assets were applied, and the mesh remains unclothed.

## Test assets

- [Editable Blender source](../production/blender/mpfb2-feasibility/mpfb2-child-anchor-feasibility.blend)
- [GLB export smoke-test artifact](../production/blender/mpfb2-feasibility/mpfb2-child-anchor-feasibility.glb)
- [Front preview](../production/blender/mpfb2-feasibility/mpfb2-child-anchor-front.png)
- [Side preview](../production/blender/mpfb2-feasibility/mpfb2-child-anchor-side.png)
- [Mesh inventory](../production/blender/mpfb2-feasibility/mesh-report.json)
- [Reproduction script](../production/blender/mpfb2-feasibility/create_mpfb2_feasibility_test.py)

## Reproduction

The test script expects the official v2.0.18 extension ZIP at `%TEMP%\motionboard-mpfb2-isolated\add-on-mpfb-v2.0.18.zip`. Download it from the [official Blender Extensions listing](https://extensions.blender.org/add-ons/mpfb/) and verify its SHA-256 above. Then set an isolated profile and run the script from the repository root:

```powershell
$profile = Join-Path $env:TEMP 'motionboard-mpfb2-isolated'
$env:BLENDER_USER_CONFIG = Join-Path $profile 'config'
$env:BLENDER_USER_SCRIPTS = Join-Path $profile 'scripts'
$env:BLENDER_USER_DATAFILES = Join-Path $profile 'datafiles'
& 'C:\path\to\blender.exe' --background --python 'production/blender/mpfb2-feasibility/create_mpfb2_feasibility_test.py'
```

The script installs the ZIP into an isolated extension repository through Blender's extension installer, creates the generic child-anchor base and standard rig, writes the `.blend`, renders front and side views, exports a GLB, and imports that GLB back into Blender. It does not create clothes, shoes, hair, or animations.

## Remaining blockers and recommendation

1. No evidence establishes MPFB's broad `child` morph as the right anatomy for ages 7–9. Compare proportions against age-appropriate, rights-cleared references with a qualified character artist.
2. The reference's expressive face, hairstyle, silhouette, clothing, footwear, five-finger hand quality, and flag details are not represented by this base mesh.
3. Review the 784 boundary edges and deformation behavior; this run checked counts and export, not a professional topology/deformation sign-off.
4. The GLB exporter reduces joint weights to four per vertex. Validate representative poses and skinning in the MotionBoard viewer before relying on this rig for production.
5. Additional asset packs require asset-level license review; no external pack was added.

**Recommendation: PARTIAL / NO-GO for final character production.** MPFB2 passed the base-mesh feasibility gate and is worth further artist-led evaluation. Do not begin educational animation production or claim visual approval from this technical test.
