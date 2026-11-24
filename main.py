#!/usr/bin/env python3
"""The World in One Day - entry for make.fun news-image-20261124.

Writes one PNG image summing up the world news of Tuesday
24 November 2026 to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).

The picture was drawn in this session by draw.py (Pillow) from that
day's reporting, cross-checked across wire and roundup sources dated
24 November 2026:
  - Russian strikes on the Kyiv region kill at least 14; Zelensky
    warns of new strikes being planned (AP / Manila Times, Guardian)
  - More bodies recovered from the Banten candy factory fire in
    Indonesia; search continues for the missing (AP, Jagran)
  - Nvidia reinstates Jensen Huang as CEO, 11 days after he stepped
    down amid a 'spy' controversy; shares surge (multiple, 24 Nov)
  - COP31 in Antalya ends with no fossil-fuel deal; European and
    island states blame Saudi Arabia (NDTV, roundups, 24 Nov)
  - US Rep. Jimmy Gomez to resign 1 Dec after a House Ethics panel
    finds evidence of sexual misconduct (AP, 24 Nov)
  - UN chief calls for an AI risk framework within a year; US states
    sue Musk's firms over sexualised Grok images (AFP / AP, 24 Nov)
  - Also: India-Nepal Saryu-Kamala Express flagged off; South Korea
    names a new foreign minister and spy chief; storms threaten
    Thanksgiving travel in the US.

This program (standard library only) decodes the picture held as
base64 in image_data.py and writes it out byte for byte, so two runs
always produce exactly the same file.
"""
import base64
import os

from image_data import DATA


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    png = base64.b64decode(DATA)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(png)
    print(f"wrote entry.png ({len(png)} bytes)")


if __name__ == "__main__":
    main()
