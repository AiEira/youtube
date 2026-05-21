#!/usr/bin/env python3
"""
YouTube Transcript Downloader
Usage:
  python3 src/download-transcript.py <youtube-url>
  python3 src/download-transcript.py <youtube-url> -o out/
  python3 src/download-transcript.py <youtube-url> -f blog
"""

import argparse
import os
import re
import sys
import time
import urllib.request
import json
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi


# Language priority: yue → zh-Hant → zh → zh-Hans → en
LANG_ORDER = ['yue', 'zh-Hant', 'zh', 'zh-Hans', 'en']
ZH_HANT = 'zh-Hant'


def extract_video_id(url_or_id: str) -> str:
    """Extract 11-char video ID from YouTube URL or return raw ID."""
    patterns = [
        r'youtube\.com/watch\?v=([A-Za-z0-9_-]{11})',
        r'youtu\.be/([A-Za-z0-9_-]{11})',
        r'youtube\.com/embed/([A-Za-z0-9_-]{11})',
        r'youtube\.com/shorts/([A-Za-z0-9_-]{11})',
        r'youtube\.com/live/([A-Za-z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    if re.match(r'^[A-Za-z0-9_-]{11}$', url_or_id):
        return url_or_id
    raise ValueError(f"無法從輸入提取 video ID: {url_or_id}")


def get_video_title(video_id: str) -> str:
    """Fetch video title from YouTube oembed."""
    url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json'
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get('title', video_id)
    except Exception:
        return video_id


def sanitize_filename(text: str, max_len: int = 20) -> str:
    """Convert title to filename-safe short form (keep first N chars)."""
    cleaned = re.sub(r'[^\w\u4e00-\u9fff-]', '', text.replace(' ', '-'))
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len]
    return cleaned or 'transcript'


def fetch_transcript_with_fallback(api, video_id: str, languages: list):
    """Fetch transcript; if English fetched, also try zh-Hant translation."""
    transcript = api.fetch(video_id, languages=languages)
    detected_lang = _detect_language(transcript)
    translation = None

    # If we got English, try to get zh-Hant translation
    if detected_lang == 'en':
        try:
            time.sleep(0.5)  # Small delay to avoid IP block
            tlist = api.list(video_id)
            en_track = tlist.find_transcript(['en'])
            if en_track.is_translatable:
                zh_track = en_track.translate(ZH_HANT)
                translation = zh_track.fetch()
            else:
                print('   ⚠️  此影片不支援翻譯', file=sys.stderr)
        except Exception as e:
            print(f'   ⚠️  無法取得繁體中文翻譯: {e}', file=sys.stderr)

    return transcript, detected_lang, translation


def _detect_language(transcript) -> str:
    """Guess language from first snippet text."""
    if not transcript:
        return 'unknown'
    text = transcript[0].text
    has_cjk = any('\u4e00' <= c <= '\u9fff' for c in text)
    if has_cjk:
        # Try to distinguish yue vs zh
        # Simplified has chars like 么/们/实/东/国
        simp_markers = set('么们实东国开关张机')
        has_simp = any(c in text for c in simp_markers)
        return 'zh-Hans' if has_simp else 'zh-Hant'  # default to zh-Hant if unsure
    return 'en'


def format_blog(title: str, video_id: str, url: str, transcript: list,
                detected_lang: str = 'zh', translation: list = None) -> str:
    """Format transcript as markdown. Raw transcript in collapsible section at bottom."""
    lines = [
        f'# {title}',
        '',
        f'> 來源：[YouTube]({url})',
        f'> 長度：約 {int(transcript[-1].start + transcript[-1].duration) // 60} 分鐘',
    ]

    if translation:
        lines.append(f'> 語言：英文 + 繁體中文翻譯')
    elif detected_lang == 'en':
        lines.append(f'> 語言：英文')
    elif detected_lang.startswith('zh'):
        lines.append(f'> 語言：粵語／中文')

    lines += [
        f'> 整理：AiEira',
        '',
        '---',
        '',
        '<!-- BLOG_REWRITE_PLACEHOLDER: LLM will insert rewritten blog here -->',
        '',
        '---',
        '',
        '## 全文逐字稿',
        '',
        '<details>',
        '<summary>展開逐字稿（共 {} 片段）</summary>'.format(len(transcript)),
        '',
    ]

    if translation:
        lines.append('### 英文原文')
        lines.append('')
        for s in transcript:
            lines.append(s.text)
            lines.append('')
        lines.append('### 繁體中文翻譯')
        lines.append('')
        for s in translation:
            lines.append(s.text)
            lines.append('')
    else:
        for s in transcript:
            lines.append(s.text)
            lines.append('')

    lines += [
        '',
        '</details>',
    ]

    return '\n'.join(lines)


def format_timestamps(transcript: list) -> str:
    """Format transcript with timestamps."""
    lines = []
    for s in transcript:
        ts = f"[{int(s.start // 60):02d}:{int(s.start % 60):02d}]"
        lines.append(f'{ts} {s.text}')
    return '\n'.join(lines)


def format_raw(transcript: list) -> str:
    """Plain text, no timestamps."""
    return '\n'.join(s.text for s in transcript)


