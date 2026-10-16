# MotionBoard 3D

Standalone, display-only 3D motor-skills gallery for Algerian primary physical education. This repository is an isolated foundation for possible later integration into SPEX TECH; it does not modify or depend on that platform.

## Current status

The repository contains a standalone React/TypeScript 3D viewer and the first original canonical schoolboy prototype (`schoolboy-v0.1.0`). The character is a real editable Blender model with a humanoid rig and GLB export, but remains a draft awaiting Product Owner visual and rig review. It has no animation clips and is not a pedagogically approved asset. Walking, running, and two-foot jumping remain acceptance targets, not completed content. The demo starts empty and can open a self-contained GLB from the user's device for technical preview. Imported files are processed locally and are always marked as unapproved in the UI.

Full character and animation production remains gated on review and approval of [the technical audit](docs/TECHNICAL_AUDIT.md).

## Product boundaries

- One consistent, age-appropriate cartoon schoolboy in a white PE uniform with green and red details and an accurate Algerian flag.
- A professionally produced and pedagogically reviewed animation library with orbit, zoom, play, pause, loop, slow motion, and selection controls.
- Arabic RTL user interface, with layout direction independent of 3D coordinate direction.
- Display-only library. No lesson memos, annual plans, assessment documents, automatic generation, or automatic publishing.
- No required backend. Prefer static hosting and local assets; add a service only after a demonstrated need and explicit architecture review.

## Repository map

```text
docs/                 Product, technical, asset, and quality decisions
schemas/              JSON Schemas for character and motion metadata
assets/characters/    Approved character exports and source files
assets/animations/    Approved animation exports and source files
assets/references/    Licensed reference material and review evidence
src/app/              Future standalone app shell and RTL experience
src/features/         Future gallery, viewer, and playback features
src/shared/           Future shared UI and runtime primitives
```

Asset directories are empty until actual licensed and reviewed assets are delivered.

## Run locally

Requirements: Node.js 20.19+ or 22.12+ (Node 24 is also supported by the current toolchain) and npm. The app has no backend or upload service.

```sh
npm ci
npm run dev
```

Open the local address printed by Vite. Choose a self-contained `.glb` file from your device to load a model. If it contains animation clips, select one from the clip list. An optional JSON sidecar can provide an Arabic title, description, and movement phases; it must match the selected clip name and validate against `schemas/animation-asset.schema.json`. The sidecar is descriptive only: the interface continues to identify all locally imported material as unapproved.

## Verification

```sh
npm run typecheck
npm run validate:schemas
npm test
npm run build
```

The tests cover Draft 2020-12 schema compilation, metadata parsing, playback state/speed/loop/restart, disposal, toolbar actions, camera-pad actions, and empty/local-file UI states. Also check the responsive layout in a desktop and narrow/mobile viewport, then import an appropriately licensed local GLB to check orbit, zoom, reset, clip selection, and WebGL behavior. This repository contains no GLB, so no model-specific browser check or pedagogical review can be claimed from the included tests. A successful build or a technically valid file does not certify movement quality.

See [the MB-002 verification report](docs/MB-002_VERIFICATION.md) for the current run results and limitations.

## Canonical schoolboy prototype

The MB-003B source is `production/blender/schoolboy-v0.1.0.blend`; the reproducible model/export script is `production/blender/build_schoolboy.py`. On the Microsoft Store Blender package, run `production/blender/run_store_blender.ps1`; with Blender installed conventionally, run `blender --background --python production/blender/build_schoolboy.py`. The script saves a Blender source, exports `assets/characters/schoolboy-v0.1.0.glb`, and renders front, side, rear, three-quarter, and non-educational rig-test previews under `assets/previews/`.

The GLB is included in the development-only test selector with `npm run dev` → `http://127.0.0.1:4173/?testAsset=schoolboy`. It is static by design: no walking, running, jumping, or other motion clips were authored. See [the MB-003B verification report](docs/MB-003B_VERIFICATION.md) for Blender, rig, geometry, browser validation, provenance, and pending-review limits.

## Key documents

- [Architecture](docs/ARCHITECTURE.md)
- [Technical audit](docs/TECHNICAL_AUDIT.md)
- [Asset pipeline](docs/ASSET_PIPELINE.md)
- [Character specification](docs/CHARACTER_SPEC.md)
- [Animation quality and acceptance](docs/ANIMATION_QUALITY.md)
- [Integration plan](docs/INTEGRATION_PLAN.md)
- [Development conventions](AGENTS.md)

## Local animated GLB test fixtures

For repeatable development-only browser checks, this branch includes attributed fixtures under `assets/test-only/`: RobotExpressive (CC0 1.0), Khronos Fox (model CC0; rigging and animation CC BY 4.0), and Khronos RiggedSimple (CC BY 4.0). Start Vite and open `http://127.0.0.1:4173/?testAsset=robot-expressive`, `?testAsset=fox`, or `?testAsset=rigged-simple`. The dev-only fixture selector replaces the model in place; the query bootstrap and selector are omitted from production. Source credits, licenses, checksums, clip names and durations are recorded in [the fixture README](assets/test-only/README.md). These samples are technical only and are not approved educational movements or the MotionBoard schoolboy.

Run `npm run validate` for the Draft 2020-12 schema checks (`npm run validate:schemas` remains available as an explicit alias).
