#!/usr/bin/env python3
"""
Ableton MIDI Chord Builder
Generates professional, humanized Type 0/1 MIDI files with custom voicings (Jazz, Drop-2, Close, Spread Pad).
Directly saves into Ableton User Library (./output Library\\Clips\\Chord Progressions) or custom project paths.
"""

import os
import sys
import math
import random
import argparse
import json
from pathlib import Path

try:
    import mido
    from mido import Message, MidiFile, MidiTrack, MetaMessage
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mido"])
    import mido
    from mido import Message, MidiFile, MidiTrack, MetaMessage

DEFAULT_OUTPUT_DIR = Path(r"./output/midi_clips")

# MIDI Note mapping
NOTE_TO_SEMITONE = {
    "C": 0, "C#": 1, "DB": 1,
    "D": 2, "D#": 3, "EB": 3,
    "E": 4, "FB": 4, "E#": 5,
    "F": 5, "F#": 6, "GB": 6,
    "G": 7, "G#": 8, "AB": 8,
    "A": 9, "A#": 10, "BB": 10,
    "B": 11, "CB": 11, "B#": 0
}

# Formula intervals (semitones from root)
CHORD_FORMULAS = {
    # Triads
    "maj": [0, 4, 7],
    "": [0, 4, 7],
    "min": [0, 3, 7],
    "m": [0, 3, 7],
    "dim": [0, 3, 6],
    "aug": [0, 4, 8],
    "sus4": [0, 5, 7],
    "sus2": [0, 2, 7],
    
    # 7ths
    "maj7": [0, 4, 7, 11],
    "min7": [0, 3, 7, 10],
    "m7": [0, 3, 7, 10],
    "7": [0, 4, 7, 10],
    "dom7": [0, 4, 7, 10],
    "dim7": [0, 3, 6, 9],
    "m7b5": [0, 3, 6, 10],
    "min7b5": [0, 3, 6, 10],
    "hdim7": [0, 3, 6, 10],
    
    # 6ths & 9ths & Extensions
    "6": [0, 4, 7, 9],
    "maj6": [0, 4, 7, 9],
    "min6": [0, 3, 7, 9],
    "m6": [0, 3, 7, 9],
    "6/9": [0, 4, 7, 9, 14],
    "9": [0, 4, 7, 10, 14],
    "maj9": [0, 4, 7, 11, 14],
    "min9": [0, 3, 7, 10, 14],
    "m9": [0, 3, 7, 10, 14],
    "add9": [0, 4, 7, 14],
    "11": [0, 7, 10, 14, 17],
    "min11": [0, 3, 7, 10, 14, 17],
    "m11": [0, 3, 7, 10, 14, 17],
    "13": [0, 4, 7, 10, 14, 21],
    "maj13": [0, 4, 7, 11, 14, 21],
    "min13": [0, 3, 7, 10, 14, 21],
    "m13": [0, 3, 7, 10, 14, 21],
    
    # Altered Dominants
    "7b9": [0, 4, 7, 10, 13],
    "7#9": [0, 4, 7, 10, 15],
    "7b5": [0, 4, 6, 10],
    "7#5": [0, 4, 8, 10],
    "7alt": [0, 4, 10, 13, 15, 20],
}

def parse_chord(chord_str):
    chord_str = chord_str.strip()
    slash_root = None
    if "/" in chord_str:
        parts = chord_str.split("/")
        chord_str = parts[0].strip()
        slash_root = parts[1].strip().upper()
        
    if len(chord_str) > 1 and chord_str[1] in ["#", "b", "B"]:
        root = chord_str[:2].upper()
        quality = chord_str[2:].lower()
    else:
        root = chord_str[:1].upper()
        quality = chord_str[1:].lower()
        
    # Normalize quality strings
    if quality.startswith(":"):
        quality = quality[1:]
    if quality in ["major"]:
        quality = "maj"
    elif quality in ["minor"]:
        quality = "min"
        
    formula = CHORD_FORMULAS.get(quality, CHORD_FORMULAS.get("maj"))
    root_val = NOTE_TO_SEMITONE.get(root, 0)
    slash_val = NOTE_TO_SEMITONE.get(slash_root) if slash_root else None
    
    return {
        "name": chord_str + (f"/{slash_root}" if slash_root else ""),
        "root": root_val,
        "slash": slash_val,
        "formula": formula
    }

