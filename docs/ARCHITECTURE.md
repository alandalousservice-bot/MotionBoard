# Architecture

## Goal

Provide a small, standalone browser gallery that loads reviewed 3D content and exposes playback and camera controls. Keep the data model and viewer separable so a React-based host can later mount the gallery without coupling it to SPEX TECH business records.

## Proposed layers

1. **Presentation shell** — Arabic-first RTL page, accessible controls, skill title, concise instruction, status and loading/error states.
2. **Gallery feature** — reads a static catalog, supports category/skill selection, and passes an asset reference to the viewer. No authoring or publishing flow.
3. **3D viewer feature** — owns canvas lifecycle, model loading, camera orbit/zoom limits, playback, pause, loop, speed, and cleanup.
4. **Content catalog** — versioned JSON metadata that points to approved GLB files. Catalog entries carry technical and pedagogical review states and license provenance.
5. **Static asset layer** — versioned GLB and optional preview images. No database or media service is required for the initial gallery.

## Selected stack

- React 19 + TypeScript 5.9 + Vite 8 for the standalone app. Exact versions are pinned in `package.json` and `package-lock.json`.
- React Three Fiber 9 for the responsive scene, with Three.js 0.186 for `GLTFLoader`, `AnimationMixer`, and `OrbitControls`.
- Ajv 8 with `ajv-formats` validates optional motion metadata against the Draft 2020-12 schema before display.
- Native CSS logical properties and `dir="rtl"` for the interface. Keep the model's authored forward axis and camera setup independent of text direction.
- Local `.glb` file selection for the demo. The browser reads the file into memory; it is not transmitted to a server. Optional metadata is also selected locally.

The runtime remains independent of SPEX TECH. Its use of React Three Fiber 9 is compatible with React 19, as recorded in `TECHNICAL_AUDIT.md`.

## Component boundaries

```text
AppShell
├── SkillCatalog
├── SkillDetails
└── MotionViewer
    ├── ViewerCanvas
    ├── CharacterAsset
    ├── CameraControls
    └── PlaybackControls
```

The UI owns selected skill and accessible labels. The viewer owns renderer, scene, camera, loaded GLTF scene, animation mixer/actions, and disposal. A narrow adapter accepts a validated skill record and emits playback/loader state; it does not know about school records or assessment data.

In this demo the catalog is deliberately empty. The local-file picker exposes animation clips inside an imported GLB without creating a catalog entry. Optional metadata is accepted only when it validates and its `clipName` matches the selected clip. Imported preview material remains visibly unapproved regardless of metadata review fields.

## Runtime behavior

- Load a catalog record only when it is approved and available for display.
- Start in a stable three-quarter view, with zoom and orbit bounds that keep the full body visible.
- Expose discrete play/pause, loop, speed options, clip selection, and keyboard-operable orbit/zoom/reset controls outside the canvas.
- Handle loading, parse errors, a model without clips, context loss, and reduced-motion preference without silently displaying a different clip.
- Use one active clip per character by default. Stop previous actions before switching; dispose of mixer and GPU resources when changing or unmounting assets.
- Keep scene motion deterministic at the selected playback rate. Do not encode UI state or locale into animation files.

User-selected GLB data is read with `GLTFLoader.parseAsync` and kept in client memory. On file replacement or app unmount, stop/uncache mixer actions and dispose the loaded geometry, materials, textures, and `ImageBitmap` sources.

## Deployment and cost

Initial delivery can be a static site plus static GLB/JSON assets. There is no reason to provision a database, API, authentication service, or recurring motion-generation service for the display-only scope. Keep asset size modest, cache immutable versioned exports, and measure on target school devices before deciding on compression or a CDN.

## Extension boundary for host integration

Later embedding should use a documented React component or isolated route that receives a catalog URL or catalog object and an optional theme/config object. It must not import SPEX TECH domain models. If cross-origin embedding is chosen, separately review CSP, CORS, accessibility, and sizing. Integration requires a distinct approved change described by `INTEGRATION_PLAN.md`.
