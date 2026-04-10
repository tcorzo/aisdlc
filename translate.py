#!/usr/bin/env python3
"""
translate_to_english.py
Translates all non-English text content in a repository to English
using free translation services (deep-translator / Google Translate).
Usage:
    pip install deep-translator
    python3 scripts/translate_to_english.py [--dir PATH] [--dry-run]
Options:
    --dir PATH      Root directory to process (default: current directory)
    --dry-run       Preview which files would be translated without modifying them
    --service NAME  Translation service: google (default) | mymemory | libre
    --source LANG   Source language code (default: auto)
"""
import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path
# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
NON_ENGLISH_PATTERN = re.compile(
    r"[\u4e00-\u9fff"   # CJK Unified Ideographs (Chinese)
    r"\u3040-\u309f"    # Hiragana (Japanese)
    r"\u30a0-\u30ff"    # Katakana (Japanese)
    r"\uac00-\ud7af"    # Hangul Syllables (Korean)
    r"\u0600-\u06ff]"   # Arabic
)
SKIP_EXTENSIONS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".zip", ".tar", ".gz", ".bz2", ".7z",
    ".ttf", ".woff", ".woff2", ".eot",
    ".mp3", ".mp4", ".avi", ".mov",
    ".pyc", ".exe", ".bin", ".so", ".dll",
}
# i18n-specific file patterns to preserve (do not translate)
I18N_PATTERNS = [
    re.compile(r"\.zh(-CN|-TW|-HK)?\."),   # e.g. SKILL.zh-CN.md
    re.compile(r"_zh(-CN|-TW|-HK)?\b"),     # e.g. templates_zh.md
    re.compile(r"/i18n/"),
    re.compile(r"/locales?/"),
    re.compile(r"/translations?/"),
]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
MAX_TRANSLATE_CHUNK = 4800  # characters per API request
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def has_non_english(text: str) -> bool:
    return bool(NON_ENGLISH_PATTERN.search(text))
def is_i18n_file(path: str) -> bool:
    return any(p.search(path) for p in I18N_PATTERNS)
