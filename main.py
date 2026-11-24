#!/usr/bin/env python3
"""The World in One Day - entry for make.fun news-image-20261124.

Draws one PNG image summing up the world news of Tuesday
24 November 2026 and writes it to /output/entry.png (or to
$MAKEFUN_OUTPUT_DIR/entry.png outside the grader).

Standard library only: the picture is drawn pixel by pixel with a
built-in 5x7 bitmap font and encoded as a PNG with zlib, so two
runs always produce exactly the same bytes.

Stories, cross-checked across wire and roundup sources dated
24 November 2026:
  - Russian strikes on the Kyiv region kill at least 14; Zelensky
    warns intelligence shows new strikes being planned.
  - More bodies recovered from the Banten candy factory fire in
    Indonesia; the search for missing workers continues.
  - Nvidia reinstates Jensen Huang as CEO, 11 days after he
    stepped down amid a 'spy' controversy; shares surge.
  - COP31 in Antalya ends with no fossil-fuel deal; European and
    island states blame Saudi Arabia.
  - US Rep. Jimmy Gomez to resign on 1 Dec after a House Ethics
    panel finds evidence of sexual misconduct.
  - UN chief calls for an AI risk framework within a year; US
    states sue Musk's firms over sexualised Grok images.
  - Also: India-Nepal Saryu-Kamala Express flagged off; South
    Korea names a new foreign minister and spy chief; storms
    threaten Thanksgiving travel in the US.
"""
import binascii
import os
import struct
import zlib

W = H = 1024
PAPER = (247, 244, 236)
INK = (22, 22, 22)
GREY = (74, 74, 74)
LINEC = (190, 184, 168)
ACCENTS = [(176, 32, 40), (20, 90, 160), (200, 120, 10),
           (24, 130, 76), (110, 60, 170), (180, 60, 120)]

px = bytearray(W * H * 3)


def fill_all(c):
    px[:] = bytes(c) * (W * H)


def set_px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i:i + 3] = bytes(c)


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            set_px(xx, yy, c)


def border(x, y, w, h, c):
    rect(x, y, w, 1, c)
    rect(x, y + h - 1, w, 1, c)
    rect(x, y, 1, h, c)
    rect(x + w - 1, y, 1, h, c)


# 5x7 bitmap glyphs, one value per row, bit 16 = leftmost pixel.
FONT = {
    'A': [14, 17, 17, 31, 17, 17, 17], 'B': [30, 17, 17, 30, 17, 17, 30],
    'C': [14, 17, 16, 16, 16, 17, 14], 'D': [30, 17, 17, 17, 17, 17, 30],
    'E': [31, 16, 16, 30, 16, 16, 31], 'F': [31, 16, 16, 30, 16, 16, 16],
    'G': [14, 17, 16, 23, 17, 17, 15], 'H': [17, 17, 17, 31, 17, 17, 17],
    'I': [14, 4, 4, 4, 4, 4, 14], 'J': [7, 2, 2, 2, 2, 18, 12],
    'K': [17, 18, 20, 24, 20, 18, 17], 'L': [16, 16, 16, 16, 16, 16, 31],
    'M': [17, 27, 21, 21, 17, 17, 17], 'N': [17, 25, 21, 19, 17, 17, 17],
    'O': [14, 17, 17, 17, 17, 17, 14], 'P': [30, 17, 17, 30, 16, 16, 16],
    'Q': [14, 17, 17, 17, 21, 18, 13], 'R': [30, 17, 17, 30, 20, 18, 17],
    'S': [15, 16, 16, 14, 1, 1, 30], 'T': [31, 4, 4, 4, 4, 4, 4],
    'U': [17, 17, 17, 17, 17, 17, 14], 'V': [17, 17, 17, 17, 17, 10, 4],
    'W': [17, 17, 17, 21, 21, 21, 10], 'X': [17, 10, 4, 4, 4, 10, 17],
    'Y': [17, 10, 4, 4, 4, 4, 4], 'Z': [31, 1, 2, 4, 8, 16, 31],
    '0': [14, 17, 19, 21, 25, 17, 14], '1': [4, 12, 4, 4, 4, 4, 14],
    '2': [14, 17, 1, 2, 4, 8, 31], '3': [31, 2, 4, 2, 1, 17, 14],
    '4': [2, 6, 10, 18, 31, 2, 2], '5': [31, 16, 30, 1, 1, 17, 14],
    '6': [6, 8, 16, 30, 17, 17, 14], '7': [31, 1, 2, 4, 8, 8, 8],
    '8': [14, 17, 17, 14, 17, 17, 14], '9': [14, 17, 17, 15, 1, 2, 12],
    ' ': [0, 0, 0, 0, 0, 0, 0], '.': [0, 0, 0, 0, 0, 12, 12],
    ',': [0, 0, 0, 0, 12, 4, 8], ':': [0, 12, 12, 0, 12, 12, 0],
    "'": [4, 4, 8, 0, 0, 0, 0], '-': [0, 0, 0, 31, 0, 0, 0],
    '!': [4, 4, 4, 4, 4, 0, 4], '?': [14, 17, 1, 2, 4, 0, 4],
    '/': [1, 1, 2, 4, 8, 16, 16], '(': [2, 4, 8, 8, 8, 4, 2],
    ')': [8, 4, 2, 2, 2, 4, 8], '&': [12, 18, 20, 8, 21, 18, 13],
    '%': [24, 25, 2, 4, 8, 19, 3], '+': [0, 4, 4, 31, 4, 4, 0],
}


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, c):
    cx = x
    for ch in s.upper():
        g = FONT.get(ch, FONT['?'])
        for row in range(7):
            for col in range(5):
                if g[row] & (16 >> col):
                    rect(cx + col * scale, y + row * scale, scale, scale, c)
        cx += 6 * scale


