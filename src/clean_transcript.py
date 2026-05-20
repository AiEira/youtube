#!/usr/bin/env python3
"""
Whisper 幻覺清洗器

Reads mlx_whisper JSON output, removes hallucination segments,
writes clean JSON.

四條清洗規則（靈感來自 56% 幻覺率實戰）:

  1. EMPTY:    segment text 為空白（沉默幻覺）
  2. FILLER:   segment 只含填充詞（Yeah. Yeah. Yeah. ...）
  3. DUPLICATE: 與前一保留 segment 文本完全相同（循環幻覺）
  4. LOOP:     同一 2-5 詞短語在 segment 內重複 ≥4 次（回音室幻覺）

Usage:
    python3 clean_transcript.py <input.json> [--output clean.json] [--stats]

Examples:
    python3 clean_transcript.py out/transcripts/6fr8Zzmwi5k.json
    python3 clean_transcript.py in.json --output out/clean.json --stats
"""

import argparse
import json
import os
import re
import sys
from collections import Counter


# ── 填充詞詞典 ──────────────────────────────────────────────
# 這些詞本身不是錯誤，但若整個 segment 只有它們，就是 hallucination。

FILLER_WORDS = {
    "yeah", "yeah.", "yeah!", "yeah,",
    "um", "um,", "uh", "uh,",
    "like", "like,",
    "you know", "you know,",
    "mm", "mm-hmm", "hmm",
    "oh", "oh,", "ah", "ah,",
    "right", "right.", "okay", "okay.",
    "yes", "yes.", "no", "no.",
    "so", "so,", "well", "well,",
    "and", "and,", "but", "but,",
    "i", "i,",   # 孤立 "I" 常出現在重疊對話幻覺
    "it", "it,",
    "the", "the,",
    "a", "a,",
    "to", "to,",
    "of", "of,",
    "in", "in,",
    "that", "that,",
    "is", "is,",
    "was", "was,",
    "it's", "it's,",
    "that's", "that's,",
    "yeah yeah",
    "okay okay",
    "right right",
}


def is_filler_only(text: str) -> bool:
    """True if text consists entirely of filler words/characters."""
    # Strip punctuation, normalize whitespace
    cleaned = text.strip().lower()
    if not cleaned:
        return True  # caught by EMPTY rule, but safe
    # Split on whitespace and commas
    tokens = [t.strip(".,!?;:") for t in re.split(r'[\s,]+', cleaned) if t.strip(".,!?;:")]
    if not tokens:
        return True
    return all(t in FILLER_WORDS for t in tokens)


def has_loop(text: str, threshold: int = 4, phrase_len_min: int = 2,
             phrase_len_max: int = 5) -> bool:
    """True if any 2-5 word phrase appears >= threshold times in text.

    This catches the "they're like you know they're like you know..."
    pattern — a phrase stuck on repeat inside a single segment.
    """
    words = text.strip().lower().split()
    if len(words) < threshold * phrase_len_min:
        return False

    # Slide window, count phrase occurrences
    for n in range(phrase_len_min, phrase_len_max + 1):
        phrases = {}
        for i in range(len(words) - n + 1):
            phrase = " ".join(words[i:i+n])
            phrases[phrase] = phrases.get(phrase, 0) + 1
        if any(c >= threshold for c in phrases.values()):
            return True

    return False


def clean_segments(segments: list, verbose: bool = False) -> tuple:
    """Apply cleaning rules. Returns (clean_segments, stats_dict)."""
    stats = {
        "input_count": len(segments),
        "removed_empty": 0,
        "removed_filler": 0,
        "removed_duplicate": 0,
        "removed_loop": 0,
    }

    clean = []
    last_text = None

    for seg in segments:
        text = seg.get("text", "").strip()

        # Rule 1: EMPTY
        if not text:
            stats["removed_empty"] += 1
            continue

        # Rule 2: FILLER ONLY
        if is_filler_only(text):
            stats["removed_filler"] += 1
            continue

        # Rule 3: DUPLICATE (identical to previous KEPT segment)
        if text == last_text:
            stats["removed_duplicate"] += 1
            continue

        # Rule 4: LOOP (same phrase repeated >=4 times)
        if has_loop(text):
            stats["removed_loop"] += 1
            continue

        # Passed all checks — KEEP
        clean.append(seg)
        last_text = text

    stats["output_count"] = len(clean)
    stats["removed_total"] = stats["input_count"] - stats["output_count"]
    stats["removal_pct"] = round(
        100 * stats["removed_total"] / max(stats["input_count"], 1), 1
    )

    return clean, stats


def main():
    parser = argparse.ArgumentParser(
        description="Clean whisper hallucination segments from JSON transcript"
    )
    parser.add_argument("input_json", help="mlx_whisper JSON output")
    parser.add_argument("--output", "-o", default=None,
                        help="Output path (default: input_clean.json)")
    parser.add_argument("--stats", "-s", action="store_true",
                        help="Print cleaning statistics")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only print stats, don't write output")
    args = parser.parse_args()

    if not os.path.exists(args.input_json):
        print(f"❌ File not found: {args.input_json}", file=sys.stderr)
        sys.exit(1)

    with open(args.input_json) as f:
        data = json.load(f)

    segments = data.get("segments", [])
    if not segments:
        print("⚠️  No segments found in input", file=sys.stderr)
        sys.exit(1)

    clean, stats = clean_segments(segments, verbose=args.stats)

    if args.stats or args.dry_run:
        print(f"Input:   {stats['input_count']} segments")
        print(f"  Empty:     -{stats['removed_empty']}")
        print(f"  Filler:    -{stats['removed_filler']}")
        print(f"  Duplicate: -{stats['removed_duplicate']}")
        print(f"  Loop:      -{stats['removed_loop']}")
        print(f"  ─────────────────────")
        print(f"Output:  {stats['output_count']} segments "
              f"({stats['removal_pct']}% removed)")

    if args.dry_run:
        return

    output_path = args.output
    if not output_path:
        stem = os.path.splitext(args.input_json)[0]
        output_path = f"{stem}_clean.json"

    output_data = {
        "text": " ".join(s["text"].strip() for s in clean),
        "segments": clean,
        "language": data.get("language", "unknown"),
        "_cleaned": {
            "source": args.input_json,
            "rules": ["empty", "filler", "duplicate", "loop"],
            "stats": stats,
        },
    }

    with open(output_path, "w") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Clean transcript → {output_path}")
    print(f"   {stats['input_count']} → {stats['output_count']} "
          f"({stats['removal_pct']}% removed)")


if __name__ == "__main__":
    main()
