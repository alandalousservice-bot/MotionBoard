# Later integration plan

MotionBoard 3D is a standalone project. No SPEX TECH changes or connections are included in this foundation. Integration is a future, separately scoped decision.

## Intended boundary

If integration is approved later, embed the gallery as an isolated React route or component with a narrow interface:

- Inputs: locale, optional theme, and an approved catalog/asset base URL.
- Outputs: no writes. At most, expose a local selection callback for navigation or display state.
- Data: versioned static motion catalog and approved GLBs, independent of school, lesson, annual-plan, and assessment records.
- Security: no account or student data required for display. Do not add telemetry or cross-app storage by default.

## Readiness conditions

- This audit is reviewed and approved.
- The standalone runtime and supported React major are selected and pinned.
- A real character and at least one real animation pass technical checks, license review, and independent pedagogical review.
- Arabic RTL and accessibility behavior are validated on target browsers/devices.
- Performance, asset hosting, cache invalidation, and offline requirements are agreed.
- SPEX TECH maintainers approve a distinct integration proposal, API boundary, ownership model, and change window.

## Possible integration options

1. **Route/package in the host React app:** preferred when dependency and React versions are compatible. Expose a self-contained component/route and avoid host domain imports.
2. **Isolated static app in an iframe:** use only if dependency isolation is needed. Define origin, CSP, sizing, focus, and message protocol; do not pass student records.
3. **Link to standalone gallery:** lowest coupling and cost; appropriate if embedding creates maintenance or performance burden.

Choose based on the host's actual architecture and operational constraints at that time. Do not create a backend simply to support integration.

## Data that stays out of scope

The gallery does not create, import, update, or publish lesson memos, annual plans, teacher assessments, pupil records, or school workflows. Motor-skill approval remains human-governed and display-only.
