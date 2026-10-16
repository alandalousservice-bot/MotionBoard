# Architecture

## Goal

Provide a small, standalone browser gallery that loads reviewed 3D content and exposes playback and camera controls. Keep the data model and viewer separable so a React-based host can later mount the gallery without coupling it to SPEX TECH business records.

## Proposed layers

1. **Presentation shell** — Arabic-first RTL page, accessible controls, skill title, concise instruction, status and loading/error states.
2. **Gallery feature** — reads a static catalog, supports category/skill selection, and passes an asset reference to the viewer. No authoring or publishing flow.
3. **3D viewer feature** — owns canvas lifecycle, model loading, camera orbit/zoom limits, playback, pause, loop, speed, and cleanup.
4. **Content catalog** — versioned JSON metadata that points to approved GLB files. Catalog entries carry technical and pedagogical review states and license provenance.
5. **Static asset layer** — versioned GLB and optional preview images. No database or media service is required for the initial gallery.

## Proposed stack

- React + TypeScript for the UI, after confirming the eventual host's React major version.
- React Three Fiber (R3F) for scene components if the product remains React-based; use plain Three.js if the viewer must remain framework-neutral or R3F's React peer version cannot match the host.
- Three.js `GLTFLoader`/`AnimationMixer` for glTF loading and clip playback. These provide the required browser-side primitives for pause, time scaling, and action control.
- Native CSS logical properties and `dir="rtl"` for the interface. Keep the model's authored forward axis and camera setup independent of text direction.
- Static JSON and bundled/CDN assets under a stable versioned path. Start with same-origin assets; consider a CDN only when measured transfer or cache needs justify it.

This is a recommendation, not an installed or tested app stack. See `TECHNICAL_AUDIT.md` for version pairing and unresolved checks.

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

## Runtime behavior

- Load a catalog record only when it is approved and available for display.
- Start in a stable three-quarter view, with zoom and orbit bounds that keep the full body visible.
- Expose discrete play/pause, loop, speed options, and selection controls outside the canvas so they work with keyboard and assistive technology.
- Handle loading, unsupported asset, context loss, and reduced-motion preference without silently displaying a different clip.
- Use one active clip per character by default. Stop previous actions before switching; dispose of mixer and GPU resources when changing or unmounting assets.
- Keep scene motion deterministic at the selected playback rate. Do not encode UI state or locale into animation files.

## Deployment and cost

Initial delivery can be a static site plus static GLB/JSON assets. There is no reason to provision a database, API, authentication service, or recurring motion-generation service for the display-only scope. Keep asset size modest, cache immutable versioned exports, and measure on target school devices before deciding on compression or a CDN.

## Extension boundary for host integration

Later embedding should use a documented React component or isolated route that receives a catalog URL or catalog object and an optional theme/config object. It must not import SPEX TECH domain models. If cross-origin embedding is chosen, separately review CSP, CORS, accessibility, and sizing. Integration requires a distinct approved change described by `INTEGRATION_PLAN.md`.
