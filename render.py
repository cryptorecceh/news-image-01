#!/usr/bin/env python3
"""Draw the news-image-01 entry: a one-page newspaper front page summing up
Friday 13 November 2026 world news. Pure PIL rendering (this is the build
tool; the graded entry is main.py, which copies the finished entry.png).

Stories (all first reported Fri 13 Nov 2026, cross-checked against
Reuters / BBC / AP / FT / The Guardian):
  LEAD  Nvidia chief summoned by Congress (day after Jensen Huang quit;
        probe into Nvidia China chip sales opens)
  FAA   Nationwide ground stop lifted at 8:15 p.m. ET after a 4.5-hour halt
  MSFT  Microsoft 365 outage (Outlook/Teams/Copilot) drags into Friday
  QT    Turkiye-Qatar mutual defence pact signed in Istanbul
  UKR   Europe joins Ukraine peace talks (Dublin agreement)
  TWN   Taiwan details China's unannounced Pacific drills
  OIL   IEA forecasts Q4 oil surplus (105m b/d vs demand +1.7m)
  EBOLA Ebola cases pass 11,000, second-worst outbreak on record
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (26, 26, 26)
RED = (176, 42, 42)
NAVY = (31, 58, 95)
GRAY = (110, 104, 92)
CARD_BG = (255, 253, 248)
CARD_LINE = (216, 210, 196)

FD = "/usr/share/fonts/truetype/dejavu/"

def serif_b(sz): return ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", sz)
def serif(sz): return ImageFont.truetype(FD + "DejaVuSerif.ttf", sz)
def sans_b(sz): return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", sz)
def sans(sz): return ImageFont.truetype(FD + "DejaVuSans.ttf", sz)

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, lines, font, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def rounded_rect(draw, box, rad, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)

# ---------- icons (drawn in a 64x64 tile at ox,oy) ----------
def icon_plane(d, ox, oy, c):
    d.text((ox + 6, oy + 4), "\u2708", font=ImageFont.truetype(FD + "DejaVuSans.ttf", 46), fill=c)

def icon_cloud(d, ox, oy, c):
    d.text((ox + 4, oy + 2), "\u2601", font=ImageFont.truetype(FD + "DejaVuSans.ttf", 46), fill=c)
    # lightning bolt
    d.polygon([(ox + 40, oy + 34), (ox + 30, oy + 52), (ox + 37, oy + 52),
               (ox + 31, oy + 62), (ox + 47, oy + 40), (ox + 39, oy + 40)], fill=(212, 144, 20))

def icon_shield(d, ox, oy, c):
    d.polygon([(ox + 12, oy + 8), (ox + 52, oy + 8), (ox + 52, oy + 32),
               (ox + 32, oy + 56), (ox + 12, oy + 32)], fill=c)
    d.ellipse((ox + 24, oy + 18, ox + 40, oy + 34), fill=(255, 255, 255))
    d.ellipse((ox + 28, oy + 16, ox + 44, oy + 32), fill=c)

def icon_talks(d, ox, oy, c):
    d.rounded_rectangle((ox + 8, oy + 12, ox + 38, oy + 36), radius=8, fill=(255, 255, 255), outline=c, width=3)
    d.rounded_rectangle((ox + 28, oy + 26, ox + 56, oy + 48), radius=8, fill=c)
    for cx in (18, 26, 34):
        d.ellipse((ox + cx - 2, oy + 21, ox + cx + 2, oy + 25), fill=c)
    for cx in (38, 46, 54):
        d.ellipse((ox + cx - 2, oy + 35, ox + cx + 2, oy + 39), fill=(255, 255, 255))

def icon_ship(d, ox, oy, c):
    d.polygon([(ox + 6, oy + 38), (ox + 58, oy + 38), (ox + 50, oy + 50), (ox + 14, oy + 50)], fill=c)
    d.rectangle((ox + 22, oy + 26, ox + 42, oy + 38), fill=c)
    d.rectangle((ox + 30, oy + 16, ox + 34, oy + 26), fill=c)
    d.arc((ox + 34, oy + 8, ox + 50, oy + 24), start=270, end=90, fill=c, width=3)
    d.line((ox + 32, oy + 50, ox + 32, oy + 54), fill=c, width=3)

def icon_barrel(d, ox, oy, c):
    d.rounded_rectangle((ox + 16, oy + 14, ox + 48, oy + 54), radius=6, fill=c)
    d.rectangle((ox + 16, oy + 24, ox + 48, oy + 29), fill=(255, 255, 255))
    d.rectangle((ox + 16, oy + 40, ox + 48, oy + 45), fill=(255, 255, 255))

def icon_virus(d, ox, oy, c):
    cx, cy = ox + 32, oy + 32
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        x1, y1 = cx + 16 * math.cos(a), cy + 16 * math.sin(a)
        x2, y2 = cx + 24 * math.cos(a), cy + 24 * math.sin(a)
        d.line((x1, y1, x2, y2), fill=c, width=4)
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=c)
    for dx, dy in ((-6, -4), (6, 4), (2, -8)):
        d.ellipse((cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2), fill=(255, 255, 255))

def icon_chip(d, ox, oy, c):
    d.rectangle((ox + 12, oy + 12, ox + 52, oy + 52), fill=c)
    for i in range(3):
        x = ox + 20 + i * 12
        d.rectangle((x, oy + 4, x + 5, oy + 12), fill=c)
        d.rectangle((x, oy + 52, x + 5, oy + 60), fill=c)
        y = oy + 20 + i * 12
        d.rectangle((ox + 4, y, ox + 12, y + 5), fill=c)
        d.rectangle((ox + 52, y, ox + 60, y + 5), fill=c)
    d.rectangle((ox + 22, oy + 22, ox + 42, oy + 42), fill=(212, 144, 20))

def draw_card(d, x, y, w, h, kicker, kcolor, headline, deck, icon, icolor):
    rounded_rect(d, (x, y, x + w, y + h), 6, fill=CARD_BG, outline=CARD_LINE, width=1)
    # icon tile
    tx, ty = x + 12, y + 12
    rounded_rect(d, (tx, ty, tx + 64, ty + 64), 8, fill=(238, 233, 220))
    icon(d, tx, ty, icolor)
    tx2 = x + 88
    d.text((tx2, y + 12), kicker, font=sans_b(13), fill=kcolor)
    lines = wrap(d, headline, serif_b(20), w - 100)
    yy = text_block(d, tx2, y + 30, lines[:2], serif_b(20), INK, 24)
    dlines = wrap(d, deck, sans(14), w - 24)
    text_block(d, x + 12, yy + 6, dlines[:3], sans(14), (64, 60, 52), 19)

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer border
    d.rectangle((10, 10, W - 11, H - 11), outline=INK, width=3)

    # masthead
    d.text((W // 2, 32), "THE WORLD IN ONE PAGE", font=serif_b(58), fill=INK, anchor="ma")
    d.text((W // 2, 100), "FRIDAY 13 NOVEMBER 2026", font=sans_b(21), fill=RED, anchor="ma")
    d.line((36, 138, W - 36, 138), fill=INK, width=2)
    d.line((36, 143, W - 36, 143), fill=INK, width=1)

    # ---- lead row ----
    ly = 158
    # lead story (left ~600px)
    d.text((36, ly), "TECH  ·  WASHINGTON", font=sans_b(16), fill=RED)
    hl = wrap(d, "NVIDIA CHIEF SUMMONED BY CONGRESS", serif_b(40), 470)
    yy = text_block(d, 36, ly + 26, hl, serif_b(40), INK, 46)
    deck = wrap(d, "A day after Jensen Huang quit as chief executive, lawmakers open a probe into Nvidia's China chip sales \u2014 and the ex-chief must testify.", sans(17), 470)
    text_block(d, 36, yy + 8, deck, sans(17), (64, 60, 52), 23)
    icon_chip(d, 520, ly + 34, NAVY)

    # divider
    d.line((648, ly + 4, 648, ly + 236), fill=CARD_LINE, width=1)
    # FAA story (right)
    icon_plane(d, 690, ly + 2, NAVY)
    d.text((768, ly + 14), "USA  ·  AVIATION", font=sans_b(15), fill=RED)
    hl2 = wrap(d, "FAA LIFTS NATIONWIDE GROUND STOP", serif_b(28), 300)
    yy2 = text_block(d, 672, ly + 66, hl2, serif_b(28), INK, 33)
    deck2 = wrap(d, "Flights resume at 8:15 p.m. ET after a 4\u00bd-hour halt; 8,267 departures cancelled \u2014 a third of the day's schedule.", sans(16), 312)
    text_block(d, 672, yy2 + 8, deck2, sans(16), (64, 60, 52), 22)

    # divider + section label
    d.line((36, 424, W - 36, 424), fill=INK, width=2)
    d.text((36, 436), "THE DAY IN BRIEF", font=sans_b(16), fill=INK)

    # ---- grid 3x2 ----
    cards = [
        ("TECH", (90, 90, 120), "MICROSOFT 365 OUTAGE DRAGS ON",
         "Outlook, Teams and Copilot still recovering after Thursday's global failure.",
         icon_cloud, (70, 90, 130)),
        ("MIDDLE EAST", (0, 120, 110), "T\u00dcRKIYE\u2013QATAR DEFENCE PACT",
         "Erdo\u011fan and Emir Tamim sign a mutual defence deal in Istanbul.",
         icon_shield, (0, 120, 110)),
        ("EUROPE", (110, 110, 40), "EUROPE JOINS UKRAINE TALKS",
         "Dublin agrees the EU and five states will sit at the peace table.",
         icon_talks, (110, 110, 40)),
        ("ASIA-PACIFIC", (60, 90, 120), "TAIWAN DETAILS CHINA DRILLS",
         "Taipei calls Beijing's unannounced Pacific exercises intimidation.",
         icon_ship, (60, 90, 120)),
        ("ENERGY", (180, 130, 20), "IEA FORECASTS OIL SURPLUS",
         "Supply to top demand by 1.7m barrels a day in the fourth quarter.",
         icon_barrel, (180, 130, 20)),
        ("HEALTH", (150, 40, 40), "EBOLA CASES PASS 11,000",
         "Second-worst outbreak on record; UN cites insecurity as the top challenge.",
         icon_virus, (150, 40, 40)),
    ]
    cw, chh, gx, gy = 306, 168, 16, 14
    x0, y0 = 36, 466
    for i, (kick, kc, head, deck, icon, ic) in enumerate(cards):
        cx = x0 + (i % 3) * (cw + gx)
        cy = y0 + (i // 3) * (chh + gy)
        draw_card(d, cx, cy, cw, chh, kick, kc, head, deck, icon, ic)

    # ---- ticker (shrink to fit) ----
    ty = 856
    d.rectangle((36, ty, W - 36, ty + 44), fill=NAVY)
    ticker = "ALSO:  IAEA flags an uninspected Iranian enrichment plant  \u00b7  Israeli strikes in southern Lebanon  \u00b7  Treasury faults chip-control delays"
    tfont = sans_b(15)
    while d.textlength(ticker, font=tfont) > W - 36 - 52 - 16 and tfont.size > 11:
        tfont = sans_b(tfont.size - 1)
    d.text((52, ty + 13), ticker, font=tfont, fill=(255, 255, 255))

    # ---- footer ----
    d.text((W // 2, 916), "Every story above was first reported on Friday 13 November 2026  \u00b7  Sources: Reuters, BBC, AP, FT, The Guardian",
           font=sans(14), fill=GRAY, anchor="ma")
    d.text((W // 2, 940), "Drawn by an AI agent  \u00b7  make.fun news-image-01",
           font=sans(13), fill=GRAY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
