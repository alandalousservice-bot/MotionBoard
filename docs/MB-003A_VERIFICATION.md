# MB-003A — Animated GLB browser validation

**Date:** 2026-10-16 (Africa/Algiers)  
**Branch:** `mb-003a/animated-glb-validation`  
**Base / START_HEAD:** `mb-002/interactive-viewer` — `08d1e8bd34850377cc46fb2b3ff8d1cb68e32742`  
**End commit:** see the branch tip for this report revision.

## Recommendation

**GO for MB-003A technical viewer validation.** Three legally reusable animated GLBs rendered in the real browser, materials appeared, clips visibly animated, and the requested viewer controls were exercised. This establishes technical loading and interaction for these fixtures only. It does not approve any educational movement or final character, and it does not authorize MB-003B or animation production.

During browser validation, React StrictMode exposed a scene-parent mutation bug that kept parsed GLBs invisible. The viewer now mounts the loaded scene declaratively and leaves GLTF resource cleanup to the app-owned asset lifecycle. The three test fixtures rendered after this change.

## Test asset provenance, license, and facts

The browser used three unmodified, small fixtures with adjacent notices in [`assets/test-only/`](../assets/test-only/). `RobotExpressive.glb` is the primary visual fixture from the three.js examples repository; its source README identifies Tomás Laulhé as model author under CC0 1.0 and describes Don McCurdy's modifications. The [source README](https://github.com/mrdoob/three.js/blob/dev/examples/models/gltf/RobotExpressive/README.md) applies the stated license/credits to the sample. Khronos Fox and RiggedSimple assets use their respective [Fox README and license](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/Fox) and [RiggedSimple README and license](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/RiggedSimple); notices are retained locally. All samples are clearly test-only and are not the MotionBoard schoolboy.

| Asset | Source credits / license | Size / SHA-256 | Clips and durations |
|---|---|---|---|
| `RobotExpressive.glb` | Tomás Laulhé, CC0 1.0; modifications by Don McCurdy (facial-expression morphs, FBX2GLTF conversion, duplicate-material removal and metalness adjustment). Source notice is copied to `RobotExpressive-SOURCE-README.md`. | 463,988 bytes; `047f5e5fb3bb6d378bd1df16ca6137f2a596c99b3a1b5690b4020c05aaf6f319` | `Dance` 3.3333 s; `Death` 0.9583 s; `Idle` 3.3333 s; `Jump` 0.7083 s; `No` 1.6667 s; `Punch` 0.8333 s; `Running` 0.9583 s; `Sitting` 0.4167 s; `Standing` 0.4167 s; `ThumbsUp` 1.5833 s; `Walking` 0.9583 s; `WalkJump` 0.8333 s; `Wave` 1.8333 s; `Yes` 1.6667 s |
| `Fox.glb` | PixelMannen model, CC0 1.0; tomkranis rigging/animation, CC BY 4.0; @AsoboStudio and @scurest conversion, CC BY 4.0. License notice excludes logos/trademarks. | 162,852 bytes; `d97044e701822bac5a62696459b27d7b375aada5de8574ed4362edbba94771f7` | `Survey` 3.4167 s; `Walk` 0.7083 s; `Run` 1.1583 s |
| `RiggedSimple.glb` | Cesium, CC BY 4.0. License notice excludes logos/trademarks. | 15,104 bytes; `3a79dabb67bb0cd598a18d08b954d9d357c27c30672f82ef5d3f4e7fe6ca3401` | `animation_0` 2.0833 s (source clip unnamed; loader supplies name) |

Durations are computed from the maximum input key time in each animation sampler. They are file facts, not movement ratings.

## Reproduction

Requirements: Node.js 20.19+ or 22.12+ and npm. From repository root:

```sh
npm ci
npm run dev -- --port 4173
```

Open one of `http://127.0.0.1:4173/?testAsset=robot-expressive`, `...?testAsset=fox`, or `...?testAsset=rigged-simple`. The dev-only query bootstrap fetches the fixture into a `File` and passes it through the normal GLTF loader. When a query is active, the import panel also shows a clearly labeled development-only selector that replaces the fixture in the same app instance. Production builds omit the query bootstrap and selector. See [`assets/test-only/TESTING.md`](../assets/test-only/TESTING.md).

The normal operating-system file chooser was not validated by automation. For an additional manual check, use the Arabic “اختيار ملف GLB” button with a local GLB.

## Browser setup and evidence

