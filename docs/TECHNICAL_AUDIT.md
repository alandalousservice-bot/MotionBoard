# Technical audit

**Audit date:** 2026-10-16 (Africa/Lagos)
**Repository state at audit:** empty directory; Git initialized for this work on `mb-001/project-foundation`.
**Scope:** Blender, MPFB2, Rokoko Blender integration, Three.js, React Three Fiber, licensing, runtime compatibility, and cost. This is a documentation-based compatibility audit; no software was installed and no integration smoke test was run.

## Repository and asset inventory

- The supplied repository directory contained no source files, package manifest, lockfile, tests, assets, or Git metadata.
- No character, rig, animation, or application exists in this repository.
- The target folder is now a new Git repository with the dedicated branch `mb-001/project-foundation`; no other project folder was changed.
- The initial dependency set is intentionally empty. A lockfile should be introduced only after the technical audit and target React host version are approved.

## Tool assessment

| Tool | Assessment | Compatibility / licensing / limitation |
|---|---|---|
| **Blender** | Recommended as the editable source, rigging, cleanup, export, and review application. | Blender's official releases page lists Blender 4.5 LTS, updated 2026-09-15, as the current LTS at audit time. Blender itself is GPL; this is the software license and should not be mistaken for a blanket license on all assets made with or distributed alongside it. Test the exact version and export settings before production. |
| **MPFB2** | Candidate for rapid base-mesh generation and human proportions, not an automatic final cartoon character solution. | Official MPFB2 README states MPFB 2.x requires Blender 4.2 or newer, so Blender 4.5 LTS meets the stated minimum. Its repository separates code licensing (GPLv3) and asset licensing (CC0 text); still check the exact installed version and each included/downloaded asset pack before redistribution. Stylization, child-safe appearance, uniform, flag, topology, rig, and final web optimization require deliberate art work and review. |
| **Rokoko Blender integration / Studio** | Optional mocap capture/import and retargeting path; not a required dependency. | Official plan page currently lists Starter at $0 and says FBX export is available, while custom-character import/retargeting is a paid feature (Basic or above in listed plans). Its Studio retargeting guide describes the feature as a simple preview-oriented retargeter rather than advanced retargeting. Terms, plan features, plugin compatibility, and price can change. Budget must not assume custom retargeting is free. |
| **Three.js** | Recommended browser runtime foundation for glTF display and animation playback. | Three.js is an MIT-licensed JavaScript 3D library with official glTF loading and `AnimationMixer`; mixer `timeScale` supports speed scaling and zero can pause/unpause. Pin compatible versions once implemented. Requires WebGL-capable browsers/devices, GPU/memory budget, asset optimization, and runtime accessibility around the canvas. |
| **React Three Fiber (R3F)** | Recommended when building the viewer within a React application; use plain Three.js when a framework-independent viewer is a stronger requirement. | Official docs say R3F v8 pairs with React 18 and v9 with React 19; the docs note v10 is alpha at audit time. R3F is an MIT-licensed React renderer. Match the exact R3F major to the host React major; do not adopt an alpha for the first production runtime. |

## Technical limitations and risks

- **Character pipeline risk:** MPFB2 is a generator, not a guaranteed cartoon design or a guarantee that output is suitable for primary-school use. Flag geometry/texture must visibly match the Algerian flag (green and white fields with red crescent and star) and be approved against an authoritative reference.
- **Retargeting risk:** source and destination skeleton proportions, rest pose, bone naming, root motion, scale, axis, and foot contact all affect quality. Retargeted data needs Blender cleanup and visual review on the final character.
- **Mocap quality risk:** video or optical mocap can contain occlusion, jitter, foot sliding, and joint ambiguity. A capture or AI-generated motion is only source material, never pedagogical approval.
- **Web delivery risk:** GLB compatibility can hide unsupported materials, texture color-space errors, wrong forward/up axes, clip name mismatches, or excessive file/memory cost. Test in target browsers and school hardware.
- **Input/accessibility risk:** orbit gestures can conflict with touch scrolling; provide visible keyboard-operable controls and bounded camera behavior. Playback controls must not exist only inside the canvas.
- **Version risk:** Blender add-ons, export plug-ins, npm packages, and external service pricing change. Record exact versions, source commits, and checked dates in the production manifest.
- **Licensing risk:** tool code, generator assets, sample characters, motion libraries, and user-produced output have separate terms. Verify redistribution, commercial/public-education use, modification, attribution, and web embedding rights item by item.

## Recommendation

Proceed with Blender 4.5 LTS + MPFB2 only as an evaluated character-blockout path. Keep Blender source editable. Use a consistent hand-authored or mocap-assisted animation pipeline with Blender retargeting/cleanup and export to GLB. Choose React Three Fiber if the future host is confirmed to use a compatible React major; otherwise use Three.js directly behind a small viewer adapter. Keep Rokoko optional and compare its paid retargeting cost with Blender/manual retargeting before procurement.

Do not begin full production until an authorized reviewer accepts this audit and confirms the target runtime/React major, Blender/add-on versions, tool budget, asset license policy, and pedagogical review owner.

## Verification checklist before implementation

- [ ] Confirm target browsers, device/GPU baseline, offline expectations, and hosting constraints.
- [ ] Identify the target platform's React major before choosing R3F v8/v9; avoid R3F v10 alpha for initial release.
- [ ] Install the selected Blender LTS and exact MPFB2 version in an isolated workstation profile; verify import, rigging, and GLB export with a disposable technical test model.
- [ ] Inspect MPFB2 code and asset license files for the selected release and every used base asset/target.
- [ ] Verify Rokoko plugin install path and supported Blender version; confirm plan entitlements and current cost before any subscription.
- [ ] Import a non-production test GLB in the target browsers and verify animation clips, camera bounds, speed, pause, and cleanup.
- [ ] Review a flag reference and visual design with an Algerian stakeholder before character approval.
- [ ] Name the qualified PE reviewer and agree movement-specific rubrics before animation production.

## Primary sources checked

- [Blender releases](https://www.blender.org/download/releases/) and [Blender license](https://www.blender.org/about/license/)
- [Blender 4.5 manual license page](https://docs.blender.org/manual/en/4.5/copyright.html)
- [MPFB2 repository and compatibility note](https://github.com/makehumancommunity/mpfb2) and [MPFB2 code license](https://github.com/makehumancommunity/mpfb2/blob/master/LICENSE.CODE.md), [asset license](https://github.com/makehumancommunity/mpfb2/blob/master/LICENSE.ASSETS.md)
- [Rokoko pricing and plan features](https://www.rokoko.com/pricing), [Rokoko retargeting guide](https://support.rokoko.com/hc/en-us/articles/14843726304657-Rokoko-Studio-Retargeting-Guide)
- [Three.js documentation](https://threejs.org/docs/), [AnimationMixer](https://threejs.org/docs/pages/AnimationMixer.html), [loading 3D models](https://threejs.org/manual/pages/loading-3d-models.html)
- [Three.js MIT license](https://github.com/mrdoob/three.js/blob/dev/LICENSE)
- [R3F introduction and React compatibility](https://r3f.docs.pmnd.rs/getting-started/introduction), [R3F MIT license](https://github.com/pmndrs/react-three-fiber/blob/master/LICENSE)

Recheck versions, plans, and terms immediately before tool selection or asset acquisition.
