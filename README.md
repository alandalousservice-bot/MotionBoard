# MotionBoard 3D

Standalone, display-only 3D motor-skills gallery for Algerian primary physical education. This repository is an isolated foundation for possible later integration into SPEX TECH; it does not modify or depend on that platform.

## Current status

This is a documentation and structure foundation only. There is no character, rig, animation, application runtime, or production asset in the repository. Walking, running, and two-foot jumping are defined as acceptance targets, not completed content. Do not describe them as available until approved assets are checked in or referenced through a verified asset package.

Full 3D production is gated on review and approval of [the technical audit](docs/TECHNICAL_AUDIT.md).

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

## Development and verification

No app dependencies or package manager are selected in this foundation commit. Review [the technical audit](docs/TECHNICAL_AUDIT.md), then approve a runtime and dependency lock before implementing the viewer.

For this documentation-only foundation:

1. Confirm the branch is `mb-001/project-foundation` and inspect `git status`.
2. Validate both schemas with a Draft 2020-12 JSON Schema validator.
3. Review every official-source link and recheck current versions and terms before adopting a tool or asset.
4. Follow the manual acceptance checklist in [animation quality](docs/ANIMATION_QUALITY.md) when real assets exist.

When a web runtime is approved, add reproducible install/build commands and automated checks in the same change as the app. Do not treat schema validation or a successful build as evidence of pedagogical correctness.

## Key documents

- [Architecture](docs/ARCHITECTURE.md)
- [Technical audit](docs/TECHNICAL_AUDIT.md)
- [Asset pipeline](docs/ASSET_PIPELINE.md)
- [Character specification](docs/CHARACTER_SPEC.md)
- [Animation quality and acceptance](docs/ANIMATION_QUALITY.md)
- [Integration plan](docs/INTEGRATION_PLAN.md)
- [Development conventions](AGENTS.md)