def slugify_filename(name: str) -> str:
    """Convert a CJK filename to a romanised slug."""
    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source="auto", target="en").translate(name)
    except Exception:
        translated = name
    # keep only alphanumeric, hyphens, dots
    slug = re.sub(r"[^\w\-.]", "-", translated.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug
def get_translator(service: str, source: str):
    """Return a callable(text) -> translated_text."""
    try:
        from deep_translator import GoogleTranslator, MyMemoryTranslator, LibreTranslator
    except ImportError:
        print("ERROR: deep-translator not installed. Run: pip install deep-translator")
        sys.exit(1)
    if service == "google":
        t = GoogleTranslator(source=source, target="en")
        return t.translate
    elif service == "mymemory":
        t = MyMemoryTranslator(source=source if source != "auto" else "zh-CN", target="en-US")
        return t.translate
    elif service == "libre":
        t = LibreTranslator(source=source if source != "auto" else "zh", target="en",
                            url="https://libretranslate.com/")
        return t.translate
    else:
        raise ValueError(f"Unknown service: {service}")
# ---------------------------------------------------------------------------
# Markdown-aware translation
# ---------------------------------------------------------------------------
# Tokens that should NOT be translated
_CODE_BLOCK = re.compile(r"(```[\s\S]*?```|`[^`\n]+`)", re.MULTILINE)
_FRONTMATTER = re.compile(r"^(---\n[\s\S]*?\n---\n?)", re.MULTILINE)
_URL = re.compile(r"https?://\S+")
_MARKDOWN_LINK_REF = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
_HTML_TAG = re.compile(r"<[^>]+>")
def _split_translatable(text: str):
    """
    Split markdown text into (translatable, raw) segments.
    Returns list of (segment, is_raw) tuples.
    """
    # Build a list of protected regions using all non-translatable patterns
    protected_ranges: list[tuple[int, int]] = []
    for pattern in (_CODE_BLOCK, _URL, _HTML_TAG):
        for m in pattern.finditer(text):
            protected_ranges.append((m.start(), m.end()))
    # Merge overlapping ranges
    protected_ranges.sort()
    merged: list[tuple[int, int]] = []
    for s, e in protected_ranges:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    segments = []
    pos = 0
    for s, e in merged:
        if pos < s:
            segments.append((text[pos:s], False))   # translatable
        segments.append((text[s:e], True))           # raw
        pos = e
    if pos < len(text):
        segments.append((text[pos:], False))
    return segments
def translate_text(text: str, translate_fn) -> str:
    """Translate a block of text, protecting code/URLs."""
    if not has_non_english(text):
        return text
    segments = _split_translatable(text)
    result = []
    for segment, is_raw in segments:
        if is_raw or not has_non_english(segment):
            result.append(segment)
            continue
        # Translate in chunks to stay within API limits
        chunk_result = []
        for chunk in _chunked(segment, MAX_TRANSLATE_CHUNK):
            if has_non_english(chunk):
                try:
                    translated = translate_fn(chunk)
                    chunk_result.append(translated if translated else chunk)
                except Exception as exc:
                    print(f"  [warn] translation error: {exc}")
                    chunk_result.append(chunk)
            else:
                chunk_result.append(chunk)
        result.append("".join(chunk_result))
    return "".join(result)
def _chunked(text: str, size: int):
    """Yield successive chunks of `text` not exceeding `size` characters,
    splitting on newlines where possible."""
    start = 0
    while start < len(text):
        end = start + size
        if end >= len(text):
            yield text[start:]
            break
        # Try to split on a newline
        split = text.rfind("\n", start, end)
        if split == -1:
            split = end
        yield text[start:split]
        start = split
def translate_frontmatter(text: str, translate_fn) -> str:
    """Translate values in YAML frontmatter, preserving keys."""
    m = _FRONTMATTER.match(text)
    if not m:
        return text
    fm = m.group(1)
    rest = text[m.end():]
    translated_fm_lines = []
    for line in fm.splitlines(keepends=True):
        if ":" in line and has_non_english(line):
            key, _, value = line.partition(":")
            if has_non_english(value):
                try:
                    value = " " + translate_fn(value.strip()) + "\n"
                except Exception:
                    pass
            translated_fm_lines.append(key + ":" + value)
        else:
            translated_fm_lines.append(line)
    return "".join(translated_fm_lines) + translate_text(rest, translate_fn)
# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------
def process_file(path: Path, translate_fn, dry_run: bool) -> bool:
    """Translate a single file in place. Returns True if modified."""
    try:
        original = path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"  [skip] cannot read {path}: {exc}")
        return False
    if not has_non_english(original):
        return False
    ext = path.suffix.lower()
    if ext in {".md", ".html", ".mdc"}:
        translated = translate_frontmatter(original, translate_fn)
    else:
        translated = translate_text(original, translate_fn)
    if translated == original:
        return False
    if not dry_run:
        path.write_text(translated, encoding="utf-8")
    return True
def rename_if_needed(path: Path, dry_run: bool) -> Path:
    """Rename file if its name contains non-English characters."""
    if not has_non_english(path.name):
        return path
    stem = path.stem
    suffix = path.suffix
    new_stem = slugify_filename(stem)
    if not new_stem or new_stem == stem:
        return path
    new_path = path.parent / (new_stem + suffix)
    if dry_run:
        print(f"  [rename] {path.name} → {new_path.name}")
    else:
        path.rename(new_path)
        print(f"  Renamed: {path.name} → {new_path.name}")
    return new_path
# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dir", default=".", help="Root directory (default: .)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying")
    parser.add_argument("--service", default="google",
                        choices=["google", "mymemory", "libre"],
                        help="Translation service (default: google)")
    parser.add_argument("--source", default="auto",
                        help="Source language code (default: auto)")
    args = parser.parse_args()
    root = Path(args.dir).resolve()
    translate_fn = get_translator(args.service, args.source)
    modified = 0
    skipped = 0
    renamed = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            rel = str(path.relative_to(root))
            # Skip binary / i18n files
            if path.suffix.lower() in SKIP_EXTENSIONS:
                continue
            if is_i18n_file(rel):
                print(f"  [i18n]  {rel}")
                skipped += 1
                continue
            print(f"Processing: {rel}")
            # Rename if filename contains non-English characters
            if has_non_english(filename):
                path = rename_if_needed(path, args.dry_run)
                renamed += 1
            # Translate content
            if process_file(path, translate_fn, args.dry_run):
                print(f"  ✓ translated")
                modified += 1
            else:
                print(f"  - no changes")
    print(f"\nDone. {modified} files translated, {renamed} files renamed, {skipped} i18n files skipped.")
if __name__ == "__main__":
    main()