def build_voicing(chord_info, voicing_style="jazz", base_octave=3):
    root_semi = chord_info["root"]
    formula = chord_info["formula"]
    slash = chord_info["slash"]
    
    root_note = (base_octave * 12) + root_semi
    
    if voicing_style == "close":
        # Straight tight chord in octave 3/4
        notes = [root_note + interval for interval in formula]
        if slash is not None:
            bass = (base_octave - 1) * 12 + slash
            notes = [bass] + [n for n in notes if n % 12 != slash]
        return sorted(notes)
        
    elif voicing_style == "jazz" or voicing_style == "open":
        # Low bass in octave 2, guide tones + extensions in octave 3/4
        bass_octave = base_octave - 1 if base_octave > 2 else base_octave
        bass_note = (bass_octave * 12) + (slash if slash is not None else root_semi)
        
        upper_notes = []
        for interval in formula:
            if interval == 0:
                continue # Skip doubling root in close upper structure
            # Place 3rd and 7th in octave 3, extensions in octave 4
            octave_add = 0 if interval < 12 else 12
            upper_notes.append(((base_octave) * 12) + root_semi + interval)
            
        if not upper_notes:
            upper_notes = [root_note + 4, root_note + 7]
            
        return sorted([bass_note] + upper_notes)
        
    elif voicing_style == "drop2":
        # Build 4-note chord, drop 2nd highest note down an octave
        base_notes = [root_note + interval for interval in formula[:4]]
        while len(base_notes) < 4:
            base_notes.append(base_notes[0] + 12)
        base_notes.sort()
        # Drop 2nd from top (index 2) down 12 semitones
        dropped = base_notes[2] - 12
        notes = [dropped, base_notes[0], base_notes[1], base_notes[3]]
        return sorted(notes)
        
    elif voicing_style == "pad" or voicing_style == "spread":
        # Massive wide voicing with sub bass and airy top
        sub_bass = (base_octave - 1) * 12 + (slash if slash is not None else root_semi)
        fifth = sub_bass + 7
        upper = [((base_octave + 1) * 12) + root_semi + interval for interval in formula]
        return sorted([sub_bass, fifth] + upper)
        
    else:
        # Default fallback
        return sorted([root_note + interval for interval in formula])

def create_midi_file(chords_list, out_path, bpm=120, beats_per_chord=4, voicing="jazz", humanize=True):
    mid = MidiFile(type=0, ticks_per_beat=480)
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Set tempo
    tempo = mido.bpm2tempo(bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    track.append(MetaMessage('track_name', name='Chord Progression', time=0))
    
    ticks_per_chord = int(480 * beats_per_chord)
    gate_ratio = 0.94 # Small gap between chords for clean release
    note_duration_ticks = int(ticks_per_chord * gate_ratio)
    rest_ticks = ticks_per_chord - note_duration_ticks
    
    for c_str in chords_list:
        if not c_str.strip():
            continue
        c_info = parse_chord(c_str)
        notes = build_voicing(c_info, voicing_style=voicing)
        
        # Humanize: small strum offset (flam)
        strum_delays = [0]
        if humanize and len(notes) > 1:
            # 8-15 ticks strum spread
            spread = random.randint(8, 16)
            for i in range(1, len(notes)):
                strum_delays.append(strum_delays[-1] + random.randint(3, spread))
        else:
            strum_delays = [0] * len(notes)
            
        # Note Ons
        last_delay = 0
        for i, note in enumerate(notes):
            vel = random.randint(82, 98) if humanize else 90
            delay = strum_delays[i] - last_delay
            track.append(Message('note_on', note=note, velocity=vel, time=delay))
            last_delay = strum_delays[i]
            
        # Note Offs
        total_strum = strum_delays[-1]
        active_duration = max(10, note_duration_ticks - total_strum)
        
        # Turn off first note after active_duration
        first = True
        for note in notes:
            if first:
                track.append(Message('note_off', note=note, velocity=64, time=active_duration))
                first = False
            else:
                track.append(Message('note_off', note=note, velocity=64, time=0))
                
        # Gap before next chord
        track.append(Message('note_off', note=0, velocity=0, time=rest_ticks))
        
    track.append(MetaMessage('end_of_track', time=0))
    
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    mid.save(str(out_file))
    return out_file

def main():
    parser = argparse.ArgumentParser(description="Build Ableton-ready MIDI chord files.")
    parser.add_argument("--chords", required=True, help="Comma-separated chord names (e.g. 'Dm9,G13,Cmaj7')")
    parser.add_argument("--out", default=None, help="Output .mid file path (defaults to User Library)")
    parser.add_argument("--bpm", type=int, default=120, help="Tempo BPM (default 120)")
    parser.add_argument("--beats", type=int, default=4, help="Beats per chord (default 4 = 1 bar)")
    parser.add_argument("--voicing", default="jazz", choices=["jazz", "close", "drop2", "pad", "spread"], help="Voicing style")
    parser.add_argument("--name", default=None, help="Custom filename prefix")
    args = parser.parse_args()
    
    chords = [c.strip() for c in args.chords.replace("->", ",").replace("-", ",").split(",") if c.strip()]
    if not chords:
        print(json.dumps({"error": "No chords provided."}))
        sys.exit(1)
        
    if args.out:
        out_path = Path(args.out)
        if out_path.is_dir() or not out_path.suffix:
            clean_name = "_".join(c.replace("/", "_") for c in chords[:4])
            out_path = out_path / f"{clean_name}_{args.voicing}.mid"
    else:
        clean_name = args.name or "_".join(c.replace("/", "_") for c in chords[:4])
        out_path = DEFAULT_OUTPUT_DIR / f"{clean_name}_{args.voicing}.mid"
        
    saved_file = create_midi_file(
        chords_list=chords,
        out_path=out_path,
        bpm=args.bpm,
        beats_per_chord=args.beats,
        voicing=args.voicing
    )
    
    result = {
        "status": "success",
        "file_path": str(saved_file.resolve()),
        "file_uri": f"file:///{str(saved_file.resolve()).replace(chr(92), '/')}",
        "chords": chords,
        "bpm": args.bpm,
        "beats_per_chord": args.beats,
        "voicing": args.voicing
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
