# Original cover art for Bridge Squad: Endless (1200x630). Pure vector, generated.
# Art direction matches the game: dusk navy sky and sea, a pale deck with yellow/black kerbs and a chevron belt,
# glass gates with white frames, glossy blue/white title type with a dark lip, horned red horde in five colours.
import math, random
random.seed(11)
W, H = 1200, 630
def lerp(a, b, t): return a + (b - a) * t
VX, VY = 790, 150                      # vanishing point of the deck
def bx(u, v):                          # u 0..1 across the deck, v 0 near .. 1 far
    return lerp(lerp(440, VX - 52, v), lerp(1180, VX + 52, v), u)
def by(v): return lerp(H + 10, VY, max(v, 0) ** 0.72)
def sc(v): return lerp(1.0, 0.12, max(v, 0) ** 0.72)

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', '''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050f2e"/><stop offset=".6" stop-color="#0d2660"/><stop offset="1" stop-color="#2a4f9c"/></linearGradient>
<radialGradient id="haze" cx=".66" cy=".25" r=".5"><stop offset="0" stop-color="#7fb4ff" stop-opacity=".55"/><stop offset="1" stop-color="#7fb4ff" stop-opacity="0"/></radialGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b2458"/><stop offset="1" stop-color="#020a22"/></linearGradient>
<linearGradient id="deck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9c4dc"/><stop offset="1" stop-color="#eef2fa"/></linearGradient>
<linearGradient id="belt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a6680"/><stop offset="1" stop-color="#8a94aa"/></linearGradient>
<linearGradient id="kerb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7d89a6"/><stop offset="1" stop-color="#c9d2e6"/></linearGradient>
<pattern id="stripe" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="22" height="22" fill="#ffc61a"/><rect width="11" height="22" fill="#1a1a1a"/></pattern>
<radialGradient id="blue" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#d6ecff"/><stop offset=".4" stop-color="#3d8dff"/><stop offset="1" stop-color="#0e3aa8"/></radialGradient>
<radialGradient id="r0" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ff9a8a"/><stop offset=".45" stop-color="#e0222e"/><stop offset="1" stop-color="#6a0810"/></radialGradient>
<radialGradient id="r1" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#d0a8ff"/><stop offset=".45" stop-color="#7a28d8"/><stop offset="1" stop-color="#2c0a5a"/></radialGradient>
<radialGradient id="r2" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffe2a0"/><stop offset=".45" stop-color="#f0a010"/><stop offset="1" stop-color="#7a4200"/></radialGradient>
<radialGradient id="r3" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#c8ffb0"/><stop offset=".45" stop-color="#4cc81e"/><stop offset="1" stop-color="#155a06"/></radialGradient>
<radialGradient id="r4" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffb4ec"/><stop offset=".45" stop-color="#e02aa8"/><stop offset="1" stop-color="#5a0a44"/></radialGradient>
<linearGradient id="gB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4d8cff" stop-opacity=".92"/><stop offset="1" stop-color="#0a2fb8" stop-opacity=".92"/></linearGradient>
<linearGradient id="gP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a45cff" stop-opacity=".92"/><stop offset="1" stop-color="#4a10b0" stop-opacity=".92"/></linearGradient>
<linearGradient id="gR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a5a" stop-opacity=".92"/><stop offset="1" stop-color="#b00a14" stop-opacity=".92"/></linearGradient>
<linearGradient id="gG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3ce08a" stop-opacity=".92"/><stop offset="1" stop-color="#067a3e" stop-opacity=".92"/></linearGradient>
<linearGradient id="gO" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc040" stop-opacity=".95"/><stop offset="1" stop-color="#d86a00" stop-opacity=".95"/></linearGradient>
<linearGradient id="tt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#e6f2ff"/><stop offset="1" stop-color="#9ccaff"/></linearGradient>
<linearGradient id="pill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fd4ff"/><stop offset=".48" stop-color="#2b8cff"/><stop offset="1" stop-color="#155be8"/></linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3460c8"/><stop offset="1" stop-color="#0e2268"/></linearGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000a2a" flood-opacity=".5"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>''']
o.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/><rect width="{W}" height="{H}" fill="url(#haze)"/>')
for i in range(40):                     # stars
    o.append(f'<circle cx="{random.uniform(0, W):.0f}" cy="{random.uniform(0, 140):.0f}" r="{random.uniform(.6, 1.6):.1f}" fill="#cfe2ff" opacity="{random.uniform(.25, .8):.2f}"/>')
