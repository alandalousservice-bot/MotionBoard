# Animation quality and acceptance criteria

These criteria define the first three gallery entries. They are release gates for future assets, not evidence that any animation exists. A qualified Algerian primary physical education reviewer must adapt/confirm pedagogical cues and sign off on each final version.

## Review principles

- Review the final character and final export, not just a source animation or textual description.
- Assess from front, side, and three-quarter views at normal speed and slow motion. Keep the whole body and ground contact visible.
- Check both the movement's observable mechanics and whether it communicates the intended basic motor skill to a primary-school pupil.
- Separate technical correctness from pedagogy. A technically clean animation may still be pedagogically misleading.
- Record reviewer identity/role, date, reviewed asset version, rubric result, required corrections, and approval status in the release record.
- A change to phase timing, balance, contact, limbs, root path, or instruction cue invalidates the affected movement review until reapproved.

## Shared technical acceptance

- Correct character/rig version and matching skeleton binding; no bind-pose pop on start.
- No missing/renamed tracks, unexpected scale/axis changes, mesh separation, visible penetration, severe joint collapse, or flag mirroring.
- Ground plane/contact is visible; feet do not unintentionally slide or pass through the floor.
- No unexplained pauses, jitter, abrupt popping, or incomplete frames.
- Exported clip length and named clip match metadata. Playback, pause, loop (where allowed), and slow motion remain intelligible and stable.
- At least one normal-speed and one slow-motion review are completed. The final movement is understandable from the default three-quarter camera and at front/side review views.
- License/provenance is complete; both technical and pedagogical reviews are approved before catalog publication.

## 1. Walking — `walk_cycle`

**Skill intent:** show a steady basic forward walk with alternating steps and controlled balance.

Acceptance:

- Left and right steps alternate clearly; weight transfers between supporting feet instead of both legs moving as one.
- Stance foot visibly supports the body during its contact portion; swing foot clears the ground sufficiently to avoid obvious dragging.
- Arms counter-swing naturally in opposition to legs without exaggerated shoulder twisting or crossed-body confusion.
- Torso and head remain controlled with age-appropriate, relaxed posture; no excessive bounce or leaning that obscures the gait.
- In-place cycle has matching start/end pose, foot phase, and body height, with no visible loop snap. If traveling, root motion is marked and the endpoint displacement matches the cycle.
- The reviewer confirms that the pace and amplitude read as walking, not running or marching, and that cues are appropriate for the intended grade/age.

## 2. Running — `run_cycle`

**Skill intent:** show a faster locomotion pattern with a clear flight phase and coordinated arm/leg action.

Acceptance:

- Alternating leg drive and opposing arm action are clear; arms remain coordinated and do not become rigid or flap.
- A brief flight phase is visible between foot contacts for the selected running pattern; contact and push-off remain readable in slow motion.
- Trunk inclination, knee lift, and stride are purposeful and balanced without excessive forward pitch or unsafe-looking collapse.
- Contact foot does not slide during stance; no foot clipping through the floor or body parts interpenetrating.
- In-place loop seam is continuous in body pose, foot phase, and vertical trajectory. Root motion is explicit if the character travels.
- The reviewer confirms that the action reads clearly as running and distinguishes it from walking at normal speed.

## 3. Two-foot jump — `jump_two_foot`

**Skill intent:** show a basic vertical jump and controlled two-foot landing.

Acceptance:

- Both feet begin from a stable, balanced stance and participate in a visible preparation/crouch before take-off.
- Take-off is visibly coordinated from both feet; there is no unintended one-foot lead that changes the skill into a hop.
- Flight has clear lift and body control; knees/arms follow an intentional, understandable path and remain within an age-appropriate range.
- Landing uses both feet in a controlled sequence/near-synchronous contact suitable for the rubric, followed by knee/hip flexion to absorb impact and recovery to balance.
- No foot/body floor penetration, sliding at contact, uncontrolled fall, or abrupt reset. The one-shot ends in a stable pose; looping is off by default.
- The reviewer confirms that preparation, two-foot take-off, flight, landing, and recovery are distinct enough for teaching observation.

## Result states

- **Draft:** work exists but has not passed all required checks. Excluded from approved gallery listings.
- **Technical approved:** asset passes technical/export/accessibility and provenance checks; pedagogy may still be pending.
- **Pedagogically approved:** PE reviewer approves movement, intended age range, and cue; technical approval may still be pending.
- **Approved for display:** both approvals are recorded for the exact same immutable asset version and license is cleared.
- **Rejected / changes requested:** not displayed; corrections create a new review candidate.

Do not treat a generated or stock clip as approved merely because its metadata says so; review evidence must identify a real reviewer and version.
