from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import math, os

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
F = {k: TTFont(D + f"fonts/{k}.woff2") for k in ["anton", "archivo", "bebas", "notokr"]}

BG, INK, AMBER, GOLD, CORE = "#0B0A09", "#F2EBDD", "#FF9F1C", "#FFC93C", "#FFF1C1"


def glyphs(font, text, size, x, base, track=0.0, gaps=None):
    """returns list of (path_d, x0, x1) per char, baseline at `base`."""
    f = F[font]; upm = f["head"].unitsPerEm; s = size / upm
    gs, cm, hm = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    out = []
    for i, ch in enumerate(text):
        g = cm[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, base)))
        adv = hm[g][0] * s
        out.append((pen.getCommands(), x, x + adv))
        x += adv + track * size + (gaps or {}).get(i, 0)
    return out


def width(font, text, size, track=0.0, gaps=None):
    g = glyphs(font, text, size, 0, 0, track, gaps)
    return g[-1][2]


def word(font, text, size, cx, base, track=0.0, gaps=None):
    w = width(font, text, size, track, gaps)
    return glyphs(font, text, size, cx - w / 2, base, track, gaps)


def P(gl, **a):
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items())
    return f'<path d="{" ".join(g[0] for g in gl)}" {attrs}/>'


def defs_common():
    return f'''
  <linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GOLD}" stop-opacity=".0"/>
    <stop offset=".45" stop-color="{GOLD}" stop-opacity=".55"/>
    <stop offset=".5" stop-color="{CORE}" stop-opacity="1"/>
    <stop offset=".55" stop-color="{GOLD}" stop-opacity=".55"/>
    <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
  <filter id="glow2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>'''


def svg(body, defs, w=1600, h=900):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>{defs_common()}{defs}
</defs>
<rect width="{w}" height="{h}" fill="{BG}"/>
{body}
</svg>'''


def sub(cx, y, size=30, track=0.42, color=AMBER, ko=True):
    # "볕뉘 · SUNFLECK" tagline
    t = "SUNFLECK"
    wl = width("anton", t, size, track) - track * size
    kw = width("notokr", "볕뉘", size * 1.05, 0.05) if ko else 0
    gap = 46 if ko else 0
    total = kw + gap + wl
    x0 = cx - total / 2
    s = ""
    if ko:
        s += P(glyphs("notokr", "볕뉘", size * 1.05, x0, y + 1, 0.05), fill=INK)
        s += f'<circle cx="{x0 + kw + gap / 2:.1f}" cy="{y - size * .36:.1f}" r="4" fill="{AMBER}"/>'
    s += P(glyphs("anton", t, size, x0 + kw + gap, y, track), fill=color)
    return s


def rot_slit(cx, cy, w, h, ang):
    """slanted thin rectangle (parallelogram) centered at cx,cy; ang=deg from vertical"""
    t = math.tan(math.radians(ang)) * h / 2
    pts = [(cx - w / 2 + t, cy - h / 2), (cx + w / 2 + t, cy - h / 2), (cx + w / 2 - t, cy + h / 2), (cx - w / 2 - t, cy + h / 2)]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


# ---------- A: THE GAP (Anton) ----------
def concept_a(light=False):
    global BG, INK
    BG, INK = ("#F4EEE3", "#15120F") if light else ("#0B0A09", "#F2EBDD")
    size, base, cx = 300, 520, 800
    track = 0.02
    gi = 4  # gap after index 4 (O) -> between O|N? we want N|N: indices B0 Y1 E2 O3 N4 N5 W6 I7
    gl = word("anton", "BYEONNWI", size, cx, base, track, {4: 28})
    nx = (gl[4][2] + gl[5][1]) / 2 + 14  # center of NN gap
    capH = 1760 / 2048 * size
    cy = base - capH / 2
    ang = 16
    slit = rot_slit(nx, cy, 16, capH + 260, ang)
    # beam: wide fan behind the slit, along the slit direction, spilling down-right
    dx = math.tan(math.radians(ang))
    bx, by = nx - dx * capH / 2, cy + capH / 2
    L = 900 - by
    fan = f"{bx - 4:.0f},{by:.0f} {bx + 4:.0f},{by:.0f} {bx - dx*L + 240:.0f},900 {bx - dx*L - 300:.0f},900"
    defs = f'''
  <mask id="cutA"><rect width="1600" height="900" fill="#fff"/><polygon points="{slit}" fill="#000"/></mask>
  <linearGradient id="fanA" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GOLD}" stop-opacity=".75"/>
    <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="warmA" cx="{nx:.0f}" cy="{cy:.0f}" r="{260 if light else 420}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{AMBER if light else GOLD}"/><stop offset=".35" stop-color="{'#5A3A12' if light else '#F7D9A0'}"/><stop offset="1" stop-color="{INK}"/>
  </radialGradient>'''
    body = f'''<polygon points="{fan}" fill="url(#fanA)" filter="url(#glow)" opacity="{.3 if light else .6}"/>
