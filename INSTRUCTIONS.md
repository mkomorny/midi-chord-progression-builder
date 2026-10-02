# MIDI Chord Progression Builder - Setup & Usage Guide

## Prerequisites
- **Python**: 3.8+

```bash
pip install -r requirements.txt
```

---

## 1. Generating MIDI Files via CLI

Generate a Neo-Soul progression in Drop-2 voicing:
```bash
python scripts/build_midi_clip.py --chords "Fmaj9 Em7 Dm9 Cmaj7" --voicing drop2 --output ./output/neo_soul.mid
```

Generate an Ambient Pad progression with strum roll and humanized velocity:
```bash
python scripts/build_midi_clip.py --chords "Abmaj7 Cm7 Fm9 Dbmaj7#11" --voicing ambient-pad --humanize 0.8 --output ./output/ambient_chords.mid
```

---

## 2. Loading into Your DAW

Drag and drop the generated `.mid` file directly onto any MIDI or software instrument track in Ableton Live, Logic Pro, FL Studio, or Reaper.
