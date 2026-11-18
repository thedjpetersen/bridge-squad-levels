# Original cover art for the Bridge Squad levels kit (1200x630). Pure vector, generated.
import random; random.seed(7)
W,H=1200,630
# bridge in perspective: vanishing toward (760,150); bottom edge spans x 430..1130 at y=630
def lerp(a,b,t): return a+(b-a)*t
def bridge_x(u,v):  # u: 0..1 across deck (left->right), v: 0 bottom .. 1 far
    xl=lerp(430,712,v); xr=lerp(1130,808,v); return lerp(xl,xr,u)
def bridge_y(v): return lerp(630,150,max(v,0)**0.75)
def scale(v): return lerp(1.0,0.14,max(v,0)**0.75)
o=[]
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
o.append('''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d0b3a"/><stop offset=".45" stop-color="#7a1d4f"/><stop offset=".78" stop-color="#e2553a"/><stop offset="1" stop-color="#ffb347"/></linearGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a1240"/><stop offset="1" stop-color="#0b1030"/></linearGradient>
<linearGradient id="deck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9c9b8"/><stop offset="1" stop-color="#f4ece6"/></linearGradient>
<linearGradient id="belt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6c6680"/><stop offset="1" stop-color="#8d8aa0"/></linearGradient>
<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff4c2"/><stop offset=".5" stop-color="#ffcf5a" stop-opacity=".9"/><stop offset="1" stop-color="#ff8a3a" stop-opacity="0"/></radialGradient>
<radialGradient id="blue" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#bfe3ff"/><stop offset=".45" stop-color="#2f7bff"/><stop offset="1" stop-color="#0b2f9a"/></radialGradient>
<radialGradient id="red" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#ffb09a"/><stop offset=".5" stop-color="#e3262b"/><stop offset="1" stop-color="#7a0a14"/></radialGradient>
<linearGradient id="gGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe680"/><stop offset="1" stop-color="#f08a00"/></linearGradient>
<linearGradient id="gPurp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2a8ff"/><stop offset="1" stop-color="#7b1fd6"/></linearGradient>
<linearGradient id="gRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff9a9a"/><stop offset="1" stop-color="#c8101e"/></linearGradient>
<linearGradient id="gBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8d4ff"/><stop offset="1" stop-color="#1f5fe0"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#1a0420" flood-opacity=".55"/></filter>
</defs>''')
o.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
o.append('<circle cx="760" cy="170" r="150" fill="url(#sun)"/>')
o.append(f'<rect y="200" width="{W}" height="{H-200}" fill="url(#sea)"/>')
for i in range(70):  # water glints
    y=random.uniform(215,620); x=random.uniform(0,W); w=random.uniform(10,60)*(y-180)/440
    o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{max(1.5,(y-180)/180):.1f}" rx="1" fill="#ff9a6a" opacity="{random.uniform(.15,.45):.2f}"/>')
# piers
for v in [0.08,0.3,0.52,0.72]:
    xl=bridge_x(0,v); xr=bridge_x(1,v); y=bridge_y(v); s=scale(v)
    o.append(f'<rect x="{lerp(xl,xr,.3):.0f}" y="{y:.0f}" width="{(xr-xl)*.4:.0f}" height="{120*s+30:.0f}" fill="#2a0f2e" opacity=".75"/>')
# deck
pts=[(bridge_x(0,0),bridge_y(0)),(bridge_x(0,1),bridge_y(1)),(bridge_x(1,1),bridge_y(1)),(bridge_x(1,0),bridge_y(0))]
o.append('<polygon points="'+' '.join(f'{x:.0f},{y:.0f}' for x,y in pts)+'" fill="url(#deck)"/>')
# barriers
for u,c in [(0,'#b08a8a'),(1,'#b08a8a')]:
    o.append(f'<polygon points="{bridge_x(u,0)-(14 if u==0 else -14):.0f},{H} {bridge_x(u,0):.0f},{H} {bridge_x(u,1):.0f},{bridge_y(1):.0f} {bridge_x(u,1)-(3 if u==0 else -3):.0f},{bridge_y(1):.0f}" fill="{c}"/>')
# belt lane u 0.74..0.94
bl=[(bridge_x(.74,0),H),(bridge_x(.74,1),bridge_y(1)),(bridge_x(.94,1),bridge_y(1)),(bridge_x(.94,0),H)]
o.append('<polygon points="'+' '.join(f'{x:.0f},{y:.0f}' for x,y in bl)+'" fill="url(#belt)"/>')
for k in range(22):  # chevrons
    v=k/22; y=bridge_y(v); s=scale(v); cx=bridge_x(.84,v); w=36*s
    o.append(f'<polyline points="{cx-w:.1f},{y-w*.5:.1f} {cx:.1f},{y:.1f} {cx+w:.1f},{y-w*.5:.1f}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="{6*s:.1f}"/>')
