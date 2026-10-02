# MIDI Chord Progression Builder

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
