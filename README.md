# Animatic Builder (V1 Prototype)

A lightweight, shot-based animatic builder prototype with a desktop UI.

## Implemented V1-focused capabilities

- Single timeline track (list-based)
- Add clips, reorder shots, and replace media
- Auto shot naming (`shot_010`, `shot_020`, ...)
- Manual rename, trim in/out, and per-shot comments
- Preview panel with shot-name overlay + timecode scrubber
- Save/open project files (`*.animatic.json`)
- MP4 export through `ffmpeg` concat workflow

## Run locally

```bash
python -m animatic_builder
```

Or install as a package and run:

```bash
pip install -e .
animatic-builder
```

## Build an EXE package

This project includes a build script for Windows executable packaging via PyInstaller:

```bash
pip install pyinstaller
python build_exe.py
```

The output executable is created under `dist/AnimaticBuilder/`.

## Notes

- Export requires `ffmpeg` available on `PATH`.
- Replacement preserves shot name, timeline slot, and comment metadata.