def format_summary(title: str, url: str, transcript: list,
                   detected_lang: str = 'zh', translation: list = None) -> str:
    """Basic summary format."""
    total_sec = transcript[-1].start + transcript[-1].duration
    lines = [
        f'# {title}',
        '',
        f'來源：{url}',
        f'長度：約 {int(total_sec // 60)} 分鐘',
        f'片段數：{len(transcript)}',
        '',
        '---',
        '',
        '> ⚠️ 摘要格式需要 LLM 處理。目前提供 raw 全文，可用 Claude/GPT 生成摘要。',
        '',
        '## 前 500 字預覽',
        '',
    ]
    preview = transcript[:15]
    for s in preview:
        lines.append(s.text)
    lines.append('')
    lines.append('...')
    return '\n'.join(lines)


def format_chapters(transcript: list) -> str:
    """Generate timestamp-based chapter markers (every ~3 minutes)."""
    lines = ['## 章節（依時間自動分段）', '']
    chunk_sec = 180
    total_sec = transcript[-1].start + transcript[-1].duration
    for t in range(0, int(total_sec), chunk_sec):
        preview = ''
        for s in transcript:
            if s.start >= t:
                preview = s.text[:60]
                break
        ts = f'{t // 60:02d}:{t % 60:02d}'
        lines.append(f'- **{ts}** — {preview}...')
    return '\n'.join(lines)


FORMATTERS = {
    'blog': format_blog,
    'raw': format_raw,
    'timestamps': format_timestamps,
    'summary': format_summary,
    'chapters': format_chapters,
}


def main():
    parser = argparse.ArgumentParser(
        description='下載 YouTube 影片逐字稿',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
格式說明:
  blog       — 全文逐字稿（預設；英文自動附 zh-Hant 翻譯）
  raw        — 純文字，無時間戳
  timestamps — 每行附時間戳 [MM:SS]
  summary    — 摘要預覽
  chapters   — 依時間自動分段

語言次序: yue → zh-Hant → zh → zh-Hans → en（en 自動加繁體翻譯）

範例:
  python3 src/download-transcript.py https://youtube.com/watch?v=VIDEO_ID
  python3 src/download-transcript.py VIDEO_ID -f timestamps
  python3 src/download-transcript.py https://youtu.be/VIDEO_ID -o out/
        """
    )
    parser.add_argument('url', help='YouTube URL 或 video ID')
    parser.add_argument('-o', '--out', default='out', help='輸出目錄（預設: out/）')
    parser.add_argument('-f', '--format', default='blog',
                        choices=list(FORMATTERS.keys()),
                        help='輸出格式（預設: blog）')
    parser.add_argument('-l', '--language', default=','.join(LANG_ORDER),
                        help=f'語言偏好（預設: {",".join(LANG_ORDER)}）')
    parser.add_argument('-t', '--title', default=None,
                        help='自訂標題（預設: 自動從 YouTube 取得）')
    parser.add_argument('--no-translate', action='store_true',
                        help='停用英文→繁體中文自動翻譯')
    args = parser.parse_args()

    # Extract video ID
    try:
        video_id = extract_video_id(args.url)
    except ValueError as e:
        print(f'❌ {e}', file=sys.stderr)
        sys.exit(1)

    # Parse languages
    languages = [l.strip() for l in args.language.split(',') if l.strip()]

    # Fetch transcript
    api = YouTubeTranscriptApi()

    if args.no_translate:
        try:
            transcript = api.fetch(video_id, languages=languages)
        except Exception as e:
            print(f'❌ 無法取得逐字稿: {e}', file=sys.stderr)
            sys.exit(1)
        detected_lang = _detect_language(transcript)
        translation = None
    else:
        try:
            transcript, detected_lang, translation = fetch_transcript_with_fallback(
                api, video_id, languages
            )
        except Exception as e:
            print(f'❌ 無法取得逐字稿: {e}', file=sys.stderr)
            sys.exit(1)

    if not transcript:
        print('❌ 逐字稿為空', file=sys.stderr)
        sys.exit(1)

    # Get title
    title = args.title or get_video_title(video_id)

    # Build URL
    url = f'https://www.youtube.com/watch?v={video_id}'

    # Generate output
    formatter = FORMATTERS[args.format]
    if args.format in ('blog', 'summary'):
        content = formatter(title, video_id, url, transcript,
                          detected_lang=detected_lang, translation=translation)
    else:
        content = formatter(transcript)

    # Build output path
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    short_title = sanitize_filename(title)
    filename = f'{video_id}-{short_title}.md'
    out_path = out_dir / filename

    out_path.write_text(content, encoding='utf-8')

    # Summary
    duration_min = int(transcript[-1].start + transcript[-1].duration) // 60
    lang_info = detected_lang
    if translation:
        lang_info += '+zh-Hant'
    print(f'✅ 已儲存: {out_path}')
    print(f'   [{args.format}] {len(transcript)} 片段 · ~{duration_min} 分鐘')
    print(f'   語言: {lang_info} · {len(content)} 字元')


if __name__ == '__main__':
    main()
