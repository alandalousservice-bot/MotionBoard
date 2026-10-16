# Asset and animation pipeline

This workflow is a proposal for review; production has not started. Full production is blocked until the technical audit is approved.

## Roles and gates

1. **Art direction** approves the character silhouette, age range, uniform colors, and flag reference.
2. **Character artist / technical artist** creates the editable Blender source, skeleton, materials, and web export.
3. **Motion animator** creates or captures movement and cleans/retargets it on the approved production rig.
4. **PE reviewer** checks movement against the agreed learning intent and age-appropriate execution.
5. **Technical reviewer** checks rig/clip integrity, web rendering, performance, metadata, and license provenance.
6. **Content steward** records both approvals and releases an immutable version to the display catalog.

No generated or captured movement is automatically approved or published. Any source motion requires manual cleanup, review, and explicit release.

## Recommended production flow

1. **Lock baseline.** Record Blender, MPFB2 (if used), add-on, export settings, target browser, and source rig version. Keep the first tool trial offline/local.
2. **Create blockout.** Use MPFB2 only as a starting mesh if it meets the approved visual direction. Otherwise use commissioned modeling. Develop one canonical character; don't produce alternate characters before the first is accepted.
3. **Finalize character.** Hand-author uniform, green/red details, and the Algerian flag. Confirm the red crescent and five-point star are correctly oriented and legible at gallery scale. Build a stable humanoid rig with a documented rest pose and forward axis.
4. **Freeze rig contract.** Publish a rig version and a neutral test pose. All movement sources target this rig or use an explicit retarget/cleanup step to it.
5. **Produce movement.** Prefer keyframed animation by an experienced animator for small, precisely defined primary-school skills. Mocap may be used as a reference or base where suitable, with consent and provenance; it is not a pedagogical source of truth.
6. **Retarget and clean.** In Blender, normalize scale, axes, rest pose, root motion, contact timing, joint trajectories, and transitions. Remove sliding, jitter, penetrations, and incorrect limb paths. Review from front, side, and three-quarter views.
7. **Review movement.** Have a qualified Algerian primary PE reviewer review the final motion and its written cue/description. Record reviewer, date, result, comments, and version. Resolve issues and obtain a new approval for changes that affect movement.
8. **Export and validate.** Export GLB with named clips and only required meshes/materials. Verify browser import, clip duration, root trajectory, loop seams where applicable, neutral pose, materials, flag appearance, and device performance.
9. **Release.** Store editable source, export, preview, metadata, provenance, and review record under the same immutable asset version. Add to the catalog only after all gates pass.

## Rig and export contract

- One shared humanoid skeleton for all movement clips in a character release.
- Blender source (`.blend`) is the editable master; `.glb` is the web delivery format.
- Character forward is local **+Y**, up is local **+Z** in the Blender source convention, with transforms applied before export. If this changes, update the contract and revalidate all consumers.
- Define and keep a neutral A-pose rest pose. Do not silently change bone names or rest pose after animation review; issue a new rig version and retarget/re-review affected clips.
- Prefer in-place locomotion cycles for walk/run playback loops; represent traveling distance through documented root-motion metadata or a separate viewer policy. Never mix in-place and root-motion clips without marking the distinction.
- Keep the Algerian flag as a visible, inspectable material/mesh component and verify face/arm placement after skinning.
- Use glTF-supported materials and textures. Keep textures embedded in GLB unless an explicit caching strategy justifies external files.
- Validate clip names, frame rate, duration, bounds, and expected skeleton bindings after every export.

## File and identifier rules

Stable IDs are lowercase kebab-case. Files include semantic ID and version, e.g. `schoolboy-v1.0.0.glb`, `locomotion-walk-v1.0.0.glb` or a combined character bundle named by the agreed packaging strategy. Keep source and delivery files paired. Do not store raw video of children or identifiable personal data in this repository.

Animation clip names in GLB:

- `walk_cycle`
- `run_cycle`
- `jump_two_foot`

Catalog IDs are stable and locale-neutral: `locomotion-walk`, `locomotion-run`, `jump-two-foot`. Display labels and instructions are localized metadata, not embedded in clip names.

## Rights and source tracking

For each source mesh, texture, rig, motion, reference, add-on, and export, record author/source URL, exact license/terms/version, attribution requirement, modifications, allowed commercial/educational use, allowed redistribution and web embedding, and proof/date of verification. For mocap capture, also record capture method and consent or other lawful basis without retaining unnecessary personal data. A purchased or free motion asset is not cleared for web redistribution until its license expressly allows that use.
