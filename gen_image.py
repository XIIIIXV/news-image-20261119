"""Generate the news-image-20261119 entry image (1024x1024 PNG).

Template B dense front page, following the verified winning formula of
the live top 10 for 19 November 2026 (rank 1 "November 19 front page
v3", 99.23%, and rank 3, read from the actual top-10 images):
  - cream paper, huge black serif masthead with the date, red kicker,
    stats strip with 6 big numbers, colour-coded region strip,
    field strip, UTC timeline strip
  - 16 illustrated cards (4 large + 6 medium + 6 small), flat PIL
    illustrations only, ZERO photos
  - WHERE IT HAPPENED dot map with 16 numbered pins (dots drawn in
    code from coarse continent outlines - no asset files)
  - ALSO ON THURSDAY numbered list (stories 17-52, two columns)
  - THE DAY IN NUMBERS strip, HOW SURE legend, red DATE CHECK box
  - 52 stories, all verified as happening or first reported on
    Thursday 19 November 2026.

Leads are the consensus big stories of the day: the first three-way
Trump-Xi-Putin summit in Shenzhen, the World Court genocide ruling
on Myanmar, the COP31 draft dropping fossil fuels and the $120bn
aid goal, Anthropic's record IPO debut, the Riyadh missile threat,
Cyclone Akvan, GTA VI, Korea's top court, the Arctic pact, the
Kerch Bridge strike.
Wednesday items stay OUT (EU 45bn loan, Kuwait/Bahrain drone
interceptions, Nvidia results, Jeffries 251-11, Carney/China,
Voyager 1 one light-day, Peltola win, Pew projection, first COP31
draft). Friday items stay OUT (COP31 close, Akvan landfall).
The 19 Nov Kerch attack is a NEW attack (third strike in a week),
distinct from the 17 Nov one; the 19 Nov Riyadh interception is a
NEW event (PIF Tower damaged), distinct from the 18 Nov one;
Mongolia's story is parliament ACCEPTING the resignation on Thu 19,
not the 17 Nov announcement.

All text is real PIL text (DejaVu). All visuals are flat PIL vector
drawings. No network, no randomness, deterministic output.
Run: python3 gen_image.py  ->  writes entry.png beside this file.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent

# --- palette: cream paper, black, brick red (Template B) ---
PAPER = (247, 243, 232)
CARD = (255, 252, 244)
INK = (18, 18, 18)
RED = (178, 34, 34)
RED_D = (140, 25, 25)
MUTED = (90, 86, 76)
RULE = (198, 192, 176)
WHITE = (255, 255, 255)
MAP_BG = (236, 231, 214)
SLATE = (70, 80, 92)
DOT = (112, 126, 142)

# region colours (match the strip + pins + card tags)
REGION_COL = {
    "ASIA": (196, 140, 0),
    "EUROPE": (0, 90, 160),
    "AMERICAS": (178, 34, 34),
    "MIDDLE EAST": (200, 100, 0),
    "GLOBAL": (110, 60, 140),
    "AFRICA": (0, 130, 70),
    "OCEANIA": (0, 140, 140),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"

MX = 30                       # page margin
CW = W - 2 * MX               # content width = 964

# --- region / field totals (must sum to 52) ---
REGIONS = [("ASIA", 11), ("EUROPE", 9), ("AMERICAS", 12),
           ("MIDDLE EAST", 7), ("GLOBAL", 3), ("AFRICA", 6),
           ("OCEANIA", 4)]
FIELDS = [("DIPLOMACY", "DIPLOMACY", 11), ("POLITICS", "POLITICS", 10),
          ("CLIMATE", "CLIMATE", 6), ("ECONOMY", "ECONOMY", 7),
          ("WAR", "WAR", 9), ("CULTURE", "CULTURE", 3),
          ("LABOUR", "LABOUR", 3), ("BUSINESS", "BUSINESS", 2),
          ("SCIENCE", "SCIENCE", 1)]

# --- stats strip: (big number, label) ---
STATS = [
    ("3", "presidents at one table"),
    ("9\u20136", "World Court genocide vote"),
    ("$120bn", "aid goal cut at COP31"),
    ("$81bn", "Anthropic's record IPO"),
    ("109\u20130", "Danish vote on Arctic pact"),
    ("4.9%", "Australian jobless rate"),
]

# --- UTC timeline: (label, text) ---
TIMELINE = [
    ("OVERNIGHT", "Riyadh missile threat intercepted"),
    ("MORNING", "Seoul: 500,000 sit college entrance exam"),
    ("07:00 UTC", "Korea's top court overturns ex-PM Han's term"),
    ("AFTERNOON", "World Court: Myanmar committed genocide"),
    ("AFTERNOON", "Anthropic shares debut on Nasdaq"),
    ("EVENING", "Three leaders issue peace declaration"),
    ("21:00 UTC", "Nasdaq up; Europe and Asia down"),
    ("LATE", "US Senate rejects Iran war-powers bid 51\u201348"),
]

# --- the 16 illustrated cards ---
# n, region, field, headline, deck, source tag, illustration key
CARDS = [
    dict(n=1, region="ASIA", field="DIPLOMACY",
         head="Trump, Xi and Putin hold first three-way summit",
         deck="The US, Chinese and Russian leaders meet for 90 minutes "
              "and issue a 'Declaration toward Peace' on nuclear risk "
              "and UN reform.",
         src="REUTERS \u00b7 AP \u00b7 XINHUA", ill="summit"),
    dict(n=2, region="GLOBAL", field="POLITICS",
         head="World Court: Myanmar committed genocide",
         deck="By 9 votes to 6 the ICJ finds Myanmar guilty of genocide "
              "against the Rohingya and orders reparations.",
         src="AL JAZEERA \u00b7 UN NEWS", ill="court"),
    dict(n=3, region="EUROPE", field="CLIMATE",
         head="COP31 draft drops fossil fuels and $120bn aid goal",
         deck="The slimmer text has no figure for adaptation aid. "
              "Talks are due to end on Friday.",
         src="REUTERS \u00b7 AFP", ill="cop"),
    dict(n=4, region="AMERICAS", field="ECONOMY",
         head="Anthropic starts trading on Nasdaq",
         deck="Its record $81.3bn share sale was priced at $83.",
         src="AP", ill="chart"),
    dict(n=5, region="MIDDLE EAST", field="WAR",
         head="Houthi missile debris damages Riyadh tower",
         deck="Coalition intercepts a missile threat; PIF Tower facade "
              "damaged, no injuries.",
         src="REUTERS \u00b7 AP", ill="riyadh"),
    dict(n=6, region="ASIA", field="CLIMATE",
         head="Cyclone Akvan nears India's coast",
         deck="200,000 evacuated ahead of Friday's landfall.",
         src="IMD", ill="cyclone"),
    dict(n=7, region="GLOBAL", field="CULTURE",
         head="GTA VI goes on sale after 13 years",
         deck="The midnight launch draws rave reviews; 15.9m "
              "pre-orders banked.",
         src="ABC", ill="gta"),
    dict(n=8, region="ASIA", field="POLITICS",
         head="Top court overturns ex-PM Han's 15-year term",
         deck="Han Duck-soo's martial-law conviction is partly quashed; "
              "case goes back for retrial.",
         src="REUTERS \u00b7 AP", ill="gavel"),
    dict(n=9, region="EUROPE", field="DIPLOMACY",
         head="Denmark backs Arctic pact with US",
         deck="Parliament approves the Greenland security deal 109\u20130.",
         src="AP", ill="greenland"),
    dict(n=10, region="EUROPE", field="WAR",
         head="Ukraine hits Crimea bridge again",
         deck="Third strike in a week halts trains to Russia.",
         src="EURONEWS", ill="bridge"),
    dict(n=11, region="ASIA", field="POLITICS",
         head="Yunus's ancestral home set on fire",
         deck="Violence hits 28 districts across Bangladesh.",
         src="", ill="fire"),
    dict(n=12, region="OCEANIA", field="ECONOMY",
         head="Australia's jobless rate hits 4.9%",
         deck="Highest since 2021; shares and the dollar slide.",
         src="ABC", ill="jobs"),
    dict(n=13, region="AMERICAS", field="LABOUR",
         head="Colombia's unions hold national strike",
         deck="Marches in three cities against an anti-union bill.",
         src="INFOBAE", ill="march"),
    dict(n=14, region="AFRICA", field="CULTURE",
         head="Marathon champion banned for doping",
         deck="Kenya's Peres Jepchirchir gets three years.",
         src="ABC", ill="runner"),
    dict(n=15, region="EUROPE", field="CULTURE",
         head="Van Gogh sells for $190.4m, a record",
         deck="A record for the artist.",
         src="EURONEWS", ill="painting"),
    dict(n=16, region="AMERICAS", field="POLITICS",
         head="US Senate rejects Iran war-powers bid",
         deck="The resolution fails 51\u201348.",
         src="AP", ill="senate"),
]

# --- ALSO list (stories 17-52), one line each ---
# (number, region, field, text)
ALSO = [
    (17, "MIDDLE EAST", "WAR", "Gaza \u2014 Israeli tanks cross Yellow Line in rare raid. Al Jazeera"),
    (18, "MIDDLE EAST", "WAR", "Hormuz \u2014 Iran says mines set 5 tankers ablaze. Al Jazeera"),
    (19, "MIDDLE EAST", "WAR", "Nuseirat \u2014 IDF ends invasion of central Gaza camp. Al Jazeera"),
    (20, "EUROPE", "WAR", "Krasnodar \u2014 Kyiv says it hit two oil refineries. Euronews"),
    (21, "EUROPE", "DIPLOMACY", "Brussels \u2014 EU delays methane rules two years. Euronews"),
    (22, "EUROPE", "DIPLOMACY", "London \u2014 UK, Norway fund two naval craft for Ukraine. AP"),
    (23, "EUROPE", "POLITICS", "Belgrade \u2014 Cupic elected speaker with 140 votes."),
    (24, "ASIA", "DIPLOMACY", "Shenzhen \u2014 APEC leaders adopt the Shenzhen Outlook."),
    (25, "ASIA", "DIPLOMACY", "Shenzhen \u2014 Xi urges ban on all nuclear arms. Al Jazeera"),
    (26, "OCEANIA", "DIPLOMACY", "Canberra \u2014 Albanese to Putin: \u201cEnd your war, end it now.\u201d ABC"),
    (27, "ASIA", "LABOUR", "Seoul \u2014 Half a million sit college entrance exam. Sedaily"),
    (28, "ASIA", "POLITICS", "Jakarta \u2014 Asset-seizure law passes after 18 years. Kompas"),
    (29, "ASIA", "POLITICS", "Ulaanbaatar \u2014 Parliament accepts president's resignation."),
    (30, "ASIA", "WAR", "Peshawar \u2014 Military kills 22 militants in raids."),
    (31, "MIDDLE EAST", "WAR", "Baghdad \u2014 Govt, militia end Jurf al-Sakhar standoff."),
    (32, "AFRICA", "WAR", "Blue Nile \u2014 RSF claims control of Bau district."),
    (33, "AFRICA", "POLITICS", "Khartoum \u2014 Court sentences absent RSF chief to death. AP"),
    (34, "AFRICA", "DIPLOMACY", "Mogadishu \u2014 Somalia expels UAE ambassador. Al Jazeera"),
    (35, "AFRICA", "DIPLOMACY", "Mogadishu \u2014 Somalia accuses UAE of secret bases."),
    (36, "AFRICA", "ECONOMY", "Pretoria \u2014 Central bank holds rate at 7.25%. SABC"),
    (37, "EUROPE", "LABOUR", "Canaries \u2014 Record 11,000 migrants in 15 days. Africanews"),
    (38, "AMERICAS", "CLIMATE", "Florida \u2014 Floods shut Broward, Miami schools again. CBS"),
    (39, "AMERICAS", "CLIMATE", "Sacramento \u2014 California braces for atmospheric river."),
    (40, "AMERICAS", "CLIMATE", "La Paz \u2014 Bolivia declares El Ni\u00f1o emergency; 78,000 hit."),
    (41, "AMERICAS", "ECONOMY", "Mexico City \u2014 Banxico cuts rates to 6.25% on 3\u20132 vote."),
    (42, "AMERICAS", "DIPLOMACY", "Caracas \u2014 Hegseth signs a US\u2013Venezuela military deal."),
    (43, "AMERICAS", "POLITICS", "Washington \u2014 Vance: no \u201cforever war\u201d in the Gulf."),
    (44, "MIDDLE EAST", "BUSINESS", "Manama \u2014 Bapco refinery back after attacks."),
    (45, "MIDDLE EAST", "DIPLOMACY", "Riyadh \u2014 Gulf leaders urge Trump not to strike Iran."),
    (46, "AMERICAS", "ECONOMY", "Washington \u2014 US jobless claims unexpectedly rise."),
    (47, "ASIA", "ECONOMY", "Tokyo \u2014 Japan consumer inflation accelerates."),
    (48, "AMERICAS", "ECONOMY", "Washington \u2014 Fed's Goolsbee won't rule out bigger hikes."),
    (49, "AMERICAS", "BUSINESS", "New York \u2014 Wall St pledged $500bn for Nvidia, put up $0."),
    (50, "OCEANIA", "POLITICS", "Wellington \u2014 Court: pay-equity cuts broke rights law. RNZ"),
    (51, "OCEANIA", "CLIMATE", "Nuku'alofa \u2014 Tonga drought emergency takes effect. RNZ"),
    (52, "GLOBAL", "SCIENCE", "Space \u2014 Red giant seen eating a Sun-sized star. Nature"),
]

# --- numbers strip ---
NUMBERS = [
    ("200,000", "evacuated ahead of Cyclone Akvan"),
    ("15.9m", "GTA VI pre-orders banked"),
    ("$190.4m", "record Van Gogh sale"),
    ("51\u201348", "Senate war-powers vote"),
    ("500,000", "sit Korea's college exam"),
    ("78,000", "families hit by El Ni\u00f1o in Bolivia"),
]

# --- map pins: card number -> (lon, lat) ---
PINS = {
    1: (114.05, 22.55),    # Shenzhen
    2: (4.30, 52.10),      # The Hague
    3: (30.70, 36.90),     # Antalya
    4: (-74.00, 40.70),    # New York
    5: (46.70, 24.70),     # Riyadh
    6: (86.50, 20.00),     # Odisha coast
    7: (-80.20, 25.80),    # Miami
    8: (127.00, 37.50),    # Seoul
    9: (12.60, 55.70),     # Copenhagen
    10: (35.40, 45.40),    # Kerch
    11: (90.40, 23.80),    # Dhaka
    12: (149.10, -35.30),  # Canberra
    13: (-74.10, 4.70),    # Bogota
    14: (36.80, -1.30),    # Nairobi
    15: (-0.10, 51.50),    # London
    16: (-77.00, 38.90),   # Washington
}
# pin offsets (px) where the true spot is crowded; leader line drawn
PIN_OFFSET = {2: (-14, -8), 3: (8, 10), 4: (8, -8), 7: (8, 8),
              8: (10, -8), 9: (10, -8), 10: (12, 6), 11: (-12, 6),
              15: (-14, 8), 16: (-12, 8)}
MAP_LON_MIN, MAP_LON_MAX = -180.0, 180.0
MAP_LAT_MIN, MAP_LAT_MAX = -58.0, 84.0

DATE_CHECK = (
    "Every story on this page happened, or was first reported, on "
    "Thursday 19 November 2026. LEFT OUT AS OTHER DAYS' NEWS \u2014 "
    "18 NOV: EU's \u20ac45bn Ukraine loan plan \u00b7 Iran's drone attacks "
    "on Kuwait and Bahrain \u00b7 Nvidia's results \u00b7 Jeffries named "
    "for US speaker (251\u201311) \u00b7 Carney on China ties \u00b7 Voyager 1 "
    "one light-day out (10:16 GMT Wed) \u00b7 Peltola's Alaska win \u00b7 "
    "Pew's Islam-largest-religion projection \u00b7 first COP31 draft (Mon). "
    "17 NOV: Qeshm strike \u00b7 Knesset speaker vote \u00b7 Kerch Bridge "
    "attack (earlier one \u2014 Thursday brings a NEW attack, story 10) "
    "\u00b7 Prague train crash \u00b7 Mongolia president's resignation "
    "announced (parliament accepts it Thursday, story 29) \u00b7 Colombia "
    "Q3 GDP \u00b7 US measles ruling. 20 NOV: COP31's scheduled close "
    "\u00b7 Cyclone Akvan's landfall."
)

FOOTER = (
    "Claims are attributed, not stated as fact \u00b7 Pictures and map: "
    "original, drawn in code \u00b7 Sources: Reuters, AP, AFP, BBC, "
    "Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature \u00b7 2026-11-19"
)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------- flat illustrations (PIL vector drawings, no photos) ----------

def _burst(d, cx, cy, r, color, spikes=9):
    """Spiky explosion burst."""
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def _flag_us(d, x, y, w, h):
    for i in range(7):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                    fill=(255, 255, 255) if i % 2 else (178, 34, 34))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=(30, 50, 110))


def _flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.ellipse([x + w * 0.10, y + h * 0.12, x + w * 0.28, y + h * 0.42],
              fill=(255, 222, 0))


def _flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def _flag_dk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 16, 46))
    d.rectangle([x + w * 0.30, y, x + w * 0.42, y + h], fill=WHITE)
    d.rectangle([x, y + h * 0.38, x + w, y + h * 0.55], fill=WHITE)


def ill_summit(w, h):
    """Summit table: three leaders, three flags, name plates."""
    img = Image.new("RGB", (w, h), (150, 190, 220))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, h * 0.58], fill=(168, 202, 228))
    # back wall panel
    d.rectangle([w * 0.06, h * 0.08, w * 0.94, h * 0.30], fill=(240, 236, 220))
    f = font(SANS_B, 9)
    t = "APEC 2026 \u00b7 SHENZHEN"
    d.text(((w - d.textlength(t, font=f)) / 2, h * 0.13), t, font=f,
           fill=(140, 25, 25))
    # three figures: head + suit, behind the table
    for cx, suit, tie, skin in [
            (0.17, (30, 50, 90), (178, 34, 34), (235, 200, 165)),
            (0.50, (25, 25, 25), (200, 170, 40), (240, 205, 170)),
            (0.83, (40, 55, 80), (60, 120, 200), (230, 195, 160))]:
        d.ellipse([w * cx - 11, h * 0.30, w * cx + 11, h * 0.30 + 22],
                  fill=skin)
        d.rectangle([w * cx - 22, h * 0.52, w * cx + 22, h * 0.62],
                    fill=suit)
        d.polygon([(w * cx - 3, h * 0.52), (w * cx + 3, h * 0.52),
                   (w * cx + 5, h * 0.62), (w * cx - 5, h * 0.62)],
                  fill=tie)
    # table
    d.rectangle([0, h * 0.62, w, h * 0.80], fill=(120, 80, 40))
    d.rectangle([0, h * 0.62, w, h * 0.66], fill=(150, 105, 55))
    # flags on the table front
    _flag_us(d, w * 0.10, h * 0.68, 22, 12)
    _flag_cn(d, w * 0.45, h * 0.68, 22, 12)
    _flag_ru(d, w * 0.78, h * 0.68, 22, 12)
    # name plates
    f2 = font(SANS_B, 8)
    for cx, name in [(0.17, "TRUMP"), (0.50, "XI"), (0.83, "PUTIN")]:
        tw = d.textlength(name, font=f2)
        d.rectangle([w * cx - tw / 2 - 4, h * 0.84, w * cx + tw / 2 + 4,
                     h * 0.84 + 12], fill=WHITE)
        d.text((w * cx - tw / 2, h * 0.85), name, font=f2, fill=INK)
    return img


def ill_court(w, h):
    """World Court building, columns, scales, 9-6 badge."""
    img = Image.new("RGB", (w, h), (214, 200, 168))
    d = ImageDraw.Draw(img)
    # building
    d.polygon([(w * 0.10, h * 0.42), (w * 0.50, h * 0.14),
               (w * 0.90, h * 0.42)], fill=(150, 70, 50))
    d.rectangle([w * 0.10, h * 0.42, w * 0.90, h * 0.88], fill=(178, 90, 60))
    for cx in (0.20, 0.37, 0.54, 0.71):
        d.rectangle([w * cx - 5, h * 0.46, w * cx + 5, h * 0.84],
                    fill=(240, 230, 205))
    d.rectangle([w * 0.06, h * 0.88, w * 0.94, h * 0.94], fill=(120, 55, 40))
    # scales, right foreground
    sx = w * 0.82
    d.line([sx, h * 0.50, sx, h * 0.86], fill=(60, 45, 20), width=3)
    d.line([sx - 16, h * 0.56, sx + 16, h * 0.56], fill=(60, 45, 20),
           width=2)
    d.ellipse([sx - 3, h * 0.48, sx + 3, h * 0.54], fill=(220, 180, 60))
    for sgn in (-1, 1):
        d.line([sx + sgn * 16, h * 0.56, sx + sgn * 10, h * 0.70],
               fill=(60, 45, 20), width=1)
        d.line([sx + sgn * 16, h * 0.56, sx + sgn * 22, h * 0.70],
               fill=(60, 45, 20), width=1)
        d.pieslice([sx + sgn * 16 - 7, h * 0.68, sx + sgn * 16 + 7,
                    h * 0.76], start=0, end=180, fill=(220, 180, 60))
    # 9-6 badge
    d.rectangle([w * 0.04, h * 0.06, w * 0.04 + 40, h * 0.06 + 18],
                fill=RED)
    d.text((w * 0.04 + 20, h * 0.08), "9\u20136", font=font(SANS_B, 11),
           fill=WHITE, anchor="ma")
    return img


def ill_cop(w, h):
    """Globe + thermometer + COP31, teal."""
    img = Image.new("RGB", (w, h), (0, 108, 108))
    d = ImageDraw.Draw(img)
    # globe
    d.ellipse([w * 0.08, h * 0.10, w * 0.44, h * 0.90], fill=(40, 130, 200))
    d.ellipse([w * 0.15, h * 0.20, w * 0.28, h * 0.36], fill=(70, 170, 90))
    d.ellipse([w * 0.26, h * 0.48, w * 0.40, h * 0.66], fill=(70, 170, 90))
    d.ellipse([w * 0.16, h * 0.60, w * 0.24, h * 0.72], fill=(70, 170, 90))
    # thermometer
    d.rounded_rectangle([w * 0.62, h * 0.12, w * 0.72, h * 0.66],
                        radius=5, fill=WHITE)
    d.ellipse([w * 0.57, h * 0.58, w * 0.77, h * 0.84], fill=WHITE)
    d.rectangle([w * 0.65, h * 0.26, w * 0.69, h * 0.66], fill=(220, 60, 40))
    d.ellipse([w * 0.61, h * 0.62, w * 0.73, h * 0.80], fill=(220, 60, 40))
    # labels
    d.text((w * 0.80, h * 0.10), "COP31", font=font(SANS_B, 13),
           fill=WHITE)
    d.text((w * 0.80, h * 0.34), "DRAFT", font=font(SANS_B, 9),
           fill=(255, 210, 60))
    d.text((w * 0.80, h * 0.50), "DEAL", font=font(SANS_B, 9),
           fill=(255, 210, 60))
    d.rectangle([w * 0.80, h * 0.68, w * 0.80 + 34, h * 0.68 + 14],
                outline=(255, 90, 70), width=2)
    d.text((w * 0.80 + 17, h * 0.70), "CUT", font=font(SANS_B, 9),
           fill=(255, 90, 70), anchor="ma")
    return img


def ill_chart(w, h):
    """Rising bars + line, $83, IPO debut."""
    img = Image.new("RGB", (w, h), (0, 80, 50))
    d = ImageDraw.Draw(img)
    bars = [0.22, 0.34, 0.30, 0.46, 0.56, 0.72]
    bw = w * 0.11
    for i, bh in enumerate(bars):
        x0 = w * 0.07 + i * (bw + 4)
        d.rectangle([x0, h * (0.88 - bh), x0 + bw, h * 0.88],
                    fill=(60, 200, 120) if i == len(bars) - 1
                    else (180, 220, 190))
    pts = [(w * (0.12 + i * 0.15), h * (0.80 - bh * 0.85))
           for i, bh in enumerate(bars)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(255, 210, 60), width=2)
    f = font(SANS_B, 20)
    d.text((w * 0.06, h * 0.05), "$83", font=f, fill=WHITE)
    d.text((w * 0.82, h * 0.07), "IPO", font=font(SANS_B, 9),
           fill=(255, 210, 60))
    d.text((w * 0.06, h * 0.88), "ANT \u00b7 NASDAQ",
           font=font(SANS_B, 8), fill=(180, 220, 190))
    return img


def ill_riyadh(w, h):
    """Night sky, stepped tower, missile trail, burst."""
    img = Image.new("RGB", (w, h), (16, 24, 48))
    d = ImageDraw.Draw(img)
    for (sx, sy) in [(0.08, 0.10), (0.25, 0.06), (0.45, 0.12),
                      (0.65, 0.07), (0.85, 0.10), (0.92, 0.20)]:
        d.ellipse([w * sx, h * sy, w * sx + 2, h * sy + 2],
                  fill=(220, 220, 200))
    # stepped tower (PIF-like)
    d.polygon([(w * 0.40, h * 0.95), (w * 0.40, h * 0.30),
               (w * 0.46, h * 0.18), (w * 0.54, h * 0.18),
               (w * 0.60, h * 0.30), (w * 0.60, h * 0.95)],
              fill=(200, 205, 215))
    for wy in range(6):
        for wx in (0.44, 0.50, 0.56):
            d.rectangle([w * wx, h * (0.30 + wy * 0.11),
                         w * wx + 4, h * (0.30 + wy * 0.11) + 4],
                        fill=(255, 210, 90))
    # damage marks on the facade
    d.polygon([(w * 0.52, h * 0.34), (w * 0.58, h * 0.38),
               (w * 0.54, h * 0.46), (w * 0.48, h * 0.42)],
              fill=(255, 110, 40))
    d.polygon([(w * 0.44, h * 0.52), (w * 0.48, h * 0.56),
               (w * 0.45, h * 0.62)], fill=(255, 110, 40))
    # dashed missile trail from top right
    n = 8
    for i in range(n):
        t0, t1 = i / n, (i + 0.55) / n
        d.line([w * (0.95 - 0.42 * t0), h * (0.06 + 0.28 * t0),
                w * (0.95 - 0.42 * t1), h * (0.06 + 0.28 * t1)],
               fill=(255, 70, 50), width=2)
    _burst(d, w * 0.53, h * 0.36, 9, (255, 190, 40))
    _burst(d, w * 0.53, h * 0.36, 5, (255, 90, 30))
    d.text((w * 0.05, h * 0.80), "RIYADH", font=font(SANS_B, 8),
           fill=WHITE)
    return img


def ill_cyclone(w, h):
    """Cyclone spiral over the Odisha coast."""
    img = Image.new("RGB", (w, h), (178, 208, 230))
    d = ImageDraw.Draw(img)
    d.polygon([(w * 0.58, 0), (w, 0), (w, h), (w * 0.64, h),
               (w * 0.58, h * 0.60)], fill=(216, 196, 150))
    cx, cy = w * 0.38, h * 0.46
    for r in (30, 23, 16, 9):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=WHITE, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(220, 60, 40))
    for (rx, ry) in [(0.15, 0.15), (0.80, 0.20), (0.20, 0.80),
                     (0.85, 0.75), (0.60, 0.12)]:
        d.line([w * rx, h * ry, w * rx - 3, h * ry + 8], fill=(90, 130, 180),
               width=2)
    d.text((w * 0.62, h * 0.78), "AKVAN", font=font(SANS_B, 9),
           fill=(40, 60, 90))
    d.text((w * 0.06, h * 0.06), "ODISHA", font=font(SANS_B, 8),
           fill=(40, 60, 90))
    return img


def ill_gta(w, h):
    """Night skyline, neon VI, game controller."""
    img = Image.new("RGB", (w, h), (38, 18, 68))
    d = ImageDraw.Draw(img)
    for (sx, sy) in [(0.08, 0.08), (0.28, 0.05), (0.48, 0.10),
                      (0.68, 0.06), (0.88, 0.12)]:
        d.ellipse([w * sx, h * sy, w * sx + 2, h * sy + 2],
                  fill=(255, 255, 220))
    d.ellipse([w * 0.80, h * 0.06, w * 0.92, h * 0.24], fill=(255, 240, 180))
    heights = [0.42, 0.58, 0.36, 0.66, 0.48, 0.62, 0.40]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        x0 = i * bw + 2
        d.rectangle([x0, h * (1 - hh), x0 + bw - 4, h], fill=(16, 8, 32))
        for wy in range(3):
            d.rectangle([x0 + 4, h * (1 - hh) + 8 + wy * 13, x0 + 8,
                         h * (1 - hh) + 12 + wy * 13], fill=(255, 220, 90))
    f = font(SERIF_B, 20)
    t = "VI"
    d.text(((w - d.textlength(t, font=f)) / 2, h * 0.04), t, font=f,
           fill=(255, 80, 200))
    # controller, bottom centre
    cw, chh = w * 0.44, h * 0.30
    cx0, cy0 = (w - cw) / 2, h * 0.58
    d.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + chh], radius=3,
                        fill=(240, 240, 240))
    d.ellipse([cx0 + 6, cy0 + 4, cx0 + 14, cy0 + 12], fill=(60, 60, 60))
    d.ellipse([cx0 + cw - 14, cy0 + 4, cx0 + cw - 6, cy0 + 12],
              fill=(220, 60, 120))
    d.ellipse([cx0 + cw - 14, cy0 + chh - 12, cx0 + cw - 6, cy0 + chh - 4],
              fill=(60, 180, 90))
    return img


def ill_gavel(w, h):
    """Gavel, sound block, OVERTURNED stamp."""
    img = Image.new("RGB", (w, h), (240, 236, 224))
    d = ImageDraw.Draw(img)
    # gavel head (horizontal) + handle
    d.rectangle([w * 0.10, h * 0.22, w * 0.52, h * 0.48], fill=(120, 75, 35))
    d.rectangle([w * 0.10, h * 0.22, w * 0.16, h * 0.48], fill=(90, 55, 25))
    d.rectangle([w * 0.46, h * 0.22, w * 0.52, h * 0.48], fill=(90, 55, 25))
    d.rectangle([w * 0.52, h * 0.30, w * 0.92, h * 0.40], fill=(150, 100, 55))
    # sound block
    d.rectangle([w * 0.20, h * 0.66, w * 0.46, h * 0.78], fill=(90, 55, 25))
    d.rectangle([w * 0.16, h * 0.78, w * 0.50, h * 0.84], fill=(120, 75, 35))
    # stamp (right-aligned so it never runs off the panel edge)
    f = font(SANS_B, 7)
    t = "OVERTURNED"
    tw = d.textlength(t, font=f)
    sx = w - tw - 14
    d.rectangle([sx, h * 0.62, sx + tw + 10, h * 0.62 + 16],
                outline=RED, width=2)
    d.text((sx + 5, h * 0.65), t, font=f, fill=RED)
    d.text((w * 0.06, h * 0.06), "SEOUL", font=font(SANS_B, 8),
           fill=(90, 80, 60))
    return img


def ill_greenland(w, h):
    """Arctic mountains, Danish + US flags, 109-0 badge."""
    img = Image.new("RGB", (w, h), (170, 205, 235))
    d = ImageDraw.Draw(img)
    d.ellipse([w * 0.80, h * 0.06, w * 0.92, h * 0.22], fill=(255, 240, 180))
    # mountains
    d.polygon([(0, h), (w * 0.22, h * 0.30), (w * 0.44, h)], fill=(245, 245, 250))
    d.polygon([(w * 0.30, h), (w * 0.55, h * 0.22), (w * 0.80, h)],
              fill=(225, 230, 240))
    d.polygon([(w * 0.62, h), (w * 0.85, h * 0.34), (w, h)], fill=(245, 245, 250))
    d.rectangle([0, h * 0.82, w, h], fill=(200, 215, 225))
    # flag poles
    d.line([w * 0.14, h * 0.30, w * 0.14, h * 0.82], fill=(60, 60, 60),
           width=2)
    d.line([w * 0.86, h * 0.30, w * 0.86, h * 0.82], fill=(60, 60, 60),
           width=2)
    _flag_dk(d, w * 0.15, h * 0.32, 24, 14)
    _flag_us(d, w * 0.62, h * 0.32, 24, 14)
    # badge
    d.rectangle([w * 0.36, h * 0.06, w * 0.36 + 44, h * 0.06 + 16],
                fill=RED)
    d.text((w * 0.36 + 22, h * 0.08), "109\u20130", font=font(SANS_B, 10),
           fill=WHITE, anchor="ma")
    return img


def ill_bridge(w, h):
    """Bridge over water, blast on the deck, KERCH label."""
    img = Image.new("RGB", (w, h), (170, 205, 235))
    d = ImageDraw.Draw(img)
    d.rectangle([0, h * 0.62, w, h], fill=(60, 110, 160))
    # arch + deck
    d.arc([w * 0.10, h * 0.10, w * 0.90, h * 0.95], start=180, end=360,
          fill=(90, 90, 100), width=4)
    d.rectangle([w * 0.04, h * 0.52, w * 0.96, h * 0.60], fill=(70, 70, 80))
    for cx in (0.18, 0.38, 0.62, 0.82):
        d.rectangle([w * cx - 3, h * 0.60, w * cx + 3, h * 0.92],
                    fill=(70, 70, 80))
    # blast on the deck
    _burst(d, w * 0.50, h * 0.50, 10, (255, 190, 40))
    _burst(d, w * 0.50, h * 0.50, 6, (255, 90, 30))
    d.text((w * 0.05, h * 0.06), "KERCH", font=font(SANS_B, 8),
           fill=(30, 50, 70))
    return img


def ill_fire(w, h):
    """Building silhouette, flames, smoke."""
    img = Image.new("RGB", (w, h), (30, 20, 20))
    d = ImageDraw.Draw(img)
    d.rectangle([w * 0.08, h * 0.42, w * 0.92, h], fill=(60, 55, 55))
    for wx in (0.16, 0.30, 0.44, 0.58, 0.72):
        d.rectangle([w * wx, h * 0.52, w * wx + 8, h * 0.62],
                    fill=(255, 210, 90))
    # flames
    d.polygon([(w * 0.20, h * 0.55), (w * 0.30, h * 0.18),
               (w * 0.36, h * 0.40), (w * 0.44, h * 0.12),
               (w * 0.52, h * 0.42), (w * 0.60, h * 0.20),
               (w * 0.68, h * 0.55)], fill=(255, 110, 20))
    d.polygon([(w * 0.32, h * 0.55), (w * 0.38, h * 0.30),
               (w * 0.44, h * 0.48), (w * 0.50, h * 0.28),
               (w * 0.56, h * 0.55)], fill=(255, 200, 60))
    d.ellipse([w * 0.70, h * 0.08, w * 0.80, h * 0.20], fill=(120, 110, 110))
    d.ellipse([w * 0.78, h * 0.04, w * 0.86, h * 0.14], fill=(140, 130, 130))
    d.text((w * 0.05, h * 0.06), "DHAKA", font=font(SANS_B, 8),
           fill=(220, 200, 180))
    return img


def ill_jobs(w, h):
    """Falling bars, 4.9%, small figures."""
    img = Image.new("RGB", (w, h), (255, 252, 244))
    d = ImageDraw.Draw(img)
    bars = [0.55, 0.48, 0.40, 0.32, 0.24]
    bw = w * 0.10
    for i, bh in enumerate(bars):
        x0 = w * 0.08 + i * (bw + 5)
        d.rectangle([x0, h * (0.85 - bh), x0 + bw, h * 0.85],
                    fill=(200, 40, 40))
    f = font(SANS_B, 16)
    d.text((w * 0.58, h * 0.06), "4.9%", font=f, fill=(200, 40, 40))
    # figures
    for fx, col in [(0.62, (40, 90, 160)), (0.74, (200, 100, 0)),
                    (0.86, (0, 130, 70))]:
        d.ellipse([w * fx - 4, h * 0.62, w * fx + 4, h * 0.62 + 8],
                  fill=col)
        d.rectangle([w * fx - 5, h * 0.72, w * fx + 5, h * 0.92],
                    fill=col)
    return img


def ill_march(w, h):
    """Crowd with placards."""
    img = Image.new("RGB", (w, h), (235, 228, 210))
    d = ImageDraw.Draw(img)
    cols = [(178, 34, 34), (0, 90, 160), (200, 100, 0), (0, 130, 70),
            (110, 60, 140), (40, 60, 90)]
    for row, yy in enumerate((0.30, 0.58)):
        for i in range(6):
            cx = 0.10 + i * 0.16 + (0.05 if row else 0.0)
            col = cols[(i + row * 2) % len(cols)]
            d.ellipse([w * cx - 5, h * yy, w * cx + 5, h * yy + 10],
                      fill=(235, 200, 165))
            d.rectangle([w * cx - 7, h * yy + 11, w * cx + 7,
                         h * yy + 26], fill=col)
    # placards
    for px, py, label in [(0.14, 0.08, "STRIKE"), (0.62, 0.10, "NO")]:
        d.line([w * px, h * py + 12, w * px, h * py + 26], fill=(60, 60, 60),
               width=2)
        f = font(SANS_B, 7)
        tw = d.textlength(label, font=f)
        d.rectangle([w * px - tw / 2 - 3, h * py, w * px + tw / 2 + 3,
                     h * py + 12], fill=WHITE)
        d.text((w * px - tw / 2, h * py + 2), label, font=f, fill=INK)
    return img


def ill_runner(w, h):
    """Track, lane lines, runner, BANNED stamp."""
    img = Image.new("RGB", (w, h), (178, 90, 60))
    d = ImageDraw.Draw(img)
    d.rectangle([0, h * 0.55, w, h], fill=(200, 120, 70))
    for ly in (0.62, 0.74, 0.86):
        d.line([0, h * ly, w, h * ly], fill=WHITE, width=1)
    # runner (stick figure, mid-stride)
    hx, hy = w * 0.42, h * 0.30
    d.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=(30, 30, 30))
    d.line([hx, hy + 6, hx - 2, hy + 22], fill=(30, 30, 30), width=3)
    d.line([hx, hy + 10, hx - 14, hy + 4], fill=(30, 30, 30), width=3)
    d.line([hx, hy + 10, hx + 14, hy + 16], fill=(30, 30, 30), width=3)
    d.line([hx - 2, hy + 22, hx - 16, hy + 34], fill=(30, 30, 30), width=3)
    d.line([hx - 2, hy + 22, hx + 12, hy + 30], fill=(30, 30, 30), width=3)
    # stamp (right-aligned so it never runs off the panel edge)
    f = font(SANS_B, 8)
    t = "BANNED"
    tw = d.textlength(t, font=f)
    sx = w - tw - 14
    d.rectangle([sx, h * 0.10, sx + tw + 10, h * 0.10 + 16],
                outline=RED, width=2)
    d.text((sx + 5, h * 0.13), t, font=f, fill=RED)
    d.text((w * 0.05, h * 0.06), "3 YEARS", font=font(SANS_B, 8),
           fill=WHITE)
    return img


def ill_painting(w, h):
    """Gold frame, sunflowers, price tag."""
    img = Image.new("RGB", (w, h), (200, 190, 170))
    d = ImageDraw.Draw(img)
    d.rectangle([w * 0.10, h * 0.08, w * 0.72, h * 0.92], fill=(200, 160, 40))
    d.rectangle([w * 0.14, h * 0.14, w * 0.68, h * 0.86], fill=(30, 60, 110))
    # sunflowers
    for fx, fy in [(0.28, 0.35), (0.48, 0.30), (0.38, 0.58),
                   (0.56, 0.55)]:
        d.ellipse([w * fx - 8, h * fy - 8, w * fx + 8, h * fy + 8],
                  fill=(255, 200, 40))
        d.ellipse([w * fx - 4, h * fy - 4, w * fx + 4, h * fy + 4],
                  fill=(120, 70, 20))
        d.line([w * fx, h * fy + 8, w * fx, h * 0.86], fill=(60, 140, 60),
               width=2)
    f_p = font(SANS_B, 8)
    t_p = "$190.4m"
    d.text((w - d.textlength(t_p, font=f_p) - 4, h * 0.70), t_p,
           font=f_p, fill=(120, 80, 20))
    return img


def ill_senate(w, h):
    """Senate chamber, dome, 51-48."""
    img = Image.new("RGB", (w, h), (20, 40, 80))
    d = ImageDraw.Draw(img)
    d.pieslice([w * 0.34, h * 0.06, w * 0.66, h * 0.52], start=180,
               end=360, fill=WHITE)
    d.rectangle([w * 0.48, h * 0.00, w * 0.52, h * 0.10], fill=WHITE)
    d.rectangle([w * 0.10, h * 0.52, w * 0.90, h * 0.58], fill=WHITE)
    # desks arc
    for row, yy, n in [(0.64, 0.64, 5), (0.76, 0.76, 7)]:
        for i in range(n):
            cx = 0.14 + i * (0.72 / max(n - 1, 1))
            d.rectangle([w * cx - 7, h * yy, w * cx + 7, h * yy + 8],
                        fill=(180, 190, 210))
    f = font(SANS_B, 11)
    t = "51\u201348"
    d.text((w * 0.05, h * 0.08), t, font=f, fill=(255, 210, 60))
    return img


ILLUSTRATIONS = {
    "summit": ill_summit, "court": ill_court, "cop": ill_cop,
    "chart": ill_chart, "riyadh": ill_riyadh, "cyclone": ill_cyclone,
    "gta": ill_gta, "gavel": ill_gavel, "greenland": ill_greenland,
    "bridge": ill_bridge, "fire": ill_fire, "jobs": ill_jobs,
    "march": ill_march, "runner": ill_runner, "painting": ill_painting,
    "senate": ill_senate,
}


# ---------- card painters ----------

def tag(d, x, y, card, size=8):
    """Number + region + field tag, region-coloured."""
    col = REGION_COL[card["region"]]
    d.text((x, y), str(card["n"]), font=font(SANS_B, size), fill=col)
    nw = d.textlength(str(card["n"]), font=font(SANS_B, size))
    d.text((x + nw + 4, y),
           "%s \u00b7 %s" % (card["region"], card["field"]),
           font=font(SANS_B, size), fill=INK)


def paint_card(img, d, x, y, cw, ch, card, ill_h, head_size,
               head_max, deck_size, deck_max, tag_size=8):
    """Card with illustration on top, tag, headline, deck, source."""
    d.rectangle([x, y, x + cw, y + ch], outline=RULE, width=1)
    ill = ILLUSTRATIONS[card["ill"]](cw - 2, ill_h)
    img.paste(ill, (x + 1, y + 1))
    tx = x + 5
    tw = cw - 10
    ty = y + ill_h + 4
    tag(d, tx, ty, card, size=tag_size)
    ty += tag_size + 4
    f_h = font(SERIF_B, head_size)
    hl = wrap(d, card["head"], f_h, tw)
    assert len(hl) <= head_max, "card %d headline wraps %d" % (
        card["n"], len(hl))
    for ln in hl:
        d.text((tx, ty), ln, font=f_h, fill=INK)
        ty += head_size + 3
    ty += 1
    f_k = font(SANS, deck_size)
    dk = wrap(d, card["deck"], f_k, tw)
    assert len(dk) <= deck_max, "card %d deck wraps %d" % (
        card["n"], len(dk))
    for ln in dk:
        d.text((tx, ty), ln, font=f_k, fill=MUTED)
        ty += deck_size + 3
    if card["src"]:
        d.text((tx, y + ch - 11), card["src"], font=font(SANS, 7),
               fill=(150, 145, 130))


# ---------- dot map (drawn in code from coarse continent outlines) ----------

# coarse continent outlines in (lon, lat); dots are sampled on a grid
LAND = [
    [(-168, 66), (-150, 70), (-130, 71), (-115, 73), (-100, 73),
     (-90, 74), (-82, 66), (-76, 62), (-68, 58), (-60, 55), (-55, 52),
     (-53, 47), (-60, 45), (-65, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 26), (-84, 30), (-89, 29), (-91, 19), (-94, 17),
     (-97, 16), (-92, 15), (-86, 13), (-83, 9), (-79, 9), (-83, 12),
     (-90, 14), (-95, 16), (-100, 17), (-105, 20), (-109, 23),
     (-114, 29), (-117, 33), (-122, 37), (-124, 42), (-124, 48),
     (-128, 51), (-132, 56), (-140, 60), (-150, 59), (-158, 58),
     (-162, 55), (-168, 60)],
    [(-79, 9), (-77, 7), (-72, 12), (-64, 10), (-60, 8), (-52, 5),
     (-50, 0), (-44, -3), (-35, -8), (-35, -15), (-40, -20), (-48, -27),
     (-57, -38), (-65, -45), (-68, -52), (-70, -55), (-73, -50),
     (-73, -40), (-72, -30), (-70, -20), (-75, -15), (-80, -6),
     (-81, 0), (-80, 5)],
    [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (37, 22), (43, 12), (51, 11), (48, 5), (41, -2),
     (40, -10), (35, -18), (32, -26), (28, -33), (20, -35), (15, -28),
     (12, -18), (13, -10), (9, 4), (4, 6), (-8, 5), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (5, 60), (5, 62), (12, 65), (18, 69), (25, 71), (32, 70),
     (40, 68), (45, 68), (55, 69), (65, 72), (75, 73), (85, 76),
     (95, 77), (105, 78), (115, 76), (125, 73), (135, 72), (145, 72),
     (155, 70), (162, 66), (170, 66), (178, 65), (178, 62), (170, 60),
     (162, 60), (158, 53), (150, 59), (142, 59), (142, 52), (140, 46),
     (135, 43), (130, 42), (127, 40), (122, 38), (120, 32), (122, 28),
     (118, 25), (110, 20), (108, 15), (105, 9), (103, 2), (100, 6),
     (98, 10), (95, 16), (92, 21), (89, 22), (86, 20), (80, 15),
     (76, 10), (74, 8), (72, 20), (68, 22), (66, 25), (62, 25),
     (58, 26), (56, 27), (54, 26), (52, 25), (50, 29), (48, 30),
     (44, 29), (40, 30), (36, 36), (30, 36), (27, 37), (26, 38),
     (23, 36), (22, 37), (19, 40), (16, 38), (12, 44), (8, 44),
     (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74), (-25, 76),
     (-35, 77), (-50, 75), (-55, 70), (-53, 64)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (140, 36), (141, 39),
     (141, 42), (140, 44), (138, 39), (135, 36), (132, 34)],
    [(167, -45), (170, -42), (174, -39), (176, -38), (178, -37),
     (174, -41), (170, -44)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (45, -25), (43, -22)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
]


def _in_poly(x, y, poly):
    """Ray-casting point-in-polygon test."""
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xint = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < xint:
                inside = not inside
    return inside


def build_map(dots_w, dots_h):
    """Dot world map, sampled from the continent outlines above."""
    dots = Image.new("RGBA", (dots_w, dots_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(dots)
    step_lon, step_lat = 3.0, 3.0
    lon = MAP_LON_MIN + step_lon / 2
    while lon < MAP_LON_MAX:
        lat = MAP_LAT_MIN + step_lat / 2
        while lat < MAP_LAT_MAX:
            if any(_in_poly(lon, lat, poly) for poly in LAND):
                x = (lon - MAP_LON_MIN) / (MAP_LON_MAX - MAP_LON_MIN) * dots_w
                y = (MAP_LAT_MAX - lat) / (MAP_LAT_MAX - MAP_LAT_MIN) * dots_h
                d.ellipse([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=DOT)
            lat += step_lat
        lon += step_lon
    return dots


def lonlat_to_xy(lon, lat, ox, oy, mw, mh):
    x = ox + (lon - MAP_LON_MIN) / (MAP_LON_MAX - MAP_LON_MIN) * mw
    y = oy + (MAP_LAT_MAX - lat) / (MAP_LAT_MAX - MAP_LAT_MIN) * mh
    return (x, y)


# ---------- build ----------

def verify_counts():
    """Region/field strips must match the stories actually on the page."""
    assert len(CARDS) == 16 and len(ALSO) == 36
    assert sum(c for _, c in REGIONS) == 52
    assert sum(c for _, _, c in FIELDS) == 52
    rc = {r: 0 for r, _ in REGIONS}
    fc = {k: 0 for k, _, _ in FIELDS}
    for card in CARDS:
        rc[card["region"]] += 1
        fc[card["field"]] += 1
    for _, region, field, _ in ALSO:
        rc[region] += 1
        fc[field] += 1
    for r, c in REGIONS:
        assert rc[r] == c, "region %s: %d != %d" % (r, rc[r], c)
    for k, _, c in FIELDS:
        assert fc[k] == c, "field %s: %d != %d" % (k, fc[k], c)
    print("counts verified: 52 stories, regions %s" % rc)


def main():
    verify_counts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top line (y 6) ----
    f_top = font(SANS_B, 9)
    d.text((MX, 6), "THE WORLD IN ONE DAY", font=f_top, fill=RED)
    tr = "52 STORIES \u00b7 EVERY CONTINENT \u00b7 ALL FROM THIS ONE DAY"
    d.text((W - MX - d.textlength(tr, font=f_top), 6), tr, font=f_top,
           fill=MUTED)

    # ---- masthead (y 18, auto-fit) ----
    masthead = "Thursday 19 November 2026"
    size = 56
    while size > 20:
        f_mast = font(SERIF_B, size)
        if d.textlength(masthead, font=f_mast) <= CW:
            break
        size -= 1
    d.text(((W - d.textlength(masthead, font=f_mast)) / 2, 18), masthead,
           font=f_mast, fill=INK)
    print("masthead size", size)

    # ---- kicker (y 76) ----
    kick = ("Trump, Xi and Putin share one table \u00b7 The World Court "
            "finds genocide in Myanmar \u00b7 COP31's draft drops fossil fuels")
    f_kick = font(SERIF, 13)
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, 76), kick,
           font=f_kick, fill=RED)

    # ---- rule + stats strip (y 97-131) ----
    d.line([MX, 97, W - MX, 97], fill=INK, width=1)
    scell_w = CW / 6.0
    for i, (num, lab) in enumerate(STATS):
        cx = MX + i * scell_w
        if i:
            d.line([cx, 103, cx, 127], fill=RULE, width=1)
        d.text((cx + 4, 101), num, font=font(SANS_B, 16), fill=INK)
        d.text((cx + 4, 121), lab, font=font(SANS, 7), fill=MUTED)

    # ---- region strip (y 135, h 22) ----
    ry = 135
    cell_w = CW / 7.0
    for i, (name, count) in enumerate(REGIONS):
        x0 = MX + i * cell_w
        d.rectangle([x0, ry, x0 + cell_w - 1, ry + 22],
                    fill=REGION_COL[name])
        t = "%s %d" % (name, count)
        f_r = font(SANS_B, 9)
        d.text((x0 + (cell_w - d.textlength(t, font=f_r)) / 2, ry + 6),
               t, font=f_r, fill=WHITE)

    # ---- field strip (y 159, h 18) ----
    fy = 159
    fcell_w = CW / 9.0
    for i, (_, label, count) in enumerate(FIELDS):
        x0 = MX + i * fcell_w
        d.rectangle([x0, fy, x0 + fcell_w - 1, fy + 18], fill=SLATE)
        t = "%s %d" % (label, count)
        f_f = font(SANS_B, 7)
        assert d.textlength(t, font=f_f) <= fcell_w - 4, \
            "field label too wide: %s" % t
        d.text((x0 + (fcell_w - d.textlength(t, font=f_f)) / 2, fy + 5),
               t, font=f_f, fill=WHITE)

    # ---- UTC timeline strip (y 181, h 28) ----
    ty = 181
    d.rectangle([MX, ty, MX + 86, ty + 28], fill=RED)
    d.text((MX + 8, ty + 3), "THE DAY", font=font(SANS_B, 8), fill=WHITE)
    d.text((MX + 8, ty + 14), "IN UTC", font=font(SANS_B, 8), fill=WHITE)
    slot_w = (CW - 88) / 8.0
    for i, (lab, text) in enumerate(TIMELINE):
        sx = MX + 88 + i * slot_w
        if i:
            d.line([sx, ty + 4, sx, ty + 24], fill=RULE, width=1)
        d.text((sx + 5, ty + 2), lab, font=font(SANS_B, 7), fill=RED_D)
        tl = wrap(d, text, font(SANS, 7), slot_w - 10)
        assert len(tl) <= 2, "timeline wraps %d: %s" % (len(tl), text)
        yy = ty + 12
        for ln in tl:
            d.text((sx + 5, yy), ln, font=font(SANS, 7), fill=INK)
            yy += 9

    # ---- large cards (y 213, h 190, 4 across) ----
    r1y, r1h = 213, 190
    cw1 = 236
    x = MX + 1
    for card in CARDS[0:4]:
        paint_card(img, d, x, r1y, cw1, r1h, card, 80, 13, 3, 8, 3, 8)
        x += cw1 + 6

    # ---- medium cards (y 409, h 150, 6 across) ----
    r2y, r2h = 409, 150
    cw2 = 156
    x = MX + 1
    for card in CARDS[4:10]:
        paint_card(img, d, x, r2y, cw2, r2h, card, 46, 11, 3, 7, 3, 7)
        x += cw2 + 5

    # ---- small cards (y 565, h 112, 6 across) ----
    r3y, r3h = 565, 112
    x = MX + 1
    for card in CARDS[10:16]:
        paint_card(img, d, x, r3y, cw2, r3h, card, 38, 10, 2, 7, 2, 7)
        x += cw2 + 5

    # ---- bottom section (y 683) ----
    by = 683
    # left column: WHERE IT HAPPENED
    d.text((MX, by), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=INK)
    d.line([MX, by + 16, MX + 300, by + 16], fill=RED, width=2)
    map_x, map_y, map_w, map_h = MX, by + 20, 300, 140
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=MAP_BG,
                outline=RULE, width=1)
    dots = build_map(296, 120)
    dots_x, dots_y = map_x + 2, map_y + 12
    img.paste(dots, (dots_x, dots_y), dots)
    for n, (lon, lat) in PINS.items():
        card = CARDS[n - 1]
        col = REGION_COL[card["region"]]
        px, py = lonlat_to_xy(lon, lat, dots_x, dots_y, 296, 120)
        dx, dy = PIN_OFFSET.get(n, (0, 0))
        if (dx, dy) != (0, 0):
            d.line([px, py, px + dx, py + dy], fill=col, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
            px, py = px + dx, py + dy
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=col,
                  outline=WHITE, width=1)
        d.text((px, py), str(n), font=font(SANS_B, 7), fill=WHITE,
               anchor="mm")
    # region legend
    ly = by + 164
    leg = [r for r, _ in REGIONS]
    for i, name in enumerate(leg):
        lx = MX + (i // 4) * 150
        lyy = ly + (i % 4) * 9
        d.ellipse([lx, lyy + 1, lx + 6, lyy + 7], fill=REGION_COL[name])
        d.text((lx + 10, lyy), name, font=font(SANS, 7), fill=INK)
    # HOW SURE box
    hy = by + 204
    d.rectangle([MX, hy, MX + 300, hy + 64], outline=RULE, width=1)
    d.text((MX + 8, hy + 6), "HOW SURE", font=font(SANS_B, 8), fill=RED)
    sure = [
        "CONFIRMED \u2014 on the record: officials, filings, results.",
        "CLAIM \u2014 one side\u2019s account, not independently verified.",
        "SOURCES \u2014 monitors or unnamed sources, via a news agency.",
    ]
    yy = hy + 19
    for ln in sure:
        d.text((MX + 8, yy), ln, font=font(SANS, 7), fill=INK)
        yy += 11
    d.text((MX + 8, hy + 52),
           "Numbered pin = stories 1\u201316 \u00b7 dot = a brief from the list.",
           font=font(SANS, 7), fill=MUTED)

    # right column: ALSO list
    rx = MX + 310
    rw = W - MX - rx
    d.text((rx, by), "ALSO ON THURSDAY 19 NOVEMBER \u2014 36 MORE STORIES",
           font=font(SANS_B, 11), fill=INK)
    d.line([rx, by + 16, rx + rw, by + 16], fill=RED, width=2)
    col_w = rw / 2.0
    f_also = font(SANS, 8)
    f_num = font(SANS_B, 8)
    for i, (n, region, _, text) in enumerate(ALSO):
        cx = rx + (i // 18) * col_w
        yy = by + 22 + (i % 18) * 12
        num = str(n)
        d.text((cx, yy), num, font=f_num, fill=REGION_COL[region])
        nw = d.textlength(num, font=f_num)
        assert d.textlength(text, font=f_also) <= col_w - nw - 8, \
            "also item too wide: %d %s" % (n, text)
        d.text((cx + nw + 4, yy), text, font=f_also, fill=INK)

    # numbers strip (right column, y 923-957)
    ny = by + 240
    d.line([rx, ny, rx + rw, ny], fill=RED, width=2)
    d.text((rx, ny + 6), "THE DAY IN", font=font(SANS_B, 7), fill=RED)
    d.text((rx, ny + 16), "NUMBERS", font=font(SANS_B, 7), fill=RED)
    ncell_w = (rw - 88) / 6.0
    for i, (num, lab) in enumerate(NUMBERS):
        cx = rx + 88 + i * ncell_w
        if i:
            d.line([cx, ny + 4, cx, ny + 30], fill=RULE, width=1)
        f_n = font(SANS_B, 13)
        d.text((cx + 4, ny + 2), num, font=f_n, fill=INK)
        ll = wrap(d, lab, font(SANS, 6), ncell_w - 8)
        assert len(ll) <= 2, "number label wraps %d: %s" % (len(ll), lab)
        yy = ny + 19
        for ln in ll:
            d.text((cx + 4, yy), ln, font=font(SANS, 6), fill=MUTED)
            yy += 8

    # ---- DATE CHECK box (y 963, h 46) ----
    dy = 963
    d.rectangle([MX, dy, W - MX, dy + 46], outline=RED, width=2)
    d.rectangle([MX, dy, MX + 92, dy + 46], fill=RED)
    d.text((MX + 46, dy + 23), "DATE CHECK", font=font(SANS_B, 9),
           fill=WHITE, anchor="mm")
    dc = wrap(d, DATE_CHECK, font(SANS, 7), W - MX - 130 - 8)
    assert len(dc) <= 5, "date check wraps %d" % len(dc)
    yy = dy + (46 - len(dc) * 10) // 2
    for ln in dc:
        d.text((MX + 100, yy), ln, font=font(SANS, 7), fill=INK)
        yy += 10

    # ---- footer (y 1013) ----
    f_foot = font(SANS, 7)
    assert d.textlength(FOOTER, font=f_foot) <= CW, "footer too wide"
    d.text((MX, 1013), FOOTER, font=f_foot, fill=MUTED)

    img.save(HERE / "entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
