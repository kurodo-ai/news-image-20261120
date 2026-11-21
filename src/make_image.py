#!/usr/bin/env python3
"""Draw entry.png — one image summing up the world news of Friday 20 November 2026.

A newspaper front page drawn with Pillow: a masthead, a red date band and a
two-by-three grid of story panels, each with a small drawn icon, a bold
headline and a one-line summary. Every story is listed, with its sources,
in STORIES.md beside this script. All text is real text rendered from the
fonts below — nothing is pasted in from anywhere else.

Run:  python3 src/make_image.py   (writes ../entry.png)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "entry.png"

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

W = H = 1024
PAPER = (246, 241, 229)
PANEL = (255, 253, 247)
INK = (22, 19, 14)
GREY = (84, 78, 66)
RED = (179, 35, 27)
WHITE = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def check(draw, text, fnt, max_w, what):
    w = draw.textlength(text, font=fnt)
    if w > max_w:
        raise SystemExit(f"TOO WIDE ({what}): {w:.0f}px > {max_w}px :: {text!r}")
    return w


# ---------------------------------------------------------------- icons
def icon_flags(d, x, y, s):
    """Three summit flags: United States, China, Russia (simplified)."""
    fw, fh, gap = s * 0.30, s * 0.34, s * 0.05
    top = y + s * 0.10
    for i in range(3):
        fx = x + i * (fw + gap)
        d.line([(fx, top), (fx, y + s * 0.92)], fill=INK, width=max(3, s // 28))
        d.rectangle([fx, top, fx + fw, top + fh], outline=INK, width=max(2, s // 36))
    # US: stripes + blue canton
    fx = x
    for r in range(4):
        if r % 2 == 0:
            d.rectangle([fx + 2, top + 2 + r * fh / 4, fx + fw - 2, top + (r + 1) * fh / 4 - 1], fill=(178, 34, 52))
    d.rectangle([fx + 2, top + 2, fx + fw * 0.45, top + fh / 2], fill=(30, 40, 110))
    # China: red field, yellow dots
    fx = x + fw + gap
    d.rectangle([fx + 2, top + 2, fx + fw - 2, top + fh - 2], fill=(222, 41, 16))
    for dx, dy in [(0.16, 0.22), (0.34, 0.12), (0.38, 0.30), (0.34, 0.46)]:
        cx, cy, rr = fx + fw * dx, top + fh * dy, s * 0.022
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 222, 0))
    # Russia: white / blue / red bands
    fx = x + 2 * (fw + gap)
    for i, col in enumerate([(245, 245, 245), (0, 57, 166), (213, 43, 30)]):
        d.rectangle([fx + 2, top + 2 + i * fh / 3, fx + fw - 2, top + (i + 1) * fh / 3 - 1], fill=col)
    # ground line under the poles
    d.line([(x + s * 0.02, y + s * 0.94), (x + s * 0.98, y + s * 0.94)], fill=INK, width=max(3, s // 26))


def icon_barrage(d, x, y, s):
    """Night sky, a rocket and a burst over rooftops."""
    d.rectangle([x, y, x + s, y + s], fill=(24, 30, 58))
    # rooftops
    d.rectangle([x, y + s * 0.80, x + s, y + s], fill=(10, 10, 16))
    d.rectangle([x + s * 0.08, y + s * 0.68, x + s * 0.30, y + s * 0.82], fill=(10, 10, 16))
    d.rectangle([x + s * 0.62, y + s * 0.70, x + s * 0.86, y + s * 0.82], fill=(10, 10, 16))
    for wx, wy in [(0.14, 0.72), (0.70, 0.75), (0.45, 0.86)]:
        d.rectangle([x + s * wx, y + s * wy, x + s * (wx + 0.05), y + s * (wy + 0.05)], fill=(255, 196, 64))
    # rocket, nose down-left
    import math
    cx, cy = x + s * 0.62, y + s * 0.30
    ang = math.radians(50)
    dx, dy = math.cos(ang), math.sin(ang)
    px, py = -dy, dx
    nose = (cx + dx * s * 0.30, cy + dy * s * 0.30)
    tail = (cx - dx * s * 0.26, cy - dy * s * 0.26)
    wdt = s * 0.075
    body = [(nose[0], nose[1]),
            (cx + px * wdt, cy + py * wdt),
            (tail[0] + px * wdt, tail[1] + py * wdt),
            (tail[0] - px * wdt, tail[1] - py * wdt),
            (cx - px * wdt, cy - py * wdt)]
    d.polygon(body, fill=(226, 228, 232))
    flame = [(tail[0] + px * wdt * 0.8, tail[1] + py * wdt * 0.8),
             (tail[0] - px * wdt * 0.8, tail[1] - py * wdt * 0.8),
             (tail[0] - dx * s * 0.20, tail[1] - dy * s * 0.20)]
    d.polygon(flame, fill=(255, 140, 0))
    # burst, low left
    bx, by = x + s * 0.24, y + s * 0.60
    for a in range(0, 360, 30):
        r1, r2 = s * 0.05, s * (0.20 if a % 60 == 0 else 0.13)
        d.line([(bx + r1 * math.cos(math.radians(a)), by + r1 * math.sin(math.radians(a))),
                (bx + r2 * math.cos(math.radians(a)), by + r2 * math.sin(math.radians(a)))],
               fill=(255, 166, 0), width=max(3, s // 22))
    d.ellipse([bx - s * 0.055, by - s * 0.055, bx + s * 0.055, by + s * 0.055], fill=(255, 214, 90))


def icon_court(d, x, y, s):
    """A courthouse: pediment, columns, steps."""
    cx = x + s / 2
    d.polygon([(x + s * 0.08, y + s * 0.30), (x + s * 0.92, y + s * 0.30), (cx, y + s * 0.08)], fill=INK)
    d.ellipse([cx - s * 0.045, y + s * 0.155, cx + s * 0.045, y + s * 0.245], fill=PAPER)
    d.rectangle([x + s * 0.10, y + s * 0.33, x + s * 0.90, y + s * 0.38], fill=INK)
    for i in range(4):
        cxx = x + s * (0.17 + i * 0.185)
        d.rectangle([cxx, y + s * 0.42, cxx + s * 0.085, y + s * 0.74], fill=INK)
    d.rectangle([x + s * 0.10, y + s * 0.76, x + s * 0.90, y + s * 0.81], fill=INK)
    d.rectangle([x + s * 0.05, y + s * 0.85, x + s * 0.95, y + s * 0.90], fill=INK)


def icon_climate(d, x, y, s):
    """A warming globe with a thermometer."""
    cx, cy, r = x + s * 0.44, y + s * 0.50, s * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 124, 196))
    green = (52, 153, 84)
    d.polygon([(cx - r * 0.62, cy - r * 0.55), (cx - r * 0.10, cy - r * 0.72), (cx - r * 0.02, cy - r * 0.30),
               (cx - r * 0.34, cy - r * 0.12), (cx - r * 0.66, cy - r * 0.28)], fill=green)
    d.polygon([(cx + r * 0.18, cy + r * 0.05), (cx + r * 0.62, cy + r * 0.02), (cx + r * 0.70, cy + r * 0.42),
               (cx + r * 0.34, cy + r * 0.62), (cx + r * 0.16, cy + r * 0.34)], fill=green)
    d.polygon([(cx - r * 0.30, cy + r * 0.42), (cx + r * 0.02, cy + r * 0.36), (cx - r * 0.02, cy + r * 0.70),
               (cx - r * 0.34, cy + r * 0.66)], fill=green)
    # thermometer
    tx = x + s * 0.86
    d.rounded_rectangle([tx - s * 0.045, y + s * 0.14, tx + s * 0.045, y + s * 0.72], radius=s * 0.045, fill=(214, 48, 49))
    d.ellipse([tx - s * 0.095, y + s * 0.66, tx + s * 0.095, y + s * 0.90], fill=(214, 48, 49))
    for i in range(3):
        yy = y + s * (0.24 + i * 0.14)
        d.line([(tx + s * 0.07, yy), (tx + s * 0.13, yy)], fill=INK, width=max(2, s // 40))


def icon_markets(d, x, y, s):
    """Falling bars and a red down arrow."""
    base = y + s * 0.86
    d.line([(x + s * 0.08, y + s * 0.10), (x + s * 0.08, base)], fill=INK, width=max(3, s // 30))
    d.line([(x + s * 0.08, base), (x + s * 0.94, base)], fill=INK, width=max(3, s // 30))
    for i, hgt in enumerate([0.30, 0.44, 0.38, 0.56]):
        bx = x + s * (0.16 + i * 0.19)
        d.rectangle([bx, base - s * hgt, bx + s * 0.11, base], fill=(120, 116, 108))
    pts = [(x + s * 0.14, y + s * 0.22), (x + s * 0.40, y + s * 0.38),
           (x + s * 0.58, y + s * 0.30), (x + s * 0.86, y + s * 0.66)]
    d.line(pts, fill=RED, width=max(4, s // 18), joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex + s * 0.06, ey - s * 0.02), (ex - s * 0.10, ey - s * 0.06), (ex - s * 0.02, ey + s * 0.10)], fill=RED)


def icon_health(d, x, y, s):
    """A medical cross in a circle."""
    cx, cy, r = x + s / 2, y + s / 2, s * 0.44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(15, 118, 110), width=max(4, s // 16))
    t, l = s * 0.13, s * 0.30
    d.rectangle([cx - t / 2, cy - l / 2, cx + t / 2, cy + l / 2], fill=(15, 118, 110))
    d.rectangle([cx - l / 2, cy - t / 2, cx + l / 2, cy + t / 2], fill=(15, 118, 110))


# ---------------------------------------------------------------- panels
def panel(d, box, kicker, kicker_col, head, sub, icon):
    """One story panel: icon + kicker on top, headline, then the summary."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PANEL, outline=INK, width=3)
    icon(d, x0 + 18, y0 + 16, 76)
    kf = font(SANS_BOLD, 21)
    check(d, kicker, kf, x1 - (x0 + 110) - 14, "kicker")
    d.text((x0 + 110, y0 + 30), kicker, font=kf, fill=kicker_col)
    d.rectangle([x0 + 110, y0 + 62, x0 + 168, y0 + 68], fill=kicker_col)
    hf = font(SANS_BOLD, 32)
    yy = y0 + 102
    for line in head:
        check(d, line, hf, x1 - x0 - 36, "headline")
        d.text((x0 + 18, yy), line, font=hf, fill=INK)
        yy += 38
    sf = font(SANS, 21)
    yy = y1 - 62
    for line in sub:
        check(d, line, sf, x1 - x0 - 36, "sub")
        d.text((x0 + 18, yy), line, font=sf, fill=GREY)
        yy += 25


