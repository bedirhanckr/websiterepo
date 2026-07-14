#!/usr/bin/env python3
"""
Recursively optimize a source image tree into assets/img/.

Emits both an optimized JPEG/PNG (keeping the original extension so existing
HTML keeps working) and a WebP sibling with the same base name, so a future
HTML pass can layer <picture> on top without another regeneration.

Sizing profiles are chosen from the file name / parent folder:
  hero-*            → 2400 px wide, q82
  everything else   → 1600 px wide, q80
  thumb*/*-thumb*   →  800 px wide, q78
PNG-with-alpha is kept as PNG (palette-quantised); JPEGs are re-encoded
with mozjpeg-quality settings via Pillow.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageOps

PROFILES = {
    "hero":  {"max_w": 2400, "webp_q": 82, "jpeg_q": 84},
    "std":   {"max_w": 1600, "webp_q": 80, "jpeg_q": 82},
    "thumb": {"max_w":  800, "webp_q": 78, "jpeg_q": 80},
}


def pick_profile(rel_path: Path) -> dict:
    name = rel_path.name.lower()
    parent = rel_path.parent.name.lower()
    if "thumb" in name or "thumb" in parent:
        return PROFILES["thumb"]
    if name.startswith("hero") or "hero" in parent:
        return PROFILES["hero"]
    return PROFILES["std"]


def has_alpha(img: Image.Image) -> bool:
    return img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)


def optimize_one(src: Path, dst: Path, profile: dict) -> tuple[int, int]:
    """Return (jpeg/png_bytes, webp_bytes)."""
    img = Image.open(src)
    img = ImageOps.exif_transpose(img)

    max_w = profile["max_w"]
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, round(img.height * ratio)), Image.LANCZOS)

    dst.parent.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    alpha = has_alpha(img)

    if ext in (".jpg", ".jpeg") or (ext == ".png" and not alpha):
        rgb = img.convert("RGB")
        primary = dst.with_suffix(ext if ext in (".jpg", ".jpeg") else ".jpg")
        rgb.save(primary, "JPEG",
                 quality=profile["jpeg_q"], optimize=True, progressive=True)
        webp = dst.with_suffix(".webp")
        rgb.save(webp, "WEBP", quality=profile["webp_q"], method=6)
    else:
        primary = dst.with_suffix(".png")
        img.save(primary, "PNG", optimize=True)
        webp = dst.with_suffix(".webp")
        img.save(webp, "WEBP", quality=profile["webp_q"], method=6,
                 lossless=False)

    # If our re-encode came out larger than the source (usually iPhone JPEGs
    # already tuned high), keep the source bytes verbatim — a smaller original
    # beats a fatter "optimized" copy.
    src_bytes = src.stat().st_size
    if primary.stat().st_size > src_bytes:
        primary.write_bytes(src.read_bytes())

    return primary.stat().st_size, webp.stat().st_size


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path,
                    help="Raw image tree (e.g. _raw-images/ or a scratchpad extract)")
    ap.add_argument("target", type=Path, default=Path("assets/img"), nargs="?",
                    help="Output tree, defaults to assets/img")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.source.is_dir():
        print(f"source not found: {args.source}", file=sys.stderr)
        return 1

    exts = {".jpg", ".jpeg", ".png"}
    files = sorted(p for p in args.source.rglob("*") if p.suffix.lower() in exts)
    if not files:
        print("no source images found")
        return 0

    total_in = total_primary = total_webp = 0
    for src in files:
        rel = src.relative_to(args.source)
        dst = args.target / rel
        profile = pick_profile(rel)
        size_in = src.stat().st_size
        total_in += size_in
        if args.dry_run:
            print(f"[dry] {rel}  profile={profile['max_w']}px")
            continue
        try:
            primary_bytes, webp_bytes = optimize_one(src, dst, profile)
        except Exception as e:
            print(f"FAIL {rel}: {e}", file=sys.stderr)
            continue
        total_primary += primary_bytes
        total_webp += webp_bytes
        print(f"{rel}  {size_in//1024}K → {primary_bytes//1024}K + webp {webp_bytes//1024}K")

    if not args.dry_run:
        print(
            f"\nTotal: {len(files)} files, "
            f"in {total_in/1e6:.1f} MB → primary {total_primary/1e6:.1f} MB "
            f"+ webp {total_webp/1e6:.1f} MB"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