def draw_centered(y, s, scale, c):
    draw_text((W - text_w(s, scale)) // 2, y, s, scale, c)


def wrap(s, scale, maxw):
    words, lines, cur = s.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if text_w(t, scale) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(x, y, s, scale, maxw, c, lh):
    yy = y
    for ln in wrap(s, scale, maxw):
        draw_text(x, yy, ln, scale, c)
        yy += lh
    return yy


PANELS = [
    ("KYIV, UKRAINE", "Strikes on Kyiv region kill at least 14",
     "Russian attacks hit homes near the capital. Zelensky warns "
     "intelligence shows Moscow is planning new strikes and presses "
     "allies for air defence."),
    ("BANTEN, INDONESIA", "More bodies found after factory fire",
     "Rescuers recover more victims from a burned candy factory in "
     "Banten and keep searching the ruins for workers still listed "
     "as missing."),
    ("NVIDIA, UNITED STATES", "Huang back as Nvidia CEO after 11 days",
     "Nvidia reinstates Jensen Huang as chief executive, 11 days "
     "after he stepped down amid a 'spy' controversy. Shares jump "
     "on the board's reversal."),
    ("ANTALYA, TURKIYE - COP31", "Climate summit ends with no fossil deal",
     "COP31 closes divided over fossil fuels. European and island "
     "states blame Saudi Arabia after talks fail to agree stronger "
     "phase-out language."),
    ("WASHINGTON, UNITED STATES", "Congressman Gomez to resign on 1 Dec",
     "Democratic Rep. Jimmy Gomez announces he will resign after a "
     "House Ethics panel finds evidence of sexual misconduct."),
    ("UNITED NATIONS - AI", "UN chief: AI risk rules within a year",
     "The UN secretary-general calls for an AI risk management "
     "framework within a year, as US states sue Musk's firms over "
     "sexualised Grok images."),
]


def draw_page():
    fill_all(PAPER)
    draw_centered(40, "THE WORLD IN ONE DAY", 8, INK)
    draw_centered(112, "TUESDAY - 24 NOVEMBER 2026", 4, ACCENTS[0])
    rect(36, 152, W - 72, 4, INK)
    rect(36, 160, W - 72, 1, INK)
    draw_centered(170, "THE DAY'S WORLD NEWS, SUMMED UP IN ONE IMAGE", 2, GREY)
    gx, gy = 36, 206
    pw = (W - 72 - 16) // 2
    ph = 218
    for i, (kicker, head, body) in enumerate(PANELS):
        x = gx + (i % 2) * (pw + 16)
        y = gy + (i // 2) * (ph + 14)
        accent = ACCENTS[i]
        border(x, y, pw, ph, LINEC)
        rect(x, y, pw, 10, accent)
        draw_text(x + 18, y + 24, kicker, 2, accent)
        hy = draw_wrapped(x + 18, y + 52, head, 3, pw - 36, INK, 26)
        draw_wrapped(x + 18, hy + 8, body, 2, pw - 36, GREY, 20)
    fy = gy + 3 * (ph + 14) - 4
    rect(36, fy, W - 72, 2, INK)
    also = ("ALSO TODAY: MODI AND NEPAL'S SHAH FLAG OFF THE SARYU-KAMALA "
            "EXPRESS - SOUTH KOREA NAMES A NEW FOREIGN MINISTER AND SPY "
            "CHIEF - STORMS AND AIRLINE GLITCHES THREATEN MESSY "
            "THANKSGIVING TRAVEL IN THE US")
    yy = fy + 12
    for ln in wrap(also, 2, W - 72):
        draw_centered(yy, ln, 2, INK)
        yy += 20


def encode_png():
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += px[y * W * 3:(y + 1) * W * 3]

    def chunk(tag, data):
        body = tag + data
        return (struct.pack(">I", len(data)) + body +
                struct.pack(">I", binascii.crc32(body) & 0xffffffff))

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
            chunk(b"IEND", b""))


def main():
    draw_page()
    png = encode_png()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(png)
    print(f"wrote entry.png ({len(png)} bytes)")


if __name__ == "__main__":
    main()