# lane dashes
for k in range(16):
    v=k/16+0.02; y0=bridge_y(v); y1=bridge_y(v+0.025); x0=bridge_x(.45,v); x1=bridge_x(.45,v+.025)
    o.append(f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="#fff" stroke-opacity=".7" stroke-width="{5*scale(v):.1f}"/>')
# horde (far, left part of deck)
horde=[]
for v in [i/60 for i in range(18,58)]:
    for u in [j/24 for j in range(1,17)]:
        if random.random()<0.9: horde.append((u+random.uniform(-.01,.01),v+random.uniform(-.004,.004)))
horde.sort(key=lambda p:-p[1])
for u,v in horde:
    x=bridge_x(u,v); y=bridge_y(v); r=11*scale(v)
    o.append(f'<circle cx="{x:.1f}" cy="{y-r:.1f}" r="{r:.1f}" fill="url(#red)"/>')
# boss: a big red brute silhouette at the far end
bv=.6; bx=bridge_x(.34,bv); by=bridge_y(bv); bs=scale(bv)*3.2
o.append(f'<g transform="translate({bx:.0f},{by:.0f}) scale({bs:.2f})" filter="url(#sh)"><ellipse cx="0" cy="-38" rx="30" ry="34" fill="url(#red)"/><circle cx="0" cy="-80" r="17" fill="url(#red)"/><path d="M-12,-94 L-20,-112 L-5,-96 Z M12,-94 L20,-112 L5,-96 Z" fill="#fff0c8"/><rect x="-9" y="-84" width="6" height="4" fill="#ffe14a"/><rect x="3" y="-84" width="6" height="4" fill="#ffe14a"/><ellipse cx="-34" cy="-40" rx="11" ry="20" fill="url(#red)"/><ellipse cx="34" cy="-40" rx="11" ry="20" fill="url(#red)"/></g>')
# gates on the belt, near -> far
def gate(v,txt,grad,edge):
    x=bridge_x(.84,v); y=bridge_y(v); s=scale(v); w=150*s; h=70*s
    o.append(f'<g filter="url(#sh)"><rect x="{x-w/2:.1f}" y="{y-h-12*s:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{16*s:.1f}" fill="url(#{grad})" stroke="#fff" stroke-width="{5*s:.1f}"/>'
             f'<text x="{x:.1f}" y="{y-12*s-h*.28:.1f}" font-family="Arial Black,Impact,sans-serif" font-weight="900" font-size="{44*s:.1f}" text-anchor="middle" fill="#fff" stroke="{edge}" stroke-width="{7*s:.1f}" paint-order="stroke">{txt}</text></g>')
for v,t,g,e in [(.58,'+1','gBlue','#0b41c4'),(.47,'+1','gBlue','#0b41c4'),(.36,'−10','gRed','#7a0010'),(.25,'×2','gPurp','#4a0a8a'),(.12,'+99','gGold','#9a4a00')]:
    gate(v,t,g,e)
# squad (near, on/near the belt)
sq=[]
for i in range(70):
    a=i*2.39996; r=7.5*(i**0.5)
    sq.append((.72+r*0.0040*__import__('math').cos(a), .03+r*0.0011*__import__('math').sin(a)+.02))
sq.sort(key=lambda p:-p[1])
o.append('<g filter="url(#sh)">')
for u,v in sq:
    x=bridge_x(u,v); y=bridge_y(v); r=17*scale(v)
    o.append(f'<circle cx="{x:.1f}" cy="{y-r:.1f}" r="{r:.1f}" fill="url(#blue)" stroke="#e8f4ff" stroke-width="1.5"/>')
o.append('</g>')
# laser streaks from squad to boss
for i in range(10):
    u0,v0=random.choice(sq[-25:]); x0=bridge_x(u0,v0); y0=bridge_y(v0)-30*scale(v0)
    t=random.uniform(.45,.8); x1=lerp(x0,bx,t); y1=lerp(y0,by-60,t)
    o.append(f'<line x1="{lerp(x0,bx,t-.12):.0f}" y1="{lerp(y0,by-60,t-.12):.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="#ff5ad8" stroke-width="5" stroke-linecap="round" opacity=".9"/>')
# title
o.append('<g font-family="Arial Black,Impact,sans-serif" font-weight="900">')
o.append('<text x="60" y="190" font-size="108" fill="#fff" stroke="#3a0a4a" stroke-width="16" paint-order="stroke" letter-spacing="-2">BRIDGE</text>')
o.append('<text x="60" y="300" font-size="108" fill="#ffd23a" stroke="#3a0a4a" stroke-width="16" paint-order="stroke" letter-spacing="-2">SQUAD</text>')
o.append('<rect x="62" y="330" width="330" height="58" rx="29" fill="#2f7bff" stroke="#fff" stroke-width="5"/><text x="227" y="370" font-size="30" text-anchor="middle" fill="#fff">ENDLESS LEVELS</text>')
o.append('<text x="64" y="440" font-size="26" fill="#ffe9d6" stroke="#3a0a4a" stroke-width="6" paint-order="stroke">9 WEAPONS · 8 WORLDS</text>')
o.append('</g>')
o.append('</svg>')
open('cover.svg','w').write('\n'.join(o))
print('ok', len('\n'.join(o)))
