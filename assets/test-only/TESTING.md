# MB-003A animated GLB browser validation

This directory contains development-only fixtures and a switcher for repeatable end-to-end browser checks without an operating-system file chooser. It is only active in Vite development mode. Production builds do not include the `testAsset` loader.

Run `npm ci` and `npm run dev -- --port 4173`, then visit one of:

- `http://127.0.0.1:4173/?testAsset=robot-expressive`
- `http://127.0.0.1:4173/?testAsset=fox`
- `http://127.0.0.1:4173/?testAsset=rigged-simple`

When a test asset query is active, the import panel provides a clearly marked development-only asset selector. Switching it replaces the current GLB in the same React app instance, exercising the normal parsing, viewer replacement, and cleanup path. It does not create a catalog entry or approval status. All sample content is still labeled as an unapproved technical preview.

See [asset attributions, licenses, hashes and clips](README.md) and the task report at `docs/MB-003A_VERIFICATION.md`.
