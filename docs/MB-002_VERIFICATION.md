# MB-002 verification report

**Date:** 2026-10-16 (Africa/Lagos)  
**Branch:** `mb-002/interactive-viewer`  
**Foundation start:** `05ce09ff3be63ead3ee15ed6d35044ebf5187826` (`mb-001/project-foundation`, published to `origin`)  
**End commit:** see the branch tip for this report revision.

## Result

The standalone React/TypeScript viewer builds and starts locally. The Arabic RTL shell has an honest empty state and can accept a user-selected local GLB and optional schema-validated JSON metadata. Playback, camera controls, state transitions, metadata validation, and resource cleanup have automated coverage. No model, character, animation, or test asset is included in the repository.

## Verification performed

- `npm run typecheck` — passed.
- `npm run validate:schemas` — passed; 5 tests compile/check the existing Draft 2020-12 schemas and metadata behavior.
- `npm test` — passed; 6 test files, 16 tests.
- `npm run build` — passed with Vite 8.3.4.
- `npm run dev -- --port 4173` — started at `http://127.0.0.1:4173/`; empty-state UI reviewed at desktop (1365×900) and narrow mobile (390×844) viewports.
- Build emits a chunk-size advisory: the lazy `Viewer` chunk is 564.55 kB minified (150.16 kB gzip). This does not fail the build; optimize further against actual target hardware and representative production assets.

## Scope limits and remaining checks

- This is a viewer implementation, not a delivered content library. No final schoolboy, rig, walking/running/jumping clip, or approved educational movement exists here.
- A temporary, self-created static triangle GLB was prepared for an attempted local parser smoke check and removed before commit. It was not an animation, educational asset, or product deliverable. Automated GLTF-loader handling is covered with mocks; a representative licensed animated GLB still needs an end-to-end browser check for decoding, clip switching, rendering, orbit, zoom, and GPU cleanup.
- Pedagogical review and visual approval of the Algerian uniform/flag require their designated human reviewers and production assets.
- The build was run on Node.js 24.19.0. Test on the intended school browser/device and WebGL hardware before deployment.
- No SPEX TECH files or services were changed or contacted. No backend or hosting service is required by this demo.

## Reproduction

From the repository root, run `npm ci`, then `npm run dev`. Run `npm run typecheck`, `npm run validate:schemas`, `npm test`, and `npm run build` for the checks above. The GLB picker accepts a self-contained `.glb`; no upload endpoint exists.