o.append(f'<rect y="{VY + 30}" width="{W}" height="{H - VY - 30}" fill="url(#sea)"/>')
for i in range(110):                    # water glints
    y = random.uniform(VY + 36, H); x = random.uniform(0, W); k = (y - VY) / (H - VY)
    o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{random.uniform(8, 50) * k + 3:.0f}" height="{max(1.2, 3 * k):.1f}" rx="1" fill="#8fc0ff" opacity="{random.uniform(.12, .4):.2f}"/>')
# piers under the deck
for v in [0.05, 0.28, 0.5, 0.7]:
    x0, x1, y, s = bx(.3, v), bx(.7, v), by(v), sc(v)
    o.append(f'<rect x="{x0:.0f}" y="{y:.0f}" width="{x1 - x0:.0f}" height="{140 * s + 24:.0f}" fill="#081738" opacity=".9"/>')
poly = lambda pts, fill, extra='': o.append('<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + f'" fill="{fill}" {extra}/>')
# deck, kerbs with hazard stripes, belt with chevrons
poly([(bx(0, 0), by(0)), (bx(0, 1), by(1)), (bx(1, 1), by(1)), (bx(1, 0), by(0))], 'url(#deck)')
for u0, u1 in [(-0.035, 0.0), (1.0, 1.035)]:
    poly([(bx(u0, 0), by(0)), (bx(u0, 1), by(1)), (bx(u1, 1), by(1)), (bx(u1, 0), by(0))], 'url(#kerb)')
    poly([(bx(u0, 0), by(0)), (bx(u0, 1), by(1)), (bx(u0 + .012, 1), by(1)), (bx(u0 + .012, 0), by(0))], 'url(#stripe)', 'opacity=".9"')
poly([(bx(.73, 0), by(0)), (bx(.73, 1), by(1)), (bx(.95, 1), by(1)), (bx(.95, 0), by(0))], 'url(#belt)')
for k in range(26):
    v = k / 26; y = by(v); s = sc(v); cx = bx(.84, v); w = 40 * s
    o.append(f'<polyline points="{cx - w:.1f},{y - w * .45:.1f} {cx:.1f},{y:.1f} {cx + w:.1f},{y - w * .45:.1f}" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="{6 * s:.1f}" stroke-linejoin="round"/>')
for k in range(18):                    # lane lights along the kerbs
    v = k / 18 + .02
    for u in (-.018, 1.018):
        o.append(f'<circle cx="{bx(u, v):.1f}" cy="{by(v) - 6 * sc(v):.1f}" r="{5 * sc(v) + .6:.1f}" fill="#ffe680"/>')
for k in range(14):
    v = k / 14 + .02; v2 = v + .028
    o.append(f'<line x1="{bx(.42, v):.0f}" y1="{by(v):.0f}" x2="{bx(.42, v2):.0f}" y2="{by(v2):.0f}" stroke="#fff" stroke-opacity=".8" stroke-width="{5 * sc(v):.1f}"/>')

def critter(x, y, s, grad, horns=True):  # a horned horde member: body, head, two cream horns, yellow eyes
    r = 13 * s
    g = f'<g transform="translate({x:.1f},{y:.1f})">'
    g += f'<ellipse cx="0" cy="{-r * .9:.1f}" rx="{r * .82:.1f}" ry="{r * .95:.1f}" fill="url(#{grad})"/>'
    g += f'<circle cx="0" cy="{-r * 2.05:.1f}" r="{r * .72:.1f}" fill="url(#{grad})"/>'
    if horns and s > .25:
        g += f'<path d="M{-r * .45:.1f},{-r * 2.5:.1f} L{-r * .7:.1f},{-r * 3.2:.1f} L{-r * .15:.1f},{-r * 2.62:.1f} Z M{r * .45:.1f},{-r * 2.5:.1f} L{r * .7:.1f},{-r * 3.2:.1f} L{r * .15:.1f},{-r * 2.62:.1f} Z" fill="#fff0c8"/>'
        g += f'<rect x="{-r * .42:.1f}" y="{-r * 2.12:.1f}" width="{r * .3:.1f}" height="{r * .14:.1f}" fill="#ffd23a"/><rect x="{r * .12:.1f}" y="{-r * 2.12:.1f}" width="{r * .3:.1f}" height="{r * .14:.1f}" fill="#ffd23a"/>'
    return g + '</g>'
def soldier(x, y, s):
    r = 15 * s
    return (f'<g transform="translate({x:.1f},{y:.1f})"><ellipse cx="0" cy="{-r * .85:.1f}" rx="{r * .8:.1f}" ry="{r * .9:.1f}" fill="url(#blue)"/>'
            f'<circle cx="0" cy="{-r * 1.95:.1f}" r="{r * .7:.1f}" fill="url(#blue)"/><path d="M{-r * .66:.1f},{-r * 2.05:.1f} A{r * .7:.1f},{r * .7:.1f} 0 0 1 {r * .66:.1f},{-r * 2.05:.1f} Z" fill="#ffffff" opacity=".9"/></g>')

# the horde: bands of the five enemy colours on the far half of the deck
horde = []
for v in [i / 70 for i in range(28, 66)]:
    band = 'r0' if v > .78 or v < .5 else ('r1' if v > .7 else 'r2' if v > .62 else 'r3' if v > .56 else 'r4')
    for u in [j / 26 for j in range(1, 18)]:
        if random.random() < .9: horde.append((u + random.uniform(-.012, .012), v + random.uniform(-.004, .004), band))
horde.sort(key=lambda p: -p[1])
o.append('<g>' + ''.join(critter(bx(u, v), by(v), sc(v) * (1.35 if g == 'r1' else 1), g) for u, v, g in horde) + '</g>')
# the boss stands in the horde
bv = .5; bxx, byy, bs = bx(.32, bv), by(bv), sc(bv) * 6.2
o.append('<g filter="url(#sh)">' + critter(bxx, byy, bs, 'r0') + '</g>')

# gates on the belt (near -> far drawn far first)
def gate(v, txt, grad, edge, sub=None, fill='#fff'):
    x, y, s = bx(.84, v), by(v), sc(v); w, h = 158 * s, 78 * s
    g = f'<g filter="url(#sh)"><rect x="{x - w / 2:.1f}" y="{y - h - 14 * s:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{15 * s:.1f}" fill="url(#{grad})" stroke="#fff" stroke-width="{5.5 * s:.1f}"/>'
    ty = y - 14 * s - h * (.42 if sub else .26)
    g += f'<text x="{x:.1f}" y="{ty:.1f}" font-family="Arial Black,Impact,sans-serif" font-weight="900" font-size="{(36 if sub else 48) * s:.1f}" text-anchor="middle" fill="{fill}" stroke="{edge}" stroke-width="{7 * s:.1f}" paint-order="stroke" stroke-linejoin="round">{txt}</text>'
    if sub:
        g += f'<rect x="{x - w * .38:.1f}" y="{y - 14 * s - h * .34:.1f}" width="{w * .76:.1f}" height="{h * .24:.1f}" rx="{h * .12:.1f}" fill="#fff"/><text x="{x:.1f}" y="{y - 14 * s - h * .16:.1f}" font-family="Arial Black,Impact,sans-serif" font-weight="900" font-size="{13 * s:.1f}" text-anchor="middle" fill="{edge}">{sub}</text>'
    o.append(g + '</g>')
for v, t, g, e, sub, f in [(.66, '+2', 'gB', '#0b41c4', None, '#fff'), (.57, '?', 'gB', '#2a2f52', 'SHOOT IT', '#ffd23a'), (.47, '−10', 'gR', '#8f0a14', None, '#fff'),
                           (.36, 'ROCKETS', 'gG', '#04603a', 'WEAPON', '#fff'), (.24, '×2', 'gP', '#4e0c9c', None, '#fff'), (.1, '+50', 'gO', '#a04e00', None, '#fff')]:
    gate(v, t, g, e, sub, f)
# rockets from the squad into the horde
for i in range(9):
    u0 = random.uniform(.45, .68); x0, y0 = bx(u0, .17), by(.17) - 40
    t = random.uniform(.35, .7); tx, ty = bx(.32, .5), by(.5) - 60
    x1, y1 = lerp(x0, tx, t), lerp(y0, ty, t); x2, y2 = lerp(x0, tx, t - .1), lerp(y0, ty, t - .1)
    o.append(f'<line x1="{x2:.0f}" y1="{y2:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="#ffb040" stroke-width="7" stroke-linecap="round" opacity=".55" filter="url(#glow)"/><line x1="{x2:.0f}" y1="{y2:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="#fff2c0" stroke-width="3" stroke-linecap="round"/>')
# the squad, near the camera
sq = []
for i in range(64):
    a = i * 2.39996; r = (i ** .5) * .0125
    sq.append((.56 + r * 1.25 * math.cos(a), .13 + r * .55 * math.sin(a)))
sq.sort(key=lambda p: -p[1])
o.append('<g filter="url(#sh)">' + ''.join(soldier(bx(u, v), by(v), sc(v) * 1.5) for u, v in sq) + '</g>')
# squad counter pill, as in the game
px, py = bx(.56, .06), by(.06) - 8
o.append(f'<g filter="url(#sh)"><rect x="{px - 62}" y="{py - 26}" width="124" height="46" rx="23" fill="url(#pill)" stroke="#fff" stroke-width="5"/><text x="{px + 10:.0f}" y="{py + 10:.0f}" font-family="Arial Black,Impact,sans-serif" font-weight="900" font-size="30" text-anchor="middle" fill="#fff" stroke="#0b3ea8" stroke-width="6" paint-order="stroke">248</text><circle cx="{px - 36:.0f}" cy="{py - 3:.0f}" r="13" fill="#0b3ea8"/></g>')

# title block, in the game's title style
o.append('<g font-family="Arial Black,Impact,sans-serif" font-weight="900">')
for txt, y in [('BRIDGE', 178), ('SQUAD', 290)]:
    o.append(f'<text x="62" y="{y + 8}" font-size="112" fill="#061a52" stroke="#061a52" stroke-width="18" stroke-linejoin="round" letter-spacing="-1">{txt}</text>')
    o.append(f'<text x="62" y="{y}" font-size="112" fill="url(#tt)" stroke="#1546b8" stroke-width="16" stroke-linejoin="round" paint-order="stroke" letter-spacing="-1">{txt}</text>')
o.append('<g filter="url(#sh)"><rect x="64" y="322" width="352" height="62" rx="20" fill="url(#pill)" stroke="#fff" stroke-width="5"/>'
         '<text x="240" y="364" font-size="31" text-anchor="middle" fill="#fff" stroke="#0b3ea8" stroke-width="6" paint-order="stroke" letter-spacing="1">ENDLESS LEVELS</text></g>')
for i, (a, b) in enumerate([('THE BRIDGE', '9 WEAPONS · 10 WORLDS'), ('FLOOD RESCUE', 'PUMP · TANK · HEROES')]):
    x = 64 + i * 182
    o.append(f'<g filter="url(#sh)"><rect x="{x}" y="404" width="170" height="74" rx="16" fill="url(#card)" stroke="#fff" stroke-width="4"/>'
             f'<text x="{x + 85}" y="436" font-size="19" text-anchor="middle" fill="#fff">{a}</text>'
             f'<text x="{x + 85}" y="460" font-family="Arial,sans-serif" font-weight="800" font-size="11.5" text-anchor="middle" fill="#cfe6ff">{b}</text></g>')
o.append('</g></svg>')
open('cover.svg', 'w').write('\n'.join(o))
print('ok')
