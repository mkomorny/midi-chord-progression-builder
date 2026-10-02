---
name: ableton-midi-chord-builder
description: Generates professional, humanized Type 0/1 MIDI chord progression clips (.mid) with custom voicings (Jazz open, Drop-2, Close, Ambient Pad, Triads) and saves them directly into your Ableton User Library (./output/midi_clips) or project folder. Triggered in chat whenever the user asks to turn chords into MIDI, export an Ableton clip, or create a chord progression file.
---

# Ableton MIDI Chord Builder

Turns chord progressions from chat directly into production-ready, humanized Type 0/1 standard `.mid` clips that appear instantly in your **Ableton Live User Library** (`User Library > Clips > Chord Progressions`).

Whenever the user asks to turn chords into MIDI, create an Ableton clip, or export a chord progression, activate this skill.

---

## When to Activate

Trigger this skill whenever the user says things like:
* *"Turn that chord progression into a MIDI clip for Ableton."*
* *"Make me a 4-bar MIDI file for Dm9 - G13 - Cmaj9 with jazz voicings."*
* *"Export these chords as a MIDI file at 115 BPM."*
* *"Create an ambient pad chord clip for F#m7 - Dmaj7 - Bm9."*
* *"Generate a drop-2 guitar chord progression clip in A minor."*

---

## Voicing Styles Supported

* **`jazz` (Default):** Warm, sophisticated voicing with root bass in octave 2, guide tones (3rd & 7th) in octave 3, and color extensions (9th, 11th, 13th) up top. Ideal for Neo-Soul, Lo-Fi, R&B, and Rhodes.
* **`drop2`:** The second-highest voice is dropped down an octave. Classic lush spread for electric pianos, guitars, and string sections.
* **`pad` / `spread`:** Massive wide spacing with sub-bass, 5th, and airy top extensions. Ideal for ambient pads, synth textures, and cinematic music.
* **`close`:** Compact keyboard inversions. Ideal for synth stabs, arpeggiators, plucks, and EDM.

---

## How to Execute Under the Hood (Silent Agent Workflow)

You do **NOT** ask the user to run scripts in PowerShell. Instead, run the generator invisibly using terminal/bash commands:

```bash
# Standard jazz voicing at 120 BPM into Ableton User Library:
python "<skill_dir>/scripts/build_midi_clip.py" --chords "Dm9,G13,Cmaj9,Am7" --bpm 120 --voicing "jazz"

# Drop-2 guitar voicings at 95 BPM:
python "<skill_dir>/scripts/build_midi_clip.py" --chords "Am9,Fmaj7,Cadd9,G6" --bpm 95 --voicing "drop2"

# Lush ambient synth pad:
python "<skill_dir>/scripts/build_midi_clip.py" --chords "F#m11,Dmaj9,Aadd9,E" --bpm 80 --voicing "pad"
```

The script automatically:
1. Voices each chord musically with voice-leading.
2. Applies micro-timing flam delays (8–15ms) so notes don't hit mechanically at the exact same microsecond.
3. Applies human velocity variance ($\pm 6$ to $\pm 10$).
4. Saves the `.mid` file directly to:  
   `./output/midi_clips\<Chords>_<voicing>.mid`
5. Returns JSON with the full file path and URI.

---

## Chat Presentation Guidelines

When the clip is generated, provide the user with:
1. **The Clickable Ableton Link:**  
   `[Chord_Progression.mid](file:///./output)`
2. **Where to Find It in Ableton:**  
   Remind them: *"This clip is now waiting in your Ableton browser under **User Library → Clips → Chord Progressions**. You can drag it straight onto any synth, piano, or sampler track."*
3. **Clip Details:** List the BPM, bar length, voicing style, and the individual chord notes.