- Browser: Codex in-app Chromium browser; local Vite dev server at `127.0.0.1:4174`.
- Desktop viewport: **1280×720**. Mobile viewport: **390×844** (page content width 375 px due to scrollbar).
- `main` reported `dir="rtl"`; Arabic controls remained visible and usable.
- Browser screenshots were inspected during the run, including RobotExpressive during clip playback, Fox, RiggedSimple, and mobile layout. Images were not saved as repository artifacts.
- Browser console on the final clean reload: no error-level messages or WebGL errors. `THREE.Clock` deprecation warning remains in the installed React Three Fiber / Three.js runtime. The earlier `PCFSoftShadowMap` warning no longer appeared after changing the R3F shadow configuration.
- On mobile, `document.documentElement.scrollWidth` and `clientWidth` both measured 375 px, with `window.innerWidth` 390 px; no horizontal overflow was observed.

## Browser test matrix

PASS means the interaction or result was actually exercised in the browser. Automated unit tests are not substituted for browser evidence.

| Check | Result | Evidence / limit |
|---|---|---|
| Model render and materials | PASS | RobotExpressive, Fox, and RiggedSimple rendered visibly; model materials/colors appeared. |
| Skeletal animation playback | PASS | Robot Dance poses differed in screenshots 0.9 s apart; Walking changed after resume. |
| Play and pause | PASS | Paused Walking and observed the same pose in two captures 800 ms apart; resumed and observed pose change. |
| Restart | PASS | Restart control was activated for selected clips. |
| Loop enabled and disabled | PASS | With loop off, restarted Walking reached and held its terminal pose; with loop on, restarted and observed continued changed poses after the clip duration. |
| Speeds 0.25×, 0.5×, 1× | PASS | Each speed was selected; Jump was observed after 700 ms at each setting and poses/timing differed. |
| Animation selection | PASS | Selected Robot `Walking` and `Jump`, and Fox `Walk` and `Run`; selected names and clip details updated. |
| Camera orbit | PASS | Desktop orbit-pad buttons changed view; mobile pointer drag changed model angle. Continuous full 360-degree orbit was not measured. |
| Camera zoom | PASS | Zoom-in/out buttons and wheel zoom over the stage changed framing. |
| Camera reset | PASS | Reset control used after camera changes and returned framing toward the initial front view. |
| Switch assets in one app instance | PASS | Selector replaced RobotExpressive → Fox → RiggedSimple → RobotExpressive; UI clips updated and one canvas remained mounted. No browser errors appeared during replacements. |
| Resource disposal / leak behavior | PASS (cleanup path), NOT TESTED (soak) | Asset switch exercised the same replacement effect and disposal path; the existing disposal unit tests pass. Heap/GPU memory was not sampled over a long soak, so absence of leaks is not claimed. |
| Arabic RTL | PASS | `dir="rtl"` was verified; Arabic labels and controls displayed. |
| Desktop layout | PASS | Loaded GLB tested at 1280×720. |
| Mobile layout | PASS | Loaded RobotExpressive tested at 390×844; controls and stage remained accessible without horizontal overflow. |
| Normal OS file chooser | NOT TESTED | This automation surface did not expose a usable file-chooser event. Development-only fixture path was used. |
| Browser console / WebGL | PASS with warning | No errors/WebGL failures. `THREE.Clock` deprecation warning remains. |

## Automated verification

These commands were run in the feature branch after the viewer fix:

- `npm run typecheck` — **PASS**.
- `npm run validate` — **PASS**, Draft 2020-12 schemas, 5 tests.
- `npm test` — **PASS**, 6 files and 16 tests.
- `npm run build` — **PASS**, Vite 8.3.4. Largest chunk `Viewer` is 564.72 kB minified / 150.22 kB gzip; Vite emitted its >500 kB advisory. `testAsset` and the development-only selector label are absent from emitted JS; test fixture GLBs are absent from `dist`.

The development-only harness was verified absent from production output (`testAsset` and the selector label do not occur in emitted JS); fixture GLBs were not emitted to `dist`.

## Known limitations

- Test characters and movements are technical fixtures, not the final Algerian schoolboy, PE curriculum content, or pedagogically approved movement demonstrations.
- Actual OS file chooser use and long-duration heap/GPU leak soak were not tested. The app's asset replacement/disposal path was exercised, and helper cleanup is covered by automated tests.
- Full continuous 360-degree camera travel was not measured; orbit input through buttons and a pointer drag was exercised.
- `THREE.Clock` runtime deprecation warning remains. No runtime or browser errors were observed.
- No SPEX TECH files or services were accessed or changed, and no paid service was added.
