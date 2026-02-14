# Animatic Builder — V1 Core Specification

This document converts the requested core feature list into an implementable V1 scope with clear behavior and acceptance criteria.

## Product Goal

A lightweight, shot-based animatic assembly tool optimized for speed and iterative replacement.

Out of scope for V1:
- Multi-track editing
- Advanced transitions/effects
- Color/audio mixing
- Collaborative workflows

---

## 1) Timeline

### Requirements
- Single video track only.
- Users can drag and drop source video clips into the timeline.
- Users can reorder clips via drag interactions.
- Users can trim clip in/out points by dragging clip edges.
- Users can zoom timeline density to support rough and fine adjustments.

### UX Notes
- Snap playhead to frame boundaries when trimming.
- Keep interactions responsive for quick shot iterations.
- Show clip duration and trimmed duration.

### Acceptance Criteria
- Adding a new clip appends it to the end of the timeline by default.
- Reordering updates shot order immediately and persists on save.
- Trimming updates playback range without mutating original source media.
- Timeline zoom supports at least three practical levels (coarse/normal/fine).

---

## 2) Shot System

### Requirements
- Auto-generate shot names in fixed increments:
  - `shot_010`, `shot_020`, `shot_030`, ...
- Allow manual shot rename per clip.
- Support per-clip comment field.
- Display active shot name on preview.

### UX Notes
- Auto-naming triggers on clip creation.
- Manual rename should preserve uniqueness by warning on duplicates.
- Comment field should be quickly editable (single click or focus).

### Acceptance Criteria
- New clips receive the next available incremented shot ID.
- Manual rename persists across save/reopen.
- Comments persist across save/reopen.
- Preview always shows current shot label during playback/scrub.

---

## 3) Replace Workflow

### Requirements
- Users can replace media by dropping a new clip onto an existing shot.
- Replacement keeps shot metadata and timing context:
  - Shot name
  - Timing (timeline position and trim intent)
  - Comment

### Behavior Details
- Timeline slot is preserved (no reorder side effects).
- If incoming media is shorter than current trim range, clamp trim out to new media length.
- Replacement should be reversible via undo (if undo is present in app shell).

### Acceptance Criteria
- Dropping a clip on an existing shot swaps source media for that shot.
- Shot name, comment, and timeline placement remain unchanged.
- Trim values are preserved when valid; otherwise safely adjusted.

---

## 4) Preview

### Requirements
- Play / pause controls.
- Timeline scrubbing that updates preview frame.
- Visible timecode display.
- Shot name overlay in preview.

### UX Notes
- Scrubbing should remain smooth at typical animatic resolutions.
- Timecode format recommendation: `HH:MM:SS:FF` (or milliseconds fallback).

### Acceptance Criteria
- Playhead movement updates preview continuously.
- Pausing preserves current frame and shot overlay.
- Scrubbing accurately maps to timeline position.

---

## 5) Export

### Requirements
- Export composed timeline to MP4 (H.264).
- Resolution presets:
  - Original
  - 1080p
  - 720p

### UX Notes
- Display export progress and completion/failure feedback.
- Name output file from project name by default.

### Acceptance Criteria
- Export succeeds for valid projects and creates playable MP4.
- Preset selection changes output dimensions as expected.
- Original preset preserves source timeline render size policy.

---

## 6) Project System

### Requirements
- Save project file.
- Reopen project file.
- Persist the following:
  - Shot order
  - Trim data
  - Comments
  - File paths

### Data Model (minimum)
Each shot entry should include:
- Stable shot ID
- Shot name
- Source file path
- Timeline order index
- Trim in/out values
- Comment

### Acceptance Criteria
- Save writes a project file that can be reopened with equivalent state.
- Reopened project restores timeline order, trims, comments, and media references.
- Missing source files are handled gracefully with relink prompts or placeholders.

---

## Suggested V1 Milestones

1. Timeline + playback foundation
2. Shot metadata + naming system
3. Replace workflow
4. Project persistence
5. Export pipeline + presets
6. QA polish (edge cases, file relinking, UX pass)

## V1 Definition of Done

- All section acceptance criteria pass.
- Project files round-trip without data loss for in-scope fields.
- Export produces stable MP4 outputs at all listed presets.
- Core flows (assemble, reorder, trim, replace, preview, save, reopen, export) are usable end-to-end.
