# Development conventions

These rules apply throughout this repository.

## Product scope

- Keep MotionBoard 3D standalone and display-only.
- Do not connect it to SPEX TECH, lesson memos, annual plans, or assessment documents without a separately approved integration plan.
- Do not generate, infer, or publish motor skills automatically.
- Arabic is the primary interface language; implement semantic RTL layout and test Arabic text, numerals, mixed Latin identifiers, and keyboard focus.
- Keep user-facing movement language clear and suitable for primary-school pupils and teachers.

## Truth and review

- Never claim an asset exists unless the file is present and has passed its documented checks.
- Never label a generated, stock, mocap-retargeted, or illustrative clip pedagogically correct without a named qualified reviewer and recorded approval.
- Mark unreviewed work as draft. Keep review status and evidence in metadata.
- A technical approval does not imply pedagogical approval; both gates are required for publication in the gallery.
- Do not begin full character or animation production until the technical audit is reviewed and approved.

## Assets and licensing

- Record source, creator, license identifier, attribution, modifications, and redistribution/embedding rights for every external asset and tool-produced asset.
- Verify terms for the exact model, texture, motion clip, plugin, and version; a tool's open-source license does not automatically license its output or downloaded content.
- Do not commit assets with unclear provenance or incompatible redistribution rights.
- Keep editable source files alongside delivery exports when rights permit. Never overwrite a reviewed release; issue a new version.

## Code and content conventions

- Keep UI, scene/viewer runtime, catalog data, and asset loading separated as described in `docs/ARCHITECTURE.md`.
- Use TypeScript for future web code. Keep dependencies explicit and pinned in a lockfile after runtime approval.
- Prefer standard glTF 2.0/GLB for web delivery; retain Blender source as the editable master.
- Use stable kebab-case asset IDs and the animation clip names in `docs/CHARACTER_SPEC.md`.
- Metadata must validate against the schemas in `schemas/`. Unknown schema fields should be rejected unless the schema is deliberately versioned.
- Keep personal data out of the app and asset metadata. Do not add analytics by default.

## Changes and verification

- Make focused changes and describe user-visible or content-facing effects in the change summary.
- Do not add an asset or code dependency without checking license, current maintenance, compatibility, and delivery impact.
- Document verification commands with the change. A successful technical check does not certify movement quality.
- Before publishing a skill, require technical asset checks, Arabic/RTL UI checks, and named pedagogical sign-off.
