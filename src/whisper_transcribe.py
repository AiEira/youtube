#!/usr/bin/env python3
"""Whisper audio transcription using faster-whisper.

Usage:
    python3 whisper_transcribe.py <audio_file> [--language LANG] [--model MODEL]

Examples:
    python3 whisper_transcribe.py /tmp/EOvkZPjJUJw.m4a
    python3 whisper_transcribe.py audio.mp3 --language yue --model medium
    python3 whisper_transcribe.py podcast.wav --language en --model large-v3
"""

from faster_whisper import WhisperModel
import argparse, time, sys, os


def main():
    parser = argparse.ArgumentParser(description="Whisper audio transcription")
    parser.add_argument("audio_file", help="Path to audio file (m4a, mp3, wav, etc.)")
    parser.add_argument("--language", default="zh", help="Language code (default: zh)")
    parser.add_argument("--model", default="large-v3", help="Model size (default: large-v3)")
    args = parser.parse_args()

    audio_path = args.audio_file
    if not os.path.exists(audio_path):
        print(f"❌ File not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    out_path = os.path.splitext(audio_path)[0] + ".txt"

    t0 = time.time()
    print(f"Loading {args.model} model...", flush=True)
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    print(f"Model loaded in {time.time()-t0:.0f}s", flush=True)

    t1 = time.time()
    print(f"Transcribing: {audio_path} (language={args.language})...", flush=True)
    segments, info = model.transcribe(audio_path, language=args.language, beam_size=5)
    print(f"Detected: {info.language} (prob={info.language_probability:.2f})", flush=True)

    with open(out_path, "w") as f:
        for seg in segments:
            line = f"[{int(seg.start//60)}:{seg.start%60:04.1f}] {seg.text}\n"
            f.write(line)
            print(line, end="", flush=True)

    elapsed = time.time() - t1
    print(f"\nDone in {elapsed:.0f}s → {out_path}", flush=True)


if __name__ == "__main__":
    main()
