#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news infographic (1024x1024 PNG).

Flat world map drawn from code (simple continent outlines, equirectangular
projection) with 6 numbered pins, a legend strip of 6 short headlines and
an 'Also' footer. Only verified facts from the task brief are used.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (13, 32, 61)
NAVY2 = (24, 52, 92)
SKY = (214, 231, 240)
LAND = (168, 196, 164)
LAND_EDGE = (110, 145, 110)
INK = (18, 24, 32)
MUTED = (70, 82, 96)
WHITE = (255, 255, 255)
GOLD = (232, 178, 44)
PIN_COLORS = [(198, 40, 40), (21, 101, 192), (46, 125, 50),
              (123, 31, 162), (230, 81, 0), (0, 105, 120)]

# Simplified continent outlines as (lon, lat) points.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-80, 73), (-70, 62), (-55, 52), (-60, 45), (-75, 35), (-80, 25),
     (-90, 20), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-165, 60)],
    # South America
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -10), (-35, -20),
     (-40, -30), (-50, -35), (-65, -40), (-70, -50), (-73, -55),
     (-70, -40), (-75, -20), (-80, -5)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
     (32, -28), (20, -35), (15, -30), (12, -18), (9, 0), (-8, 5)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (40, 68),
     (50, 70), (60, 70), (70, 73), (80, 73), (90, 75), (100, 77),
     (110, 76), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 66), (178, 65), (170, 60), (162, 56), (158, 52), (150, 59),
     (142, 55), (140, 50), (135, 43), (130, 42), (127, 40), (122, 38),
     (120, 32), (115, 23), (110, 20), (108, 12), (105, 9), (100, 8),
     (98, 15), (95, 16), (92, 21), (88, 22), (85, 19), (80, 13),
     (77, 8), (75, 12), (72, 20), (68, 23), (65, 25), (61, 25),
     (57, 26), (55, 26), (52, 27), (50, 29), (48, 30), (44, 29),
     (40, 31), (36, 36), (30, 36), (26, 38), (23, 36), (19, 40),
     (15, 44), (12, 44), (8, 44), (3, 43), (-2, 37), (-9, 37)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32),
     (132, -32), (136, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -11),
     (140, -17), (135, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
]

# (number, lon, lat, headline, detail)
STORIES = [
    (1, 114.0, 22.5, "APEC OPENS IN SHENZHEN",
     "Trump in Manila for Quad talks; Xi meets Canada's Carney."),
    (2, 50.5, 26.2, "BAHRAIN ALL-CLEAR",
     "After overnight threat warning; Kuwait intercepts drones."),
    (3, -122.0, 37.4, "NVIDIA REVENUE $115.84 BN",
     "Doubles year on year; board rejects Huang's return."),
    (4, 34.5, 31.5, "GAZA CEASEFIRE AT RISK",
     "Board of Peace warns of collapse; one hot meal every two days."),
    (5, 88.0, 15.0, "CYCLONE AKVAN STRENGTHENS",
     "In the Bay of Bengal; forecast to turn severe on 19 Nov."),
    (6, 24.0, 56.9, "LATVIA'S NEW GOVERNMENT",
     "Parliament approves Kulbergs cabinet; 372 civilians killed in Ukraine in October."),
]

FOOTER_ALSO = ("Also: MS Dhoni retires from IPL  ·  Voyager 1 nears one light-day "
               "from Earth  ·  Baidu chief warns of AI bubble")

MAP_TOP, MAP_BOTTOM = 128, 556


def project(lon, lat):
    x = (lon + 180.0) / 360.0 * W
    y = MAP_TOP + (90.0 - lat) / 180.0 * (MAP_BOTTOM - MAP_TOP)
    return x, y


def font(path, size):
    return ImageFont.truetype(path, size)


def draw():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # Header band
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 124], fill=GOLD)
    f_title = font(FONTB, 46)
    f_date = font(FONTB, 30)
    d.text((32, 14), "WORLD NEWS IN ONE IMAGE", font=f_title, fill=WHITE)
    d.text((32, 72), "Wednesday 18 November 2026", font=f_date, fill=GOLD)

    # Map background (ocean) + graticule
    d.rectangle([0, 124, W, MAP_BOTTOM], fill=SKY)
    for lon in range(-150, 181, 30):
        x = (lon + 180) / 360 * W
        d.line([(x, 124), (x, MAP_BOTTOM)], fill=(190, 212, 224), width=1)
    for lat in (-30, 0, 30, 60):
        y = MAP_TOP + (90 - lat) / 180 * (MAP_BOTTOM - MAP_TOP)
        d.line([(0, y), (W, y)], fill=(190, 212, 224), width=1)

    # Continents
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)

    # Pins
    f_pin = font(FONTB, 22)
    for num, lon, lat, _h, _dt in STORIES:
        x, y = project(lon, lat)
        r = 19
        col = PIN_COLORS[num - 1]
        d.ellipse([x - r, y - r, x + r, y + r], fill=col,
                  outline=WHITE, width=3)
        tw = d.textlength(str(num), font=f_pin)
        d.text((x - tw / 2, y - 15), str(num), font=f_pin, fill=WHITE)

    # Legend strip
    d.rectangle([0, MAP_BOTTOM, W, MAP_BOTTOM + 6], fill=GOLD)
    y = MAP_BOTTOM + 14
    f_head = font(FONTB, 24)
    f_det = font(FONT, 20)
    for num, _lon, _lat, head, det in STORIES:
        col = PIN_COLORS[num - 1]
        d.ellipse([32, y + 2, 62, y + 32], fill=col)
        tw = d.textlength(str(num), font=f_pin)
        d.text((47 - tw / 2, y + 2), str(num), font=f_pin, fill=WHITE)
        d.text((76, y), head, font=f_head, fill=INK)
        d.text((76, y + 29), det, font=f_det, fill=MUTED)
        y += 58

    # Footer: two lines, fully inside the canvas
    fy = y + 8
    d.rectangle([0, fy, W, H], fill=NAVY2)
    f_foot = font(FONT, 20)
    lines = textwrap.wrap(FOOTER_ALSO, width=76)
    yy = fy + 10
    for line in lines:
        d.text((32, yy), line, font=f_foot, fill=WHITE)
        yy += 27
    return img


if __name__ == "__main__":
    image = draw()
    image.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", image.size)