<g mask="url(#cutA)">{P(gl, fill="url(#warmA)")}</g>
<polygon points="{rot_slit(nx, cy, 10, capH + 40, ang)}" fill="{GOLD}" filter="url(#glow2)"/>
<polygon points="{rot_slit(nx, cy, 3, capH + 10, ang)}" fill="{CORE}"/>
{sub(cx, base + 130)}'''
    out = svg(body, defs)
    BG, INK = "#0B0A09", "#F2EBDD"
    return out


# ---------- B: SLICE (Archivo Black) ----------
def concept_b():
    size, base, cx = 205, 515, 800
    gl = word("archivo", "BYEONNWI", size, cx, base, -0.01)
    capH = 688 / 1000 * size
    cy = base - capH / 2
    x0, x1 = gl[0][1] - 40, gl[-1][2] + 40
    # one diagonal slit across the whole word: line from (x0, cy+30) to (x1, cy-30)
    sl = 9  # slit half-thickness
    a, b = (x0 - 200, cy + 55), (x1 + 200, cy - 55)
    up = f"0,0 1600,0 1600,{b[1]-sl:.1f} 0,{a[1]-sl + (0-a[0])*(b[1]-a[1])/(b[0]-a[0]):.1f}"
    lo = f"0,900 1600,900 1600,{b[1]+sl:.1f} 0,{a[1]+sl + (0-a[0])*(b[1]-a[1])/(b[0]-a[0]):.1f}"
    ly = lambda x: a[1] + (x - a[0]) * (b[1] - a[1]) / (b[0] - a[0])
    defs = f'''
  <clipPath id="upB"><polygon points="{up}"/></clipPath>
  <clipPath id="loB"><polygon points="{lo}"/></clipPath>
  <linearGradient id="lineB" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{AMBER}" stop-opacity="0"/><stop offset=".25" stop-color="{AMBER}"/>
    <stop offset=".6" stop-color="{CORE}"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>'''
    L = f'x1="{x0-120:.0f}" y1="{ly(x0-120):.1f}" x2="{x1+120:.0f}" y2="{ly(x1+120):.1f}"'
    body = f'''<line {L} stroke="{AMBER}" stroke-width="60" opacity=".35" filter="url(#glow)"/>
<g clip-path="url(#upB)" transform="translate(-10,-5)">{P(gl, fill=INK)}</g>
<g clip-path="url(#loB)" transform="translate(10,5)">{P(gl, fill=INK)}</g>
<line {L} stroke="url(#lineB)" stroke-width="14" filter="url(#glow2)"/>
<line {L} stroke="url(#lineB)" stroke-width="3"/>
{sub(cx, base + 125)}'''
    return svg(body, defs)


# ---------- C: SUNFLECK O (Bebas Neue) ----------
def concept_c():
    size, base, cx = 380, 560, 800
    gl = word("bebas", "BYEONNWI", size, cx, base, 0.03)
    capH = 700 / 1000 * size
    o = gl[3]; ox = (o[1] + o[2]) / 2 - 0.5; oy = base - capH / 2
    fleck = (ox, oy)
    ang = 28  # beam enters from upper-right through a slit in the O
    defs = f'''
  <radialGradient id="sunC" cx="{ox:.0f}" cy="{oy:.0f}" r="70" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{CORE}"/><stop offset=".45" stop-color="{GOLD}"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>
  <mask id="cutC"><rect width="1600" height="900" fill="#fff"/>
    <polygon points="{rot_slit(ox + 6 + math.tan(math.radians(ang))*capH*0.44, oy - capH*0.44, 13, 120, ang)}" fill="#000"/></mask>
  <linearGradient id="rayC" x1="1" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD}" stop-opacity=".85"/><stop offset="1" stop-color="{CORE}"/></linearGradient>'''
    t = math.tan(math.radians(ang))
    ray = f"{ox:.0f},{oy:.0f} {ox + 12:.0f},{oy:.0f} {ox + 40 + t*440:.0f},{oy - 440:.0f} {ox - 20 + t*440:.0f},{oy - 440:.0f}"
    body = f'''<polygon points="{ray}" fill="url(#rayC)" filter="url(#glow2)"/>
<g mask="url(#cutC)">{P(gl, fill=INK)}</g>
<ellipse cx="{ox:.0f}" cy="{oy:.0f}" rx="58" ry="110" fill="url(#sunC)" filter="url(#glow2)"/>
<circle cx="{ox:.0f}" cy="{oy:.0f}" r="20" fill="{CORE}"/>
{sub(cx, base + 115)}'''
    return svg(body, defs)


open(D + "byeonnwi_a_gap_light.svg", "w").write(concept_a(True))
for n, f in [("a_gap", concept_a), ("b_slice", concept_b), ("c_sunfleck", concept_c)]:
    open(D + f"byeonnwi_{n}.svg", "w").write(f())
print("ok")