STORIES = [
    # (box, kicker, colour, headline lines, summary lines, icon)
    ((32, 222, 504, 462), "DIPLOMACY · SHENZHEN, CHINA", (32, 80, 158),
     ["TRUMP, XI & PUTIN HOLD", "FIRST THREE-WAY SUMMIT"],
     ["The three leaders issue a joint", "peace declaration"], icon_flags),
    ((520, 222, 992, 462), "WAR · KYIV, UKRAINE", RED,
     ["RUSSIA'S MASSIVE", "BARRAGE ON KYIV"],
     ["Missiles & drones pound the power grid;", "8 killed, embassies & cathedral damaged"], icon_barrage),
    ((32, 474, 504, 714), "JUSTICE · THE HAGUE", (91, 58, 142),
     ["WORLD COURT: MYANMAR", "COMMITTED GENOCIDE"],
     ["First state genocide ruling in the court's", "history — Myanmar rejects the verdict"], icon_court),
    ((520, 474, 992, 714), "CLIMATE · ANTALYA, TÜRKIYE", (30, 125, 70),
     ["COP31 TALKS GO INTO", "OVERTIME, DEADLOCKED"],
     ["Nearly 200 nations split after fossil fuels", "were dropped from the draft deal"], icon_climate),
    ((32, 726, 504, 966), "MARKETS · NEW YORK — TOKYO", (176, 111, 0),
     ["AI SELL-OFF SHAKES", "WORLD MARKETS"],
     ["Nikkei falls 4.8% as Anthropic makes", "its giant Nasdaq debut"], icon_markets),
    ((520, 726, 992, 966), "HEALTH · NAIROBI, KENYA", (15, 118, 110),
     ["LAST EBOLA PATIENT", "GOES HOME IN KENYA"],
     ["Discharged 37 days after the first", "case of the outbreak was confirmed"], icon_health),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    centered(d, W / 2, 22, "ONE DAY · ONE IMAGE · THE WORLD'S NEWS", font(SANS_BOLD, 23), GREY)
    centered(d, W / 2, 48, "THE WORLD IN A DAY", font(SERIF_BOLD, 82), INK)
    d.line([(32, 140), (992, 140)], fill=INK, width=3)
    d.rectangle([32, 150, 992, 206], fill=RED)
    centered(d, W / 2, 157, "FRIDAY · 20 NOVEMBER 2026", font(SANS_BOLD, 44), WHITE)

    for box, kicker, col, head, sub, icon in STORIES:
        panel(d, box, kicker, col, head, sub, icon)

    centered(d, W / 2, 978, "Stories as reported on the day · Sources: Reuters · UN News · Al Jazeera · SCMP · CNN",
             font(SANS, 17), GREY)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
