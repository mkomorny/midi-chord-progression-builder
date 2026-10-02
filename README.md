# MIDI Chord Progression Builder

[![Automated Release](https://img.shields.io/badge/release-automated_batch_pipeline-blue.svg)](https://github.com/mkomorny)
[![Pipeline Execution](https://img.shields.io/badge/dispatched_by-background_script-informational.svg)](https://github.com/mkomorny)

> [!NOTE]
> **Automated Distribution**: This repository was automatically sanitized, packaged, and published via a scheduled background batch staging pipeline. All file bundling, licensing, and repository synchronization were dispatched automatically by an automated release runner.

A programmatic music generation engine that exports professional, humanized Standard MIDI Files (`.mid`, Type 0 and Type 1) with custom harmonic voicings and velocity curves. Compatible with any Digital Audio Workstation (Ableton Live, Logic Pro, FL Studio, Cubase, Reaper).

## Harmonic Voicing Modes

- **Jazz Open Voicing**: Wide intervals spreading roots and color extensions across 2+ octaves for warm, uncluttered harmonic separation.
- **Drop-2 Voicing**: Classic big-band and guitar drop-2 voicing (dropping the second voice from the top down an octave).
- **Close Keyboard Voicing**: Compact, smooth voice-leading minimizing vertical hand movement across changes.
- **Ambient Spread Pad**: Expansive, multi-octave voicing with root doublings and upper-structure tension pads.
- **Root Triads**: Fundamental 3-note diatonic block chords.

## Humanization Features

- **Velocity Dynamics**: Non-linear randomized velocity contours simulating natural pianistic finger strike dynamics.
- **Micro-Timing Humanization**: Subtle millisecond onset jitter preventing mechanical quantization.
- **Strum Delay**: Configurable millisecond roll from lowest to highest note.

## Dependencies

- **Python**: Version 3.8+
- **`mido>=1.2.10`**: Standard MIDI file encoding library

## Instructions

See [INSTRUCTIONS.md](./INSTRUCTIONS.md) for setup and generation commands.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - see the [LICENSE](./LICENSE) file for details.
