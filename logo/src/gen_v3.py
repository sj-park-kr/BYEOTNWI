import math, random
import gen
from gen import word, P, sub, AMBER, GOLD, CORE, D

W, H = 1600, 560


def crack(nx, top, bot, slant, wmax, seed, scale=1.0):
    """irregular hairline crack polygon: nearly closed at top, widest a bit below middle."""
    r = random.Random(seed)
    n = 22
    L, R = [], []
    zig = 0
    for i in range(n + 1):
        t = i / n
        y = top + (bot - top) * t
        zig = zig * 0.4 + r.uniform(-2.6, 2.6) if 0 < i < n else 0
        x = nx + slant * (0.5 - t) + zig
        w = (0.5 + wmax * math.sin(math.pi * min(1, t * 0.95 + 0.02)) ** 1.6 * (0.75 + 0.25 * t)) * scale
        L.append((x - w / 2 * r.uniform(0.7, 1.3), y))
        R.append((x + w / 2 * r.uniform(0.7, 1.3), y))
    pts = L + R[::-1]
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)


def build(light=False):
    bg, ink = ("#F4EEE3", "#15120F") if light else ("#0B0A09", "#F2EBDD")
    gen.BG, gen.INK = bg, ink
    size, cx = 340, W / 2
    capH = 1760 / 2048 * size
    top = 66
    base = top + capH
    gl = word("anton", "BYEONNWI", size, cx, base, 0.02, {4: -33})
    nx = (gl[4][2] + gl[5][1]) / 2  # joint of the two N stems
    slant = 22
    ck = crack(nx, top, base, slant, 13, 7)
    core = crack(nx, top + capH * 0.1, base - capH * 0.06, slant, 4.5, 7, 1.0)
    cy = top + capH * 0.55

    # volumetric rays: from points along the crack, flowing down-left/down, soft and fading
    r = random.Random(3)
    rays = []
    for k in range(13):
        t = r.uniform(0.25, 0.95)
        sx = nx + slant * (0.5 - t)
        sy = top + capH * t
        ang = math.radians(r.uniform(92, 128))  # from +x axis, downward
        ln = r.uniform(220, 400)
        w0, w1 = r.uniform(1.5, 4), r.uniform(22, 80)
        ex, ey = sx + math.cos(ang) * ln, sy + math.sin(ang) * ln
        px, py = -math.sin(ang), math.cos(ang)
        pts = [(sx + px * w0, sy + py * w0), (sx - px * w0, sy - py * w0), (ex - px * w1, ey - py * w1), (ex + px * w1, ey + py * w1)]
        op = r.uniform(0.14, 0.38)
        rays.append((pts, sx, sy, ex, ey, op, r.choice([3, 6, 10, 16])))
    rdefs = "".join(
        f'<linearGradient id="r{i}" gradientUnits="userSpaceOnUse" x1="{sx:.0f}" y1="{sy:.0f}" x2="{ex:.0f}" y2="{ey:.0f}">'
        f'<stop offset="0" stop-color="{GOLD}" stop-opacity="{op:.2f}"/><stop offset=".5" stop-color="{AMBER}" stop-opacity="{op*0.45:.2f}"/>'
        f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>'
        f'<filter id="b{i}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{bl}"/></filter>'
        for i, (pts, sx, sy, ex, ey, op, bl) in enumerate(rays))
    rbody = "".join(
        f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="url(#r{i})" filter="url(#b{i})"/>'
        for i, (pts, *_rest) in enumerate(rays))

    # dust motes inside the light cone
    dust = ""
    for _ in range(46):
        d = r.uniform(30, 300)
        a = math.radians(r.uniform(98, 124))
        x = nx + math.cos(a) * d + r.uniform(-25, 25)
        y = cy + math.sin(a) * d
        o = max(0.0, 0.75 - d / 520) * r.uniform(0.4, 1)
        dust += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(0.6, 2.0):.1f}" fill="{CORE}" opacity="{o:.2f}"/>'

    blend = "normal" if light else "screen"
    letters = P(gl)
    defs = f'''
  <clipPath id="lt">{letters}</clipPath>
  <mask id="cut"><rect width="{W}" height="{H}" fill="#fff"/><polygon points="{ck}" fill="#000"/></mask>
  <radialGradient id="refl" cx="{nx:.0f}" cy="{cy:.0f}" r="{230 if light else 260}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{GOLD}" stop-opacity="{.55 if light else .5}"/>
    <stop offset=".35" stop-color="{AMBER}" stop-opacity="{.18 if light else .16}"/>
    <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>
  <linearGradient id="ckg" gradientUnits="userSpaceOnUse" x1="0" y1="{top:.0f}" x2="0" y2="{base:.0f}">
    <stop offset="0" stop-color="{AMBER}"/><stop offset=".55" stop-color="{GOLD}"/><stop offset="1" stop-color="{AMBER}"/></linearGradient>
  <filter id="f2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2"/></filter>
  <filter id="f6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>
  <filter id="f30" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="34"/></filter>
  {rdefs}'''
    body = f'''<ellipse cx="{nx:.0f}" cy="{cy:.0f}" rx="70" ry="{capH*0.55:.0f}" fill="{AMBER}" opacity="{.25 if light else .35}" filter="url(#f30)"/>
<g>
  {P(gl, fill=ink)}
  <g clip-path="url(#lt)">
    <rect width="{W}" height="{H}" fill="url(#refl)"/>
    <polygon points="{ck}" fill="none" stroke="{CORE}" stroke-width="14" opacity=".6" filter="url(#f6)"/>
  </g>
</g>
<polygon points="{ck}" fill="{GOLD}" stroke="{GOLD}" stroke-width="12" filter="url(#f6)" opacity=".55"/>
<polygon points="{ck}" fill="{CORE}" stroke="{CORE}" stroke-width="3" filter="url(#f2)"/>
<polygon points="{core}" fill="#FFFBEA" filter="url(#f2)"/>
<g style="mix-blend-mode:{blend}">{rbody}{dust}</g>
{sub(cx, base + 104, size=34)}'''
    out = gen.svg(body, defs, W, H)
    gen.BG, gen.INK = "#0B0A09", "#F2EBDD"
    return out, nx, cy


if __name__ == "__main__":
    s, nx, cy = build()
    open(D + "byeonnwi_a_gap_v3.svg", "w").write(s)
    open(D + "byeonnwi_a_gap_light_v3.svg", "w").write(build(True)[0])
    print(f"{nx:.0f} {cy:.0f}")
