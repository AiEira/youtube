#!/usr/bin/env python3
"""
Whisper 轉錄 — macOS Apple Silicon GPU (mlx_whisper)

Usage:
    python3 whisper_transcribe.py <audio_file> [--language LANG] [--output-dir DIR]

Examples:
    python3 whisper_transcribe.py /tmp/6fr8Zzmwi5k.m4a
    python3 whisper_transcribe.py audio.m4a --language en --output-dir out/transcripts/

Output:
    {output_dir}/{basename}.json — full mlx_whisper output (text, segments, language)

Dependencies:
    mlx_whisper (installed in Hermes venv — Apple Silicon only)
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


MLX_WHISPER_BIN = os.path.expanduser(
    "~/.hermes/hermes-agent/venv/bin/mlx_whisper"
)
DEFAULT_MODEL = "mlx-community/whisper-large-v3-mlx"


def main():
    parser = argparse.ArgumentParser(description="mlx_whisper transcription")
    parser.add_argument("audio_file", help="Path to audio file (m4a, mp3, wav, etc.)")
    parser.add_argument("--language", default=None,
                        help="Language code (auto-detect if omitted)")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: same as audio file)")
    args = parser.parse_args()

    audio_path = args.audio_file
    if not os.path.exists(audio_path):
        print(f"❌ File not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(MLX_WHISPER_BIN):
        print(f"❌ mlx_whisper not found at {MLX_WHISPER_BIN}", file=sys.stderr)
        print("   Install: pip install mlx-whisper", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    audio_stem = Path(audio_path).stem
    output_dir = args.output_dir or str(Path(audio_path).parent)
    os.makedirs(output_dir, exist_ok=True)
    out_json = os.path.join(output_dir, f"{audio_stem}.json")

    # Build command
    cmd = [
        MLX_WHISPER_BIN,
        audio_path,
        "--model", args.model,
        "--output-dir", output_dir,
        "--output-format", "json",
    ]
    if args.language:
        cmd += ["--language", args.language]

    print(f"Transcribing: {audio_path}", flush=True)
    print(f"  Model:   {args.model}", flush=True)
    print(f"  Language: {args.language or 'auto-detect'}", flush=True)
    print(f"  Output:  {out_json}", flush=True)

    t0 = time.time()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=7200,  # 2 hour max
    )

    elapsed = time.time() - t0

    if result.returncode != 0:
        print(f"❌ mlx_whisper failed (exit {result.returncode})", file=sys.stderr)
        if result.stderr:
            print(result.stderr[:2000], file=sys.stderr)
        sys.exit(1)

    # mlx_whisper puts some info on stderr; show last few lines for timing
    stderr_lines = result.stderr.strip().split("\n")
    for line in stderr_lines[-5:]:
        print(f"  [mlx] {line}", flush=True)

    print(f"\n✅ Done in {elapsed:.0f}s ({elapsed/60:.1f}m) → {out_json}", flush=True)

    # Quick stats
    import json
    with open(out_json) as f:
        data = json.load(f)
    n_segs = len(data.get("segments", []))
    duration_min = data["segments"][-1]["end"] / 60 if n_segs else 0
    lang = data.get("language", "unknown")
    speedup = elapsed / max(duration_min * 60, 1)

    print(f"  Segments: {n_segs}  Duration: {duration_min:.0f} min  "
          f"Lang: {lang}  Speed: {speedup:.1f}x realtime", flush=True)


if __name__ == "__main__":
    main()
