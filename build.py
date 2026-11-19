#!/usr/bin/env python3
"""Turn the single-level Bridge Squad page into a data-driven game with any number of levels.

Usage:  python3 build.py path/to/original/bridge.html  [out_dir]

Adds: levels from levels.js and a seeded generator (with level archetypes) for every level
past the hand-made ones; weapons (rifle, laser, rapid, spread, rocket, rail, flamer, tesla,
freeze); gates (+N, xN, -N, /N, weapon, frenzy, shield); enemies (grunt, brute, runner,
bomber); hazards (saw blades, explosive barrels).

Every patch is an exact string replacement that must match the expected number of times,
so if the original game changes the build fails loudly instead of producing a half-patched
game.
"""
import pathlib, sys

src = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else pathlib.Path(__file__).parent)

RUNTIME = r"""
// ================================================================== level kit (patched in by build.py)
// ---- weapons. type = projectile type; int = seconds between shots per soldier; shots/fan = spread pattern
const WEAPONS = {
  rifle:  { type: 0,  int: 0.34, shots: 1, fan: 0,    label: 'RIFLE',      ring: 0xffd060, dps: 2.9 },
  laser:  { type: 1,  int: 0.34, shots: 1, fan: 0,    label: 'ATK+150%',   ring: 0xff66e0, dps: 7.35 },
  rapid:  { type: 6,  int: 0.15, shots: 1, fan: 0,    label: 'RAPID FIRE', ring: 0xb8ff40, dps: 8 },
  spread: { type: 7,  int: 0.40, shots: 3, fan: 0.2,  label: 'SPREAD',     ring: 0x40e0ff, dps: 7.5 },
  rocket: { type: 8,  int: 0.60, shots: 1, fan: 0,    label: 'ROCKETS',    ring: 0xff8a20, dps: 8.3 },
  rail:   { type: 9,  int: 0.80, shots: 1, fan: 0,    label: 'RAILGUN',    ring: 0xa0c8ff, dps: 8.75 },
  flame:  { type: 10,  int: 0.30, shots: 2, fan: 0.18, label: 'FLAMER',     ring: 0xff6010, dps: 4.5 },
  shock:  { type: 11,  int: 0.40, shots: 1, fan: 0,    label: 'TESLA',      ring: 0xa070ff, dps: 7 },
  freeze: { type: 12, int: 0.34, shots: 1, fan: 0,    label: 'FREEZE',     ring: 0x90f0ff, dps: 4.7 },
};
// per projectile type: 0 rifle, 1 laser, 2 hero, 3 hero+ATK, 4 ice jet, 5 hero ice jet (stage 2 of the original),
// 6 rapid, 7 spread, 8 rocket, 9 rail, 10 flame, 11 shock, 12 freeze. Damage is the original's PDMG table, extended below.
const PHW = [0.42, 0.42, 0.55, 0.55, 0.42, 0.55, 0.4, 0.42, 0.6, 0.5, 0.7, 0.42, 0.45];   // hit half-width
const PSPL = [0, 0, 0, 0, 0, 0, 0, 0, 1.6, 0, 0, 0, 0];                          // splash radius (rockets)
const PFX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 2];                              // 1 chain lightning, 2 freeze, 3 flame (pierces without losing damage)
let W = WEAPONS.rifle, wName = 'rifle', frenzyT = 0, shieldT = 0, shieldFx = 0;

// ---- enemy types: 0 grunt, 1 brute (tanky; survives several melee trades), 2 runner (fast, aggros early),
//      3 bomber (explodes when killed, hurting nearby enemies; takes extra soldiers with it in melee)
const ETYPE = { grunt: 0, brute: 1, runner: 2, bomber: 3 };
const EHP = [1, 5, 1, 1], ESPD = [1, 1, 1.75, 1.2], EAGG = [0, 0, 3, 2], ESCL = [1, 1.42, 0.86, 0.96];
const ECOL = [[1, 1, 1], [0.6, 0.48, 0.78], [1.4, 1.15, 0.45], [0.42, 1.45, 0.32]], ICE = [0.45, 0.95, 2.4];

// ---- gate styles
const GATE_STYLE = {
  add: { glass: [0.03, 0.2, 0.95], glow: [0.05, 0.3, 1.0], edge: '#0b41c4' },
  big: { glass: [1.0, 0.5, 0.02],  glow: [1.0, 0.5, 0.04], edge: '#b05a00' },
  x:   { glass: [0.55, 0.08, 0.95], glow: [0.6, 0.1, 1.0], edge: '#5a0ca8' },
  '-': { glass: [0.95, 0.04, 0.05], glow: [1.0, 0.08, 0.05], edge: '#8a0010' },
  '/': { glass: [0.45, 0.0, 0.12],  glow: [0.7, 0.0, 0.2],  edge: '#40001a' },
  w:   { glass: [0.02, 0.8, 0.45],  glow: [0.05, 1.0, 0.5],  edge: '#04664a' },
  f:   { glass: [1.0, 0.3, 0.0],    glow: [1.0, 0.35, 0.0],  edge: '#902800' },
  s:   { glass: [0.1, 0.85, 1.0],   glow: [0.15, 0.9, 1.0],  edge: '#005c78' },
  r:   { glass: [0.35, 0.95, 0.05], glow: [0.4, 1.0, 0.1],   edge: '#2a6a00' },
  d:   { glass: [0.95, 0.15, 0.55], glow: [1.0, 0.2, 0.6],   edge: '#7a0040' },
};
const gateMeshes = new Map();
function gateTex(text, edge) {
  return ctex(512, 256, (x, w, h) => {
    x.clearRect(0, 0, w, h);
    x.lineWidth = 11; x.strokeStyle = 'rgba(255,255,255,0.95)'; rr(x, 12, 12, w - 24, h - 24, 44); x.stroke();
    let px = 178; x.font = '900 ' + px + 'px ' + FONT;
    const tw = x.measureText(text).width; if (tw > w - 80) { px = Math.floor(px * (w - 80) / tw); x.font = '900 ' + px + 'px ' + FONT; }
    x.textAlign = 'center'; x.textBaseline = 'middle'; x.lineJoin = 'round';
    x.lineWidth = Math.max(10, px * 0.16); x.strokeStyle = edge; x.strokeText(text, w / 2, h / 2 + 12);
    const g = x.createLinearGradient(0, 40, 0, 220); g.addColorStop(0, '#ffffff'); g.addColorStop(1, '#d8ecff');
    x.fillStyle = g; x.fillText(text, w / 2, h / 2 + 12);
  });
}
function gateMeshFor(label, edge) {
  const key = label + '|' + edge;
  if (!gateMeshes.has(key)) gateMeshes.set(key, inst(gateNumGeo, new THREE.MeshBasicMaterial({ map: gateTex(label, edge), color: numBright, vertexColors: true, alphaTest: 0.5 }), 72, 0));
  return gateMeshes.get(key);
}
function makeGate(spec, t) {
  const v = spec.val || 1, op = spec.op || '+';
  const kind = spec.weapon ? 'w' : spec.buff === 'frenzy' ? 'f' : spec.buff === 'shield' ? 's' : spec.buff === 'rate' ? 'r' : spec.buff === 'dmg' ? 'd' : op === 'x' ? 'x' : op === '-' ? '-' : op === '/' ? '/' : '';
  const style = GATE_STYLE[kind || (v < 10 ? 'add' : 'big')];
  const label = kind === 'w' ? (WEAPONS[spec.weapon] || WEAPONS.laser).label.split(' ')[0] : kind === 'f' ? 'FRENZY' : kind === 's' ? 'SHIELD' : kind === 'r' ? 'FIRE+25%' : kind === 'd' ? 'DMG+25%'
    : kind === 'x' ? '×' + v : kind === '-' ? '−' + v : kind === '/' ? '÷' + v : '+' + v;
  const shoot = !!spec.shoot && (kind === '' || kind === '-');   // shootable gates count up while you shoot them
  return { x: LANE_X, d: REL * t, t, val: v, kind, weapon: spec.weapon, secs: spec.secs || (kind === 's' ? 5 : 6), label, glass: style.glass, glow: style.glow, mesh: gateMeshFor(label, style.edge), alive: true,
    shoot, sv: kind === '-' ? -v : v, step: spec.step || 6, cap: spec.cap != null ? spec.cap : (kind === '-' ? 3 : v + 5), charge: 0 };
}
function shootGate(g, dmg, x) { // every `step` damage raises the gate by one; a red trap can be shot up into a blue gate
  g.charge += dmg;
  if (PT < MAXPT - 300 && Math.random() < 0.3) burst(x, 1.1, g.d, 1, 3, 1.4, 1.8, 2.4, 0.5, 0.15);
  let changed = false;
  while (g.charge >= g.step && g.sv < g.cap) { g.charge -= g.step; g.sv++; changed = true; }
  if (g.sv >= g.cap) g.charge = 0;
  if (!changed) return;
  const style = GATE_STYLE[g.sv < 0 ? '-' : g.sv < 10 ? 'add' : 'big'];
  g.kind = g.sv < 0 ? '-' : ''; g.val = Math.abs(g.sv); g.label = g.sv < 0 ? '−' + -g.sv : '+' + g.sv;
  g.glass = style.glass; g.glow = style.glow; g.mesh = gateMeshFor(g.label, style.edge);
  if (thr('gateUp', 60)) tone('square', 640 + g.sv * 30, 900 + g.sv * 30, 0.05, 0.03);
}
function setWeapon(name) {
  wName = WEAPONS[name] ? name : 'laser'; W = WEAPONS[wName];
  atk = wName !== 'rifle'; setSoldierLook(wName === 'freeze' ? 2 : atk ? 1 : 0);
  popup(W.label, clamp(X, -2, 2), 3.4, D + 2, '#ffe23a', '#3a1d00', 2.7, 1.6, 1.4);
}
function loseNearest(k, x, d) { // the k soldiers closest to (x, d) die
  for (let n = 0; n < k && N > 0; n++) { let best = 0, bd = 1e9; for (let i = 0; i < N; i++) { const q = Math.abs(sX[i] - x) + Math.abs(sD[i] - d); if (q < bd) { bd = q; best = i; } } killSoldier(best); }
}
function gateSpecial(g) {
  if (g.kind === 'x') {
    addSoldiers(Math.max(0, Math.min(MAXS - N, Math.round(N * (g.val - 1)))), g.x - 0.6, g.d, 1.3);
    sfx.gate99(); popup(g.label, g.x - 0.6, 3.0, g.d, '#f0c8ff', '#3a0a5a', 3.4, 1.0, 2.2);
    burst(g.x, 1, g.d, 60, 10, 1.6, 0.5, 2.4, 1.1, 0.5, -5, 3); ring(g.x, g.d, 0.5, 6, 0.4, 0xc070ff); shake = Math.max(shake, 0.25);
  } else if (g.kind === '-' || g.kind === '/') {
    loseNearest(g.kind === '-' ? g.val : N - Math.floor(N / g.val), g.x, g.d);
    popup(g.label, g.x - 0.6, 3.0, g.d, '#ff8080', '#4a0000', 3.2, 1.0, 2.2); burst(g.x, 1, g.d, 40, 8, 2.4, 0.3, 0.2, 1.0, 0.5, -5, 3);
    ring(g.x, g.d, 0.5, 6, 0.4, 0xff3030); shake = Math.max(shake, 0.35);
    if (N <= 0) loseMsg = 'A red gate took your last soldiers.<br>Steer off the belt when a red gate comes!';
  } else if (g.kind === 'w') {
    setWeapon(g.weapon); sfx.power(); fovK = 1;
    burst(X, 0.8, D, 60, 9, 0.4, 2.4, 1.4, 1.2, 0.6, -4, 3); ring(X, D, 0.5, 6.5, 0.5, W.ring);
  } else if (g.kind === 'f') {
    frenzyT = g.secs; sfx.power(); popup('FRENZY! x2 FIRE', clamp(X, -2, 2), 3.4, D + 2, '#ffb020', '#4a1500', 2.4, 1.4, 1.4);
    burst(X, 0.8, D, 50, 9, 2.4, 1.0, 0.1, 1.1, 0.5, -4, 3); ring(X, D, 0.5, 6.5, 0.5, 0xff7a10);
  } else if (g.kind === 'r') {
    rateMul *= 0.8; sfx.power(); popup('FIRE RATE +25%', clamp(X, -2, 2), 3.4, D + 2, '#d8ff80', '#1f4a00', 2.3, 1.3, 1.4); ring(X, D, 0.5, 6.5, 0.5, 0x9aff30);
  } else if (g.kind === 'd') {
    dmgMul *= 1.25; sfx.power(); popup('DAMAGE +25%', clamp(X, -2, 2), 3.4, D + 2, '#ffb0e0', '#5a0030', 2.3, 1.3, 1.4); ring(X, D, 0.5, 6.5, 0.5, 0xff40a0);
  } else if (g.kind === 's') {
    shieldT = g.secs; sfx.power(); popup('SHIELD ' + g.secs + 's', clamp(X, -2, 2), 3.4, D + 2, '#a8f4ff', '#003a50', 2.4, 1.4, 1.4);
    ring(X, D, 0.5, 7, 0.5, 0x60e0ff);
  }
}
function splash(x, d, r, dmg) { // area damage to every enemy in the radius
  const r2 = r * r;
  for (let j = 0; j < E; j++) { if (eHp[j] <= 0) continue; const dx = eX[j] - x, dd = eD[j] - d; if (dx * dx + dd * dd < r2) { eHp[j] -= dmg; if (eHp[j] <= 0) killEnemy(j, true); } }
  if (PT < MAXPT - 250) burst(x, 0.8, d, 8, 7, 2.4, 1.1, 0.2, 1.0, 0.3, -6, 2);
  if (thr('boom', 70)) noise(0.16, 0.05, 2500, 200);
}
function chain(j, dmg) { // tesla: the bolt jumps to up to 3 more enemies, weakening each time
  let x = eX[j], d = eD[j], cur = j;
  for (let hop = 0; hop < 4 && cur >= 0; hop++) {
    eHp[cur] -= dmg; x = eX[cur]; d = eD[cur];
    if (PT < MAXPT - 250) burst(x, 0.9, d, 3, 3, 1.3, 0.9, 2.5, 0.6, 0.18);
    if (eHp[cur] <= 0) killEnemy(cur, hop > 0);
    dmg *= 0.75; let nx = -1, nb = 6.8;
    for (let i = 0; i < E; i++) { if (eHp[i] <= 0) continue; const q = (eX[i] - x) ** 2 + (eD[i] - d) ** 2; if (q < nb) { nb = q; nx = i; } }
    cur = nx;
  }
  if (thr('zap', 60)) tone('sawtooth', 1400, 300, 0.07, 0.03);
}

// ---- hazards: saw blades sweep across the deck at a fixed d; barrels sit in the horde and blow up when shot
const hazards = [];
const sawGeo = cylG(0.9, 0.9, 0.12, 14).rotateX(Math.PI / 2), hubGeo = cylG(0.3, 0.3, 0.22, 12).rotateX(Math.PI / 2);
const sawMat = std({ color: 0xd6dae4, roughness: 0.22, metalness: 0.95 }), hubMat = std({ color: 0xd0181f, roughness: 0.4, metalness: 0.4, emissive: 0x500000 });
const barrelGeo = cylG(0.42, 0.42, 1.05, 16), bandGeo = cylG(0.44, 0.44, 0.16, 16);
const barrelMat = std({ color: 0xd8261c, roughness: 0.4, metalness: 0.5 }), bandMat = std({ color: 0xffc400, roughness: 0.35, metalness: 0.6, emissive: 0x332200 });
const trackMat = new THREE.MeshBasicMaterial({ color: new THREE.Color(1.4, 0.15, 0.1), transparent: true, opacity: 0.35, depthWrite: false });
function buildHazards(list) {
  for (const h of hazards) { scene.remove(h.mesh); if (h.track) scene.remove(h.track); }
  hazards.length = 0;
  for (const s of list) {
    const g = new THREE.Group(); scene.add(g);
    if (s.type === 'saw') {
      const blade = new THREE.Mesh(sawGeo, sawMat); blade.castShadow = true; g.add(blade); g.add(new THREE.Mesh(hubGeo, hubMat));
      const track = new THREE.Mesh(flatQuad, trackMat); track.position.set((s.x0 + s.x1) / 2, 0.07, -s.d); track.scale.set(s.x1 - s.x0 + 1.8, 1, 0.5); scene.add(track);
      hazards.push({ type: 'saw', d: s.d, x0: s.x0, x1: s.x1, speed: s.speed || 1.6, ph: s.phase || 0, x: s.x0, mesh: g, blade, track, cd: 0 });
    } else if (s.type === 'barrel') {
      const b = new THREE.Mesh(barrelGeo, barrelMat); b.position.y = 0.53; b.castShadow = true; g.add(b);
      for (const y of [0.25, 0.8]) { const r = new THREE.Mesh(bandGeo, bandMat); r.position.y = y; g.add(r); }
      g.position.set(s.x, 0, -s.d);
      hazards.push({ type: 'barrel', x: s.x, d: s.d, hp: s.hp || 4, r: s.radius || 3.2, mesh: g });
    }
  }
}
function blowBarrel(h) {
  h.hp = 0; h.mesh.visible = false;
  burst(h.x, 1, h.d, 70, 13, 2.5, 1.2, 0.2, 1.4, 0.6, -10, 4); burst(h.x, 1, h.d, 30, 5, 2.5, 2.5, 2.5, 2.4, 0.3);
  ring(h.x, h.d, 0.5, h.r * 2, 0.45, 0xffa040); shake = Math.max(shake, 0.4); sfx.bossHit(); noise(0.4, 0.1, 3000, 120);
  popup('BOOM!', h.x, 3.2, h.d, '#ffe23a', '#5a1a00', 2.2, 0.8, 2);
  splash(h.x, h.d, h.r, 30);
}
function updateHazards(dt) {
  if (shieldT > 0) { shieldT -= dt; shieldFx -= dt; if (shieldFx <= 0) { shieldFx = 0.35; ring(X, D, hw + 0.2, hw + 1.6, 0.35, 0x60e0ff); } }
  if (frenzyT > 0) frenzyT -= dt;
  for (const h of hazards) {
    if (h.type !== 'saw') continue;
    h.x = h.x0 + (h.x1 - h.x0) * (0.5 + 0.5 * Math.sin(time * h.speed + h.ph));
    h.mesh.position.set(h.x, 0.75, -h.d); h.blade.rotation.z -= dt * 18;
    h.cd -= dt;
    if (state === 'play' && h.cd <= 0 && Math.abs(h.d - D) < hd + 1.5) {
      let k = 0;
      for (let i = N - 1; i >= 0 && k < 1; i--) if (Math.abs(sX[i] - h.x) < 0.85 && Math.abs(sD[i] - h.d) < 0.5) {
        if (shieldT > 0) { h.cd = 0.3; ring(sX[i], sD[i], 0.3, 1.6, 0.25, 0x60e0ff); break; }
        killSoldier(i); k++;
      }
      if (k) { h.cd = 0.16; burst(h.x, 0.6, h.d, 10, 7, 2.4, 2.2, 1.6, 0.5, 0.25, -8, 3); if (N <= 0) loseMsg = 'The saw blades shredded your squad.<br>Watch their sweep and slip past!'; }
    }
  }
}


// ---- themes: original palettes for sky, fog, water, deck, barriers and lights (the stock look is 'dusk')
const THEMES = {
  dusk:   { bg: [0.012, 0.04, 0.12], fog: [0.03, 0.075, 0.19], deep: [0.004, 0.022, 0.08], shal: [0.012, 0.08, 0.22], glint: [0.22, 0.42, 0.72], deck: 0xffffff, conc: 0xa3a8b6, pier: 0x5c6276, sun: [0xfff0da, 0.82], hemi: [0xdbeaff, 0x56607c, 0.27], rim: [0xcfe0ff, 0.34], css: '#0a1838' },
  day:    { bg: [0.22, 0.5, 0.92], fog: [0.42, 0.64, 0.94], deep: [0.01, 0.08, 0.30], shal: [0.04, 0.26, 0.62], glint: [0.7, 0.9, 1.0], deck: 0xffffff, conc: 0xb8bfcc, pier: 0x6a7286, sun: [0xffffff, 0.95], hemi: [0xe8f4ff, 0x7a8aa0, 0.42], rim: [0xffffff, 0.3], css: '#4a8ef0' },
  sunset: { bg: [0.50, 0.14, 0.22], fog: [0.80, 0.36, 0.30], deep: [0.08, 0.02, 0.10], shal: [0.40, 0.11, 0.22], glint: [1.0, 0.62, 0.35], deck: 0xffe2cc, conc: 0xc8a29a, pier: 0x6e4a58, sun: [0xffb070, 0.95], hemi: [0xffd2b0, 0x5a3044, 0.34], rim: [0xff9a7a, 0.42], css: '#8a2a3a' },
  neon:   { bg: [0.03, 0.0, 0.08], fog: [0.12, 0.02, 0.22], deep: [0.02, 0.0, 0.06], shal: [0.10, 0.0, 0.28], glint: [0.2, 1.0, 1.0], deck: 0xc4c0e0, conc: 0x8a80b0, pier: 0x3a2c5a, sun: [0xd8b8ff, 0.72], hemi: [0xb0a0ff, 0x30204a, 0.3], rim: [0x40f0ff, 0.6], css: '#12042a' },
  toxic:  { bg: [0.03, 0.08, 0.02], fog: [0.12, 0.22, 0.06], deep: [0.02, 0.05, 0.01], shal: [0.12, 0.28, 0.04], glint: [0.6, 1.0, 0.2], deck: 0xdde6cc, conc: 0x9aa884, pier: 0x4a5636, sun: [0xeaffb0, 0.8], hemi: [0xe0ffc0, 0x3a4a22, 0.3], rim: [0xb0ff60, 0.42], css: '#16260a' },
  desert: { bg: [0.70, 0.50, 0.28], fog: [0.88, 0.70, 0.44], deep: [0.0, 0.20, 0.26], shal: [0.05, 0.50, 0.52], glint: [0.8, 1.0, 0.95], deck: 0xfff0d0, conc: 0xd8c09a, pier: 0x8a7254, sun: [0xffe8b8, 1.0], hemi: [0xfff0d0, 0x8a6a44, 0.42], rim: [0xffe0a0, 0.35], css: '#c09050' },
  storm:  { bg: [0.10, 0.04, 0.05], fog: [0.22, 0.08, 0.08], deep: [0.04, 0.02, 0.03], shal: [0.20, 0.06, 0.07], glint: [1.0, 0.35, 0.25], deck: 0xdcd0d0, conc: 0x9a8a8e, pier: 0x4a3438, sun: [0xffd0c0, 0.75], hemi: [0xffc8c8, 0x402028, 0.3], rim: [0xff6a5a, 0.5], css: '#2a0c10' },
  frost:  { bg: [0.72, 0.82, 0.92], fog: [0.86, 0.92, 0.98], deep: [0.12, 0.30, 0.38], shal: [0.62, 0.84, 0.90], glint: [1.0, 1.0, 1.0], deck: 0xeaf6ff, conc: 0xd8e6f2, pier: 0x8aa0b8, sun: [0xf0f8ff, 0.92], hemi: [0xffffff, 0x8fa8c0, 0.48], rim: [0xd0f0ff, 0.4], css: '#8cb6dc' },
};
const ARCH_THEME = { classic: 'dusk', swarm: 'sunset', saws: 'neon', arsenal: 'day', boom: 'toxic', siege: 'desert', bossrush: 'storm', frost: 'frost' };
function applyTheme(name) {
  const T = THEMES[name] || THEMES.dusk;
  scene.background.setRGB(...T.bg); scene.fog.color.setRGB(...T.fog);
  waterMat.uniforms.uDeep.value.setRGB(...T.deep); waterMat.uniforms.uShal.value.setRGB(...T.shal); waterMat.uniforms.uGlint.value.setRGB(...T.glint);
  waterMat.uniforms.uRefH.value.setRGB(...T.fog.map(v => Math.min(1, v * 1.8))); waterMat.uniforms.uRefZ.value.setRGB(...T.deep.map(v => v * 1.2 + 0.004));
  TM.deck.color.setHex(T.deck); TM.conc.color.setHex(T.conc); TM.pier.color.setHex(T.pier);
  sun.color.setHex(T.sun[0]); sun.intensity = T.sun[1]; hemi.color.setHex(T.hemi[0]); hemi.groundColor.setHex(T.hemi[1]); hemi.intensity = T.hemi[2]; rim.color.setHex(T.rim[0]); rim.intensity = T.rim[1];
  stage.style.background = T.css;
}

// ---- levels
const STOCK_LEVEL = {
  name: 'STAGE 1',
  gates: [{ t: 2.0, every: 0.4, count: 49, val: 1 }, { t: 23.0, every: 1.1, count: 3, val: 99 }],
  horde: [{ x0: -6.05, x1: 2.85, d0: 17.5, d1: 62.6, gap: 0.62, type: 'grunt' }],
  cage: { x: -4.6, d: 16.2, hp: 30, weapon: 'laser' },
  bosses: [{ kind: 0, at: 12.6, ahead: 26 }, { kind: 1, at: 21.0, ahead: 26 }],
  final: { hp: 9999, cap: 36, speed: 2.2, wakeAt: 29 },
  hazards: [],
  stars: [150, 300],
};
function normLevel(Lv, i) {
  const o = Object.assign({}, STOCK_LEVEL, Lv);
  o.name = Lv.name || 'STAGE ' + (i + 1);
  o.cage = Object.assign({}, STOCK_LEVEL.cage, Lv.cage);
  o.final = Object.assign({}, STOCK_LEVEL.final, Lv.final);
  o.horde = (o.horde || []).map(h => { const q = Object.assign({ gap: 0.62, type: 'grunt' }, h); q.ty = ETYPE[q.type] || 0; if (q.hp == null) q.hp = EHP[q.ty]; return q; });
  o.gates = (o.gates || []).map(g => Object.assign({ every: 0, count: 1, val: 1 }, g));
  o.bosses = (o.bosses || []).map(b => Object.assign({ ahead: 26, dx: 0 }, b));
  o.hazards = o.hazards || [];
  return o;
}
function checkLevel(Lv) { // the engine's hard limits; a broken level still loads, but says why in the console
  const w = [], times = [];
  for (const g of Lv.gates) {
    if (g.weapon && !WEAPONS[g.weapon]) w.push('unknown weapon "' + g.weapon + '" (have: ' + Object.keys(WEAPONS) + ')');
    if (g.buff && !['frenzy', 'shield', 'rate', 'dmg'].includes(g.buff)) w.push('unknown buff "' + g.buff + '" (have: frenzy, shield, rate, dmg)');
    if (g.op && !['+', '-', 'x', '/'].includes(g.op)) w.push('unknown gate op "' + g.op + '" (have: + - x /)');
    if (!g.weapon && !g.buff && !(g.val >= 1)) w.push('gate values must be >= 1 (use op: "-" for minus gates)');
    for (let j = 0; j < g.count; j++) times.push(g.t + g.every * j);
  }
  times.sort((a, b) => a - b);
  for (let i = 0; i < times.length; i++) {
    let n = 0; for (let j = i; j < times.length && times[j] - times[i] < 25; j++) n++;
    if (n > 72) { w.push('more than 72 gates within 25 s of t=' + times[i].toFixed(1) + ' (the gate glass is capped at 72 on screen)'); break; }
    if (i && times[i] - times[i - 1] < 0.25) { w.push('gates at t=' + times[i - 1].toFixed(2) + ' and ' + times[i].toFixed(2) + ' overlap on the belt (keep >= 0.25 s apart)'); break; }
  }
  let e = 0; for (const h of Lv.horde) e += Math.floor((h.d1 - h.d0) / h.gap + 1) * Math.floor((h.x1 - h.x0) / h.gap + 1);
  if (e > MAXE) w.push('horde has ~' + e + ' enemies; only the first ' + MAXE + ' spawn');
  for (const h of Lv.horde) if (!(h.type in ETYPE)) w.push('unknown enemy type "' + h.type + '" (have: ' + Object.keys(ETYPE) + ')');
  for (const h of Lv.hazards) if (h.type !== 'saw' && h.type !== 'barrel') w.push('unknown hazard "' + h.type + '" (have: saw, barrel)');
  for (const b of Lv.bosses) if (b.kind !== 0 && b.kind !== 1) w.push('mid-bosses must be kind 0 or 1 (kind 2 is the final boss and ends the level)');
  if (Lv.theme && !THEMES[Lv.theme]) w.push('unknown theme "' + Lv.theme + '" (have: ' + Object.keys(THEMES) + ')');
  if (Lv.cage.weapon && !WEAPONS[Lv.cage.weapon]) w.push('unknown cage weapon "' + Lv.cage.weapon + '"');
  if (Lv.cage.x > -2) w.push('keep the cage at x <= -2: the squad is pushed to its right side, and the belt is at x = ' + LANE_X);
  if (Lv.final.wakeAt > D_MAX) w.push('final.wakeAt must be <= ' + D_MAX + ' (the squad stops advancing there)');
  return w;
}

// ---- generator: every level past the hand-made ones. Seeded, so level N is always the same level.
function rng(seed) { let a = seed >>> 0; return () => { a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const ARCHETYPES = [ // [id, HUD name, first level it can appear on]
  ['classic', '', 1], ['swarm', 'SWARM', 2], ['saws', 'SAWS', 3], ['arsenal', 'ARSENAL', 4],
  ['boom', 'BOOM', 5], ['siege', 'SIEGE', 6], ['bossrush', 'BOSS RUSH', 8], ['frost', 'FROST', 11],
];
const WEAPON_UNLOCK = { laser: 1, rapid: 3, spread: 4, rocket: 5, flame: 6, rail: 7, shock: 9, freeze: 11 };
function generateLevel(n, seed) {
  const R = rng(seed || n * 9973 + 17), pick = a => a[Math.floor(R() * a.length)], k = Math.min(1, (n - 1) / 30); // k: difficulty 0..1 over 30 levels
  const archs = ARCHETYPES.filter(a => a[2] <= n), arch = n < 2 ? ARCHETYPES[0] : pick(archs), A = arch[0];
  const unlocked = Object.keys(WEAPON_UNLOCK).filter(w => WEAPON_UNLOCK[w] <= n), finisher = unlocked.filter(w => w !== 'freeze' && w !== 'flame');   // short-range/utility weapons are poor against the final boss
  const wakeAt = Math.round(29 + k * 9), tWake = wakeAt / V_SQUAD;
  const cage = { x: -4.6 + R() * 0.8, d: 13 + R() * 5, hp: 30 + Math.min(15, Math.round(n * 0.75)) + (A === 'siege' ? 8 : 0),
    weapon: A === 'boom' ? pick(['rocket', 'flame'].filter(w => unlocked.includes(w)).concat('laser')) : A === 'frost' ? 'freeze' : n < 4 ? 'laser' : pick(finisher) };
  // gate timeline: a stream of small gates, some swapped for multipliers, traps, buffs and weapons; big gates near the boss
  const bigT = tWake - 1.2 - R() * 0.6, every = Math.max(0.3, 0.36 + R() * 0.12 + k * 0.04 - (A === 'swarm' ? 0.05 : 0)), sv = n >= 6 && R() < 0.5 ? 2 : 1;
  const slots = []; for (let t = 1.8; t < bigT - 1.4 && slots.length < 62; t += every) slots.push({ t: +t.toFixed(2), val: sv });
  const at = f => { for (let tries = 0; tries < 8; tries++) { const s = slots[Math.min(slots.length - 1, Math.floor(slots.length * f) + tries)]; if (s && !s.op && !s.weapon && !s.buff) return s; } return {}; };
  if (n >= 2) Object.assign(at(0.42 + R() * 0.1), { op: 'x', val: 2 });
  if ((n >= 8 && R() < 0.6) || A === 'swarm') Object.assign(at(0.7 + R() * 0.08), { op: 'x', val: 2 });
  const weaponGates = n < 3 ? 0 : A === 'arsenal' ? 3 : 1;
  for (let i = 0; i < weaponGates; i++) { // the last weapon gate is the one you fight the boss with, so never freeze or flame
    const pool = (i === weaponGates - 1 ? finisher : unlocked).filter(w => w !== cage.weapon);
    const s = at((0.3 + 0.55 * (i + 1) / weaponGates) - 0.05 + R() * 0.05); delete s.op; s.val = 1; s.weapon = pick(pool.length ? pool : ['laser']);
  }
  if (n >= 3) { // traps go in after the weapon gates and never right next to one, so dodging a trap can't cost you a weapon
    const traps = Math.min(4, 1 + Math.floor(n / 6)) + (A === 'saws' ? 1 : 0);
    for (let i = 0; i < traps; i++) {
      const s = at(0.35 + R() * 0.6), j = slots.indexOf(s);
      if (j >= 0 && ![-2, -1, 1, 2].some(o => slots[j + o] && (slots[j + o].weapon || slots[j + o].op === '-' || slots[j + o].op === '/'))) s.op = n >= 10 && R() < 0.25 ? '/' : '-';
    }
  }
  if (A === 'arsenal' || A === 'bossrush' || (n >= 6 && R() < 0.35)) { const s = at(0.9); s.buff = 'frenzy'; s.secs = 6; }
  if (A === 'saws' || A === 'bossrush' || (n >= 5 && R() < 0.3)) { const s = at(0.25 + R() * 0.3); s.buff = 'shield'; s.secs = 5; }
  let dpsMul = 1;   // stat gates make the squad hit harder, so the boss gets tougher to match
  if (n >= 3) for (let i = 0; i < 1 + (n >= 10 ? 1 : 0); i++) { const s = at(0.3 + R() * 0.55); if (s.t != null) { s.buff = R() < 0.5 ? 'rate' : 'dmg'; dpsMul *= 1.25; } }
  if (n >= 4) for (const s of slots) { // shootable gates: from level 4 traps can be shot up, from level 6 some +gates too
    if (s.op === '-' || s.op === '/') { if (s.op === '-') { s.shoot = true; s.step = Math.min(12, Math.round(3 + n * 0.25)); s.cap = 2 + Math.floor(R() * 5); } }
    else if (n >= 6 && !s.op && !s.weapon && !s.buff && R() < 0.18) { s.shoot = true; s.step = 6 + Math.floor(n / 5); s.cap = s.val + 3 + Math.floor(R() * 4); }
  }
  const bigN = 2 + Math.floor(R() * 3), bigV = pick([50, 99]), bigE = 1.0 + R() * 0.2;
  for (let i = 0; i < bigN; i++) slots.push({ t: +(bigT + i * bigE).toFixed(2), val: bigV });
  // expected squad if every gate is taken (traps included); sizes traps, the boss and the stars
  let ex = 1, wpn = cage.weapon, frenzyLate = false;
  for (const s of slots) {
    if (s.weapon) { wpn = s.weapon; continue; }
    if (s.buff) { if (s.buff === 'frenzy' && s.t > bigT - 4) frenzyLate = true; continue; }
    if (s.op === '-') s.val = Math.max(2, Math.round(ex * (0.12 + 0.13 * k)));   // a trap costs a share of the squad you should have by then
    if (s.op === '/') s.val = 2;
    ex = s.op === 'x' ? ex * s.val : s.op === '-' ? Math.max(1, ex - s.val) : s.op === '/' ? Math.max(1, Math.floor(ex / s.val)) : ex + s.val; ex = Math.min(MAXS, ex);
  }
  if (A === 'saws') ex *= 0.85;
  // horde: bands along the bridge; the archetype picks which enemy types fill them
  const typePool = A === 'swarm' ? ['runner', 'runner', 'grunt'] : A === 'siege' ? ['brute', 'brute', 'grunt'] : A === 'boom' ? ['bomber', 'bomber', 'grunt']
    : ['grunt'].concat(n >= 2 ? ['runner'] : [], n >= 3 ? ['brute'] : [], n >= 5 ? ['bomber'] : []);
  const d0 = cage.d + 1.3, d1 = 62.6, bands = 2 + Math.floor(R() * 2), thin = A === 'bossrush' ? 1.25 : 1;
  const horde = []; let cells = 0;
  for (let i = 0; i < bands; i++) {
    const a = d0 + (d1 - d0) * i / bands, b = d0 + (d1 - d0) * (i + 1) / bands - 0.6, type = i === 0 ? 'grunt' : pick(typePool);   // the first band is always grunts: the squad is tiny then
    const h = { x0: -6.05, x1: 2.85, d0: +a.toFixed(1), d1: +b.toFixed(1), gap: +((type === 'brute' ? 0.9 : 0.62) * thin).toFixed(2), type };
    if (type === 'brute') h.hp = Math.min(8, 4 + Math.floor(n / 8)) + (A === 'siege' ? 1 : 0);
    horde.push(h); cells += ((b - a) / h.gap + 1) * (8.9 / h.gap + 1);
  }
  if (cells > 1250) for (const h of horde) h.gap = +(h.gap * Math.sqrt(cells / 1250)).toFixed(2);
  // hazards
  const hazards = [];
  if (A === 'saws' || (n >= 7 && R() < 0.3)) {
    const nSaw = A === 'saws' ? 2 + Math.floor(R() * 2) : 1;
    for (let i = 0; i < nSaw; i++) {
      let d = 7 + (wakeAt - 12) * (i + 0.5) / nSaw + R() * 2; if (Math.abs(d - cage.d) < 3) d += 4;
      const belt = R() < 0.5;   // a belt saw guards the gates; a deck saw guards the cage side
      hazards.push({ type: 'saw', d: +d.toFixed(1), x0: belt ? 1.5 : -6, x1: belt ? 6.2 : 0.5, speed: +(1.2 + R() * 1.2 + k * 0.6).toFixed(2), phase: +(R() * 6).toFixed(2) });
    }
  }
  if (A === 'boom' || (n >= 5 && R() < 0.3)) {
    const nb = A === 'boom' ? 6 + Math.floor(R() * 6) : 3;
    for (let i = 0; i < nb; i++) hazards.push({ type: 'barrel', x: +(-5.4 + R() * 7.6).toFixed(2), d: +(d0 + 3 + R() * (d1 - d0 - 8)).toFixed(1) });
  }
  // mid-bosses
  const nb = Math.min(A === 'bossrush' ? 4 : 3, 1 + Math.floor(n / 5) + (A === 'bossrush' ? 2 : 0)), bosses = [];
  for (let i = 0; i < nb; i++) { const kind = i % 2; bosses.push({ kind, at: +(14 + (wakeAt - 21) * (nb > 1 ? i / (nb - 1) : 0)).toFixed(1), ahead: 24 + Math.floor(R() * 3), hp: Math.round((kind ? 1200 : 520) * (i === 0 ? 1 : 1 + k * 0.7) * (A === 'bossrush' ? 0.85 : 1)) }); }   // the first one stays at stock strength
  const soak = (3.4 + k * 0.9) * (frenzyLate ? 1.3 : 1);   // seconds of full-squad fire the final boss soaks
  return { name: 'STAGE ' + n + (arch[1] ? ' · ' + arch[1] : ''), archetype: A, theme: A === 'classic' ? pick(['dusk', 'day']) : ARCH_THEME[A], generated: true, gates: slots, horde, cage, bosses, hazards,
    final: { hp: Math.max(4000, Math.round(ex * 0.85 * WEAPONS[wpn].dps * dpsMul * soak / 100) * 100), wakeAt }, stars: [Math.round(ex * 0.45), Math.round(ex * 0.8)] };
}

// ---- progress, coins and upgrades (kept in this browser), the daily level and sharing
const KIT_KEY = 'bridge-squad-kit-v1';
const SAVE = (() => {
  let s = null; try { s = JSON.parse(localStorage.getItem(KIT_KEY)); } catch (e) {}
  s = s && typeof s === 'object' ? s : {};
  return { max: s.max | 0, coins: s.coins | 0, stars: s.stars || {}, daily: s.daily || {}, up: Object.assign({ squad: 0, rate: 0, dmg: 0, cage: 0, hero: 0 }, s.up) };
})();
function persist() { try { localStorage.setItem(KIT_KEY, JSON.stringify(SAVE)); } catch (e) {} }
const UPGRADES = [
  { id: 'squad', name: 'BIGGER SQUAD', desc: lv => '+' + lv * 2 + ' soldiers at the start', max: 5 },
  { id: 'rate', name: 'FASTER FIRE', desc: lv => '+' + lv * 5 + '% fire rate', max: 5 },
  { id: 'dmg', name: 'HARDER HITS', desc: lv => '+' + lv * 6 + '% damage', max: 5 },
  { id: 'cage', name: 'BOLT CUTTERS', desc: lv => '−' + lv * 8 + '% cage health', max: 5 },
  { id: 'hero', name: 'HERO TRAINING', desc: lv => '+' + lv * 20 + '% hero damage', max: 5 },
];
const upCost = lv => 40 + lv * 40;
let rateMul = 1;
function kitApplyUpgrades() { const u = SAVE.up; if (u.squad) addSoldiers(u.squad * 2, X, -0.5, 0.7); dmgMul = 1 + u.dmg * 0.06; heroMul = 1 + u.hero * 0.2; rateMul = 1 / (1 + u.rate * 0.05); }
const DAY = Math.floor((Date.now() - new Date().getTimezoneOffset() * 60000) / 86400000), DAILY_I = 1e6 + DAY, isDaily = i => i >= 1e6;
const DAY_LABEL = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' }).toUpperCase();
function kitWin(st) {
  const daily = isDaily(LI), gain = 10 + st * 10 + Math.floor(kills / 40) + (daily ? 40 : 0);
  SAVE.coins += gain;
  if (daily) SAVE.daily[DAY] = Math.max(SAVE.daily[DAY] | 0, st);
  else { SAVE.stars[LI] = Math.max(SAVE.stars[LI] | 0, st); SAVE.max = Math.max(SAVE.max, LI + 1); }
  persist(); kitUI();
  return '<div class="chip">COINS<b>+' + gain + '</b></div>';
}
function kitLose() { const gain = Math.floor(kills / 60); if (gain) { SAVE.coins += gain; persist(); kitUI(); } }
function kitNext() { return isDaily(LI) ? SAVE.max : LI + 1; }
function kitToast(t) { const e = $('kitt'); e.textContent = t; e.classList.add('show'); clearTimeout(kitToast.t); kitToast.t = setTimeout(() => e.classList.remove('show'), 1800); }
async function kitShare() {
  const daily = isDaily(LI), url = location.origin + location.pathname + (daily ? '?daily=1' : '?level=' + (LI + 1));
  const st = daily ? SAVE.daily[DAY] | 0 : SAVE.stars[LI] | 0, won = state === 'won';
  const text = (won ? 'I beat ' + L.name + ' in Bridge Squad: Endless with ' + N + ' soldiers ' + '★'.repeat(st) + '☆'.repeat(3 - st) : 'Can you beat ' + L.name + ' in Bridge Squad: Endless?');
  try { if (navigator.share) { await navigator.share({ title: 'Bridge Squad: Endless', text, url }); return; } } catch (e) { if (e && e.name === 'AbortError') return; }
  try { await navigator.clipboard.writeText(text + ' ' + url); kitToast('LINK COPIED'); } catch (e) { kitToast(url); }
}
function kitUI() {
  const c = $('coins'); if (c) c.textContent = SAVE.coins;
  const d = $('kDaily'); if (d) d.innerHTML = 'DAILY · ' + DAY_LABEL + (SAVE.daily[DAY] ? ' <u>' + '★'.repeat(SAVE.daily[DAY]) + '</u>' : '');
  const lv = $('kLevels'); if (lv) lv.textContent = 'LEVELS';
}
function kitPanel(html) { const p = $('kitp'); p.innerHTML = html ? '<div class="kpi">' + html + '<button class="kb kclose">CLOSE</button></div>' : ''; p.classList.toggle('show', !!html); }
function kitLevels() {
  const n = Math.max(SAVE.max + 1, 12), cells = [];
  for (let i = 0; i < n; i++) {
    const open = i <= SAVE.max, st = SAVE.stars[i] | 0, tag = open ? (getLevel(i).name.split(' · ')[1] || (i < HAND_LEVELS.length ? 'HANDMADE' : 'CLASSIC')) : 'LOCKED';
    cells.push('<button class="kl' + (open ? '' : ' lock') + (i === LI ? ' cur' : '') + '" data-i="' + i + '"' + (open ? '' : ' disabled') + '><b>' + (i + 1) + '</b><i>' + tag + '</i><u>' + '★'.repeat(st) + '<s>' + '★'.repeat(3 - st) + '</s></u></button>');
  }
  kitPanel('<h3>LEVELS</h3><div class="kgrid">' + cells.join('') + '</div>');
}
function kitShop() {
  const rows = UPGRADES.map(u => {
    const lv = SAVE.up[u.id], cost = upCost(lv), maxed = lv >= u.max;
    return '<div class="ku"><div><b>' + u.name + '</b><span>' + (lv ? u.desc(lv) : 'Not upgraded yet') + (maxed ? '' : ' → ' + u.desc(lv + 1)) + '</span><em>' + '■'.repeat(lv) + '<s>' + '■'.repeat(u.max - lv) + '</s></em></div>'
      + '<button class="kb kbuy" data-u="' + u.id + '"' + (maxed || SAVE.coins < cost ? ' disabled' : '') + '>' + (maxed ? 'MAX' : '<i class="kcoin"></i>' + cost) + '</button></div>';
  }).join('');
  kitPanel('<h3>UPGRADES</h3><p class="kcoins"><i class="kcoin"></i><b>' + SAVE.coins + '</b> coins · win levels to earn more</p>' + rows);
}
document.addEventListener('click', e => {
  const t = e.target.closest('button'); if (!t) return;
  if (t.id === 'kLevels') kitLevels();
  else if (t.id === 'kShop') kitShop();
  else if (t.id === 'kShare') kitShare();
  else if (t.id === 'kDaily') { kitPanel(''); LV = 1; LI = DAILY_I; startGame(); }
  else if (t.classList.contains('kclose')) kitPanel('');
  else if (t.classList.contains('kl')) { kitPanel(''); LV = 1; LI = +t.dataset.i; startGame(); }
  else if (t.classList.contains('kbuy')) {
    const u = UPGRADES.find(q => q.id === t.dataset.u), lv = SAVE.up[u.id], cost = upCost(lv);
    if (lv < u.max && SAVE.coins >= cost) { SAVE.coins -= cost; SAVE.up[u.id] = lv + 1; persist(); initAudio(); sfx.power(); kitShop(); kitUI(); }
  }
});
const HAND_LEVELS = (() => {
  try { const m = location.hash.match(/lvl=([^&]+)/); if (m) return [JSON.parse(decodeURIComponent(escape(atob(m[1].replace(/-/g, '+').replace(/_/g, '/')))))]; } catch (e) { console.warn('bad #lvl= level', e); }
  return (window.BRIDGE_LEVELS && window.BRIDGE_LEVELS.length) ? window.BRIDGE_LEVELS : [STOCK_LEVEL];
})();
const levelCache = [];
function getLevel(i) {
  if (!levelCache[i]) {
    const lv = isDaily(i) ? Object.assign(normLevel(generateLevel(12 + (i % 23), i * 7919 + 3), 0), {}) : normLevel(i < HAND_LEVELS.length ? HAND_LEVELS[i] : generateLevel(i + 1), i);
    if (isDaily(i)) lv.name = 'DAILY · ' + DAY_LABEL;
    checkLevel(lv).forEach(m => console.warn('[level ' + (i + 1) + ' ' + lv.name + '] ' + m));
    levelCache[i] = lv;
  }
  return levelCache[i];
}
window.__bridgeLevel = i => getLevel(i - 1);   // inspect any level from the console: __bridgeLevel(12)
const QS = new URLSearchParams(location.search);   // ?level=N, ?daily=1, or else the furthest level reached
let LI = QS.has('daily') ? DAILY_I : QS.get('level') ? Math.max(0, (parseInt(QS.get('level'), 10) || 1) - 1) : SAVE.max;
let L = null, bossQ = [];
kitUI();
"""

APPLY_LEVEL = r"""function applyLevel() {
  L = getLevel(LI); eTy.fill(0); eSlow.fill(0); frenzyT = shieldT = 0;
  if (LV !== 1) { buildHazards([]); applyTheme('dusk'); return; }   // the original's stage 2 (Flood Rescue) is left as it is
  CAGE_X = L.cage.x; CAGE_D = L.cage.d; CAGE_HP = Math.max(5, Math.round(L.cage.hp * (1 - SAVE.up.cage * 0.08)));
  cage.group.position.set(CAGE_X, 0, -CAGE_D);
  W = WEAPONS.rifle; wName = 'rifle'; frenzyT = shieldT = 0;
  const cw = WEAPONS[L.cage.weapon] || WEAPONS.laser, lc = lblCrate.ctx; lc.clearRect(0, 0, 640, 160);
  fancyText(lc, cw.label, 320, 80, cw.label.length > 8 ? 92 : 108, '#ffe23a', '#6a0a56', 22); lblCrate.tex.needsUpdate = true;
  buildHazards(L.hazards);
  applyTheme(L.theme);
  try { const u = new URL(location.href); if (!location.hash) { if (isDaily(LI)) { u.searchParams.delete('level'); u.searchParams.set('daily', '1'); } else { u.searchParams.delete('daily'); u.searchParams.set('level', LI + 1); } if (u.href !== location.href) history.replaceState(null, '', u); } } catch (e) {}
}
function reset() {
  applyLevel();
"""

HORDE_OLD = """  // horde
  for (let d = HORDE_D0; d <= HORDE_D1; d += HSP) for (let x = HORDE_X0; x <= HORDE_X1 + 0.01; x += HSP) {
    if (x < CAGE_X + 2.2 && d < CAGE_D + 2.6) continue;
    if (E >= MAXE) break;
    eX[E] = x + rand(-0.13, 0.13); eD[E] = d + rand(-0.13, 0.13); eHp[E] = 1; eSt[E] = 0; ePh[E] = Math.random() * TAU; E++;
  }
  // gates on the belt: arrival time t -> distance REL*t
  for (let j = 0; j < 49; j++) gates.push({ x: LANE_X, d: REL * (2.0 + 0.4 * j), val: 1, alive: true });
  for (let j = 0; j < 3; j++) gates.push({ x: LANE_X, d: REL * (23.0 + j * 1.1), val: 99, alive: true });
"""
HORDE_NEW = """  // horde: one grid of enemies per rectangle, leaving room around the cage and the barrels
  for (const h of L.horde) for (let d = h.d0; d <= h.d1 + 0.01; d += h.gap) for (let x = h.x0; x <= h.x1 + 0.01; x += h.gap) {
    if (Math.abs(x - CAGE_X) < 2.2 && Math.abs(d - CAGE_D) < 2.6) continue;
    if (hazards.some(z => z.type === 'barrel' && Math.abs(x - z.x) < 0.7 && Math.abs(d - z.d) < 0.7)) continue;
    if (E >= MAXE) break;
    eX[E] = x + rand(-0.13, 0.13); eD[E] = d + rand(-0.13, 0.13); eHp[E] = h.hp; eTy[E] = h.ty; eSlow[E] = 0; eSt[E] = 0; ePh[E] = Math.random() * TAU; E++;
  }
  // gates on the belt: a gate with arrival time t starts at distance REL*t and meets the squad front at t seconds
  gates.length = 0;
  for (const g of L.gates) for (let j = 0; j < g.count; j++) gates.push(makeGate(g, g.t + g.every * j));
  gates.sort((a, b) => a.d - b.d);
"""

KIT_CSS = r'''
  #kit{display:none;gap:.4em;flex-wrap:wrap;justify-content:center;align-items:center;margin-top:.9em;max-width:94%}
  #ov.menu #kit,#ov.end #kit{display:flex}
  #kShare{display:none}#ov.end #kShare{display:inline-block}
  .kb{font:inherit;font-size:.9em;color:#fff;cursor:pointer;border:.13em solid rgba(255,255,255,.9);border-radius:.7em;padding:.38em .75em;background:linear-gradient(180deg,rgba(255,178,40,.96),rgba(214,96,0,.96));box-shadow:0 .18em 0 rgba(90,30,0,.9);letter-spacing:.04em;text-shadow:0 .06em 0 rgba(90,30,0,.8)}
  .kb:disabled{opacity:.45;cursor:default}.kb u{text-decoration:none;color:#fff3a0}
  #kitc{display:flex;align-items:center;padding:.3em .7em;border-radius:.9em;background:rgba(0,0,0,.35);border:.12em solid rgba(255,255,255,.6);font-size:.95em;color:#ffe14a}
  .kcoin{display:inline-block;width:.9em;height:.9em;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff6b0,#ffc21a 55%,#b86a00);box-shadow:0 0 0 .08em #7a4400;vertical-align:-.1em;margin-right:.3em}
  #kitp{position:absolute;inset:0;z-index:8;display:none;align-items:center;justify-content:center;background:rgba(4,10,30,.8);cursor:default}
  #kitp.show{display:flex}
  .kpi{width:88%;max-height:84%;overflow:auto;padding:1em;border-radius:1em;background:linear-gradient(180deg,#1d3a8a,#0d1d52);border:.14em solid #fff;box-shadow:0 .3em 0 rgba(0,0,0,.5);text-align:center;color:#fff}
  .kpi h3{margin:.1em 0 .6em;font-size:1.6em;letter-spacing:.06em}
  .kgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:.45em;margin-bottom:.8em}
  .kl{font:inherit;color:#fff;cursor:pointer;border:.12em solid rgba(255,255,255,.8);border-radius:.7em;padding:.4em .2em;background:linear-gradient(180deg,#3d7bff,#1640b0)}
  .kl.cur{border-color:#ffe14a;box-shadow:0 0 0 .1em #ffe14a}.kl.lock{opacity:.4;cursor:default;background:#2a3358}
  .kl b{display:block;font-size:1.3em}.kl i{display:block;font-style:normal;font-size:.5em;letter-spacing:.04em;color:#cfe6ff;font-family:Arial,sans-serif;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .kl u{display:block;text-decoration:none;color:#ffd21f;font-size:.8em}.kl u s,.ku em s{text-decoration:none;color:rgba(255,255,255,.25)}
  .ku{display:flex;align-items:center;gap:.6em;text-align:left;padding:.5em;margin-bottom:.45em;border-radius:.7em;background:rgba(0,0,0,.25)}
  .ku>div{flex:1}.ku b{display:block;font-size:1em}.ku span{display:block;font:700 .62em Arial,sans-serif;color:#cfe6ff}.ku em{display:block;font-style:normal;color:#ffd21f;font-size:.7em;letter-spacing:.1em}
  .kcoins{font:700 .8em Arial,sans-serif;margin:-.2em 0 .8em}
  #kitt{position:absolute;left:50%;bottom:10%;transform:translateX(-50%);z-index:9;padding:.4em .9em;border-radius:.8em;background:rgba(0,0,0,.8);color:#fff;font-size:.9em;opacity:0;transition:opacity .3s;pointer-events:none;white-space:nowrap}
  #kitt.show{opacity:1}
  body.clean #kit{display:none!important}
'''

PATCHES = [  # (old, new, expected count) -- applied in order
    # ---- themes: expose the world materials and lights, make the water colours uniforms
    ("scene.add(new THREE.HemisphereLight(0xdbeaff, 0x56607c, 0.27));", "const hemi = new THREE.HemisphereLight(0xdbeaff, 0x56607c, 0.27); scene.add(hemi);", 1),
    ("let beltTex, waterMat;", "let beltTex, waterMat; const TM = {};", 1),
    ("deck.position.set(0, 0, DKC); deck.receiveShadow = true; W1.add(deck);", "deck.position.set(0, 0, DKC); deck.receiveShadow = true; W1.add(deck); TM.deck = deckMat;", 1),
    ("  const prof = [[0, -0.25]", "  TM.conc = conc; TM.pier = pierM;\n  const prof = [[0, -0.25]", 1),
    ("waterMat = new THREE.ShaderMaterial({ uniforms: { uT: { value: 0 }, uSun: { value: SUN_OFF.clone().normalize() } },",
     "waterMat = new THREE.ShaderMaterial({ uniforms: { uT: { value: 0 }, uSun: { value: SUN_OFF.clone().normalize() }, uDeep: { value: new THREE.Color(0.004, 0.022, 0.08) }, uShal: { value: new THREE.Color(0.012, 0.08, 0.22) }, "
     "uGlint: { value: new THREE.Color(0.22, 0.42, 0.72) }, uRefH: { value: new THREE.Color(0.06, 0.14, 0.34) }, uRefZ: { value: new THREE.Color(0.01, 0.03, 0.1) } },", 1),
    ("fragmentShader: `uniform float uT; uniform vec3 uSun; varying vec3 vW;", "fragmentShader: `uniform float uT; uniform vec3 uSun, uDeep, uShal, uGlint, uRefH, uRefZ; varying vec3 vW;", 1),
    ("vec3 c = mix(vec3(0.004, 0.022, 0.08), vec3(0.012, 0.08, 0.22), smoothstep(0.3, 0.75, h0));", "vec3 c = mix(uDeep, uShal, smoothstep(0.3, 0.75, h0));", 1),
    ("c = mix(c, mix(vec3(0.06, 0.14, 0.34), vec3(0.01, 0.03, 0.1), clamp(r.y, 0.0, 1.0)), fr);", "c = mix(c, mix(uRefH, uRefZ, clamp(r.y, 0.0, 1.0)), fr);", 1),
    ("c += vec3(0.22, 0.42, 0.72) * smoothstep(0.66, 0.76, h0)", "c += uGlint * smoothstep(0.66, 0.76, h0)", 1),
    # ---- level data
    ("const CAGE_X = -4.6, CAGE_D = 16.2, CAGE_HP = 30;", "let CAGE_X = -4.6, CAGE_D = 16.2, CAGE_HP = 30;", 1),
    ("let E = 0;\n", "let E = 0;\nconst eTy = new Uint8Array(MAXE), eSlow = new Float32Array(MAXE);\n", 1),
    ("let crackT = 0;\n", "let crackT = 0;\n" + RUNTIME, 1),
    ("function reset() {\n", APPLY_LEVEL, 1),
    (HORDE_OLD, HORDE_NEW, 1),
    ("bosses.length = 0; spawned1 = spawned2 = false;",
     "bosses.length = 0; bossQ = L.bosses.map(b => Object.assign({ done: false }, b));", 1),
    ("  spawnBoss(2, (HORDE_X0 + HORDE_X1) / 2 - 0.3, FORT_D - 2.6, false);",
     "  spawnBoss(2, (HORDE_X0 + HORDE_X1) / 2 - 0.3, FORT_D - 2.6, false, L.final);", 1),
    ("function spawnBoss(kind, x, d, drop) {", "function spawnBoss(kind, x, d, drop, o = {}) {", 1),
    ("const b = makeBoss(kind), def = BOSS_DEF[kind];",
     "const b = makeBoss(kind), def = Object.assign({}, BOSS_DEF[kind]); for (const k of ['hp', 'cap', 'speed']) if (o[k] != null) def[k] = o[k];", 1),
    ("    if (!spawned1 && D >= 12.6) { spawned1 = true; spawnBoss(0, clamp(X, -4, 1.5), D + 26, true); }\n"
     "    if (!spawned2 && D >= 21.0) { spawned2 = true; spawnBoss(1, clamp(X, -4, 1.5), D + 26, true); }\n",
     "    for (const q of bossQ) if (!q.done && D >= q.at) { q.done = true; spawnBoss(q.kind, clamp(X + q.dx, -4, 1.5), D + q.ahead, true, q); }\n", 1),
    ("if (!b.active) { if (LV === 1 ? D >= 29 : gt >= T_BOSS)", "if (!b.active) { if (LV === 1 ? D >= L.final.wakeAt : gt >= T_BOSS)", 1),
    ("clamp(LV === 1 ? D / 29 : gt / T_BOSS, 0, 1)", "clamp(LV === 1 ? D / L.final.wakeAt : gt / T_BOSS, 0, 1)", 1),
    ("$('hudL').textContent = 'STAGE ' + LV;", "$('hudL').textContent = LV === 1 ? L.name : 'FLOOD RESCUE';", 1),
    ("  if (play) gt += dt;", "  if (play) { gt += dt; }\n  updateHazards(dt);", 1),
    # ---- gates: any label, colour per kind, special effects
    ("c = g.val === 1 ? GLASS_B : GLASS_Y, gc = g.val === 1 ? GLOW_B : GLOW_Y", "c = g.glass, gc = g.glow", 1),
    ("    if (g.val === 1) mGateB.setMatrixAt(nb++, _gateM); else mGateY.setMatrixAt(ny++, _gateM);",
     "    g.mesh.setMatrixAt(g.mesh.count++, _gateM);", 1),
    ("let nb = 0, ny = 0, ng = 0;", "let ng = 0; for (const m of gateMeshes.values()) m.count = 0;", 1),
    ("  mGateB.count = nb; mGateY.count = ny; mGlassBack.count",
     "  mGateB.count = mGateY.count = 0; for (const m of gateMeshes.values()) m.instanceMatrix.needsUpdate = true; mGlassBack.count", 1),
    ("        if (g.val === 1) { addSoldiers(1, g.x + rand(-0.8, 0.8), g.d, 0.2);",
     "        if (g.kind) gateSpecial(g);\n        else if (g.val < 10) { addSoldiers(g.val, g.x + rand(-0.8, 0.8), g.d, 0.2);", 1),
    ("popup('+1', g.x", "popup(g.label, g.x", 1),
    ("addSoldiers(99, g.x - 0.6", "addSoldiers(g.val, g.x - 0.6", 1),
    ("popup('+99'", "popup(g.label", 1),
    # ---- weapons
    ("const PSPEED = [36, 54, 36, 54, 48, 48], PWID = [0.34, 0.72, 0.7, 1.5, 0.62, 1.3], PLEN = [1.4, 5.0, 2.2, 6.4, 3.6, 5.2], PRANGE = [RANGE, RANGE, RANGE + 2, RANGE + 2, RANGE, RANGE + 2];",
     "const PSPEED = [36, 54, 36, 54, 48, 48, 44, 40, 24, 70, 30, 64, 46], PWID = [0.34, 0.72, 0.7, 1.5, 0.62, 1.3, 0.3, 0.42, 0.95, 0.5, 1.0, 0.4, 0.5], "
     "PLEN = [1.4, 5.0, 2.2, 6.4, 3.6, 5.2, 1.8, 1.6, 1.3, 9.0, 1.1, 3.2, 1.6], PRANGE = [RANGE, RANGE, RANGE + 2, RANGE + 2, RANGE, RANGE + 2, RANGE, RANGE - 2, RANGE + 2, RANGE + 8, 14, RANGE + 2, RANGE];", 1),
    ("const PDMG = [1, 2.5, 5, 12.5, 2.5, 12.5], HEROT = [0, 0, 1, 1, 0, 1];",
     "const PDMG = [1, 2.5, 5, 12.5, 2.5, 12.5, 1.2, 1.0, 5, 7, 1.2, 2.8, 1.6], HEROT = [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0];", 1),
    ("const PCOL = [[1.9, 0.95, 0.05], [1.75, 0.045, 1.02], [2.0, 1.15, 0.1], [1.9, 0.08, 1.2], [0.3, 1.2, 2.0], [0.45, 1.4, 2.1]];",
     "const PCOL = [[1.9, 0.95, 0.05], [1.75, 0.045, 1.02], [2.0, 1.15, 0.1], [1.9, 0.08, 1.2], [0.3, 1.2, 2.0], [0.45, 1.4, 2.1], [1.3, 2.0, 0.15], [0.15, 1.5, 2.1], [2.3, 0.65, 0.08], [1.2, 1.7, 2.5], [2.5, 0.9, 0.05], [1.3, 0.8, 2.6], [1.5, 2.2, 2.5]];", 1),
    ("function fire(x, d, type) {", "function fire(x, d, type, ang = 0) {", 1),
    ("  pX[P] = x; pD[P] = d; pS[P] = 0; pT[P] = type; pUX[P] = ux; pUD[P] = ud;",
     "  if (ang && ux === 0) { const c = Math.cos(ang), s = Math.sin(ang), u = ux; ux = u * c + ud * s; ud = -u * s + ud * c; }   // fans out unless aimed\n"
     "  pX[P] = x; pD[P] = d; pS[P] = 0; pT[P] = type; pUX[P] = ux; pUD[P] = ud;", 1),
    ("sCd[i] += FIRE_T; sKick[i] = 1; fire(sX[i] + mzX, sD[i] + mzD, sType);",
     "sKick[i] = 1;\n        if (LV === 1) { sCd[i] += W.int * rateMul * (frenzyT > 0 ? 0.5 : 1); for (let k = 0; k < W.shots; k++) fire(sX[i] + mzX, sD[i] + mzD, W.type, (k - (W.shots - 1) / 2) * W.fan); }\n        else { sCd[i] += FIRE_T; fire(sX[i] + mzX, sD[i] + mzD, sType); }", 1),
    ("const pw = (HEROT[ty] ? 0.55 : 0.42)", "const pw = PHW[ty]", 1),
    ("    if (!dead) for (const b of bosses) {",
     "    if (!dead && LV === 1) for (const g of gates) if (g.alive && g.shoot && g.sv < g.cap && d1 >= g.d - 0.35 && d0 <= g.d + 0.35 && Math.abs(x - g.x) < GATE_HW) { shootGate(g, dmg, x); dead = true; break; }\n"
     "    if (!dead) for (const h of hazards) if (h.type === 'barrel' && h.hp > 0 && Math.abs(x - h.x) < 0.45 + pw * 0.5 && d1 >= h.d - 0.45 && d0 <= h.d + 0.45) { h.hp -= dmg; dead = true; if (h.hp <= 0) blowBarrel(h); break; }\n"
     "    if (!dead) for (const b of bosses) {", 1),
    ("if (Math.abs(x - b.x) < b.r && d1 >= b.d - b.r * 0.8 && d0 <= b.d + b.r) { hitBoss(b, dmg, x); dead = true; break; }",
     "if (Math.abs(x - b.x) < b.r && d1 >= b.d - b.r * 0.8 && d0 <= b.d + b.r) { if (PFX[ty] === 2) b.frost = Math.min(1, b.frost + 0.12); hitBoss(b, dmg, x); dead = true; break; }", 1),
    ("          const h = eHp[j]; eHp[j] -= dmg; dmg -= h;",
     "          if (PSPL[ty]) { splash(eX[j], eD[j], PSPL[ty], dmg); dead = true; break scan; }\n"
     "          if (PFX[ty] === 1) { chain(j, dmg); dead = true; break scan; }\n"
     "          if (PFX[ty] === 3) { eHp[j] -= dmg; if (eHp[j] <= 0) killEnemy(j, Math.random() < 0.6); continue; }\n"
     "          if (PFX[ty] === 2) eSlow[j] = 2.5;\n"
     "          const h = eHp[j]; eHp[j] -= dmg; dmg -= h;", 1),
    ("  atk = true; setSoldierLook(true); fovK = 1;\n  popup('ATK+150%', clamp(X, -2, 2), 3.4, D + 2, '#ffe23a', '#3a1d00', 2.7, 1.6, 1.4);",
     "  setWeapon(L.cage.weapon); fovK = 1;", 1),
    # ---- bosses: freeze slows them, a shield blocks a regular smash (not the final boss's slam)
    ("  b.smashA = 1; sfx.smash(); shake = Math.max(shake, 0.45);",
     "  b.smashA = 1; sfx.smash(); shake = Math.max(shake, 0.45);\n"
     "  if (shieldT > 0) { ring(X, D, 0.5, hw + 3, 0.4, 0x60e0ff); popup('BLOCKED', X, 3.2, D + hd, '#a8f4ff', '#003a50', 1.8, 0.7, 2); return; }", 1),
    # ---- enemy types and status effects
    ("function killEnemy(i, quiet) {\n  eHp[i] = 0; kills++;",
     "function killEnemy(i, quiet) {\n  eHp[i] = 0; kills++;\n"
     "  if (eTy[i] === 3) { eTy[i] = 0; ring(eX[i], eD[i], 0.3, 2.6, 0.3, 0x80ff40); splash(eX[i], eD[i], 1.5, 3); }   // bombers go off", 1),
    ("if (eD[i] - front < 6 && Math.abs(eX[i] - X) < hw + 3.2) eSt[i] = 1;",
     "if (eD[i] - front < 6 + EAGG[eTy[i]] && Math.abs(eX[i] - X) < hw + 3.2 + EAGG[eTy[i]] * 0.5) eSt[i] = 1;", 1),
    ("st = CHARGE_V * dt;", "st = CHARGE_V * ESPD[eTy[i]] * (eSlow[i] > 0 ? (eSlow[i] -= dt, 0.35) : 1) * dt;", 1),
    ("if (best >= 0) { killSoldier(best); killEnemy(i, true); }",
     "if (best >= 0) {\n"
     "      if (shieldT <= 0) { killSoldier(best); if (eTy[i] === 3) loseNearest(2, eX[i], eD[i]); }\n"
     "      if (eTy[i] === 1 && eHp[i] > 1) eHp[i] -= 1; else killEnemy(i, true);\n"
     "    }", 1),
    ("eSt[i] = eSt[E]; ePh[i] = ePh[E]; }", "eSt[i] = eSt[E]; ePh[i] = ePh[E]; eTy[i] = eTy[E]; eSlow[i] = eSlow[E]; }", 1),
    ("scl = 0.94 + (ePh[i] % 1) * 0.14;", "scl = (0.94 + (ePh[i] % 1) * 0.14) * ESCL[eTy[i]], ct = eSlow[i] > 0 ? ICE : ECOL[eTy[i]];", 1),
    ("fc[nfar * 3] = tint; fc[nfar * 3 + 1] = tint * 0.92; fc[nfar * 3 + 2] = tint * 0.92;",
     "fc[nfar * 3] = tint * ct[0]; fc[nfar * 3 + 1] = tint * 0.92 * ct[1]; fc[nfar * 3 + 2] = tint * 0.92 * ct[2];", 1),
    ("ec[ne * 3] = tint; ec[ne * 3 + 1] = tint * 0.92; ec[ne * 3 + 2] = tint * 0.92;",
     "ec[ne * 3] = tint * ct[0]; ec[ne * 3 + 1] = tint * 0.92 * ct[1]; ec[ne * 3 + 2] = tint * 0.92 * ct[2];", 1),
    # ---- progress, coins, upgrades, daily, share: markup, styles, input and hooks
    ('<button id="ovm">STAGES</button>',
     '<button id="ovm">STAGES</button>\n    <div id="kit"><div id="kitc"><i class="kcoin"></i><b id="coins">0</b></div><button class="kb" id="kLevels">LEVELS</button><button class="kb" id="kShop">UPGRADES</button><button class="kb" id="kDaily">DAILY</button><button class="kb" id="kShare">SHARE</button></div>\n    <div id="kitp"></div><div id="kitt"></div>', 1),
    ("</style>", KIT_CSS + "</style>", 1),
    ("if (e.target.closest('.ib') || e.target.id === 'unhide') return;",
     "if (e.target.closest('.ib') || e.target.closest('#kit') || e.target.closest('#kitp') || e.target.id === 'unhide') return;", 1),
    ("  addSoldiers(1, X, 0, 0); sX[0] = X; sD[0] = 0;", "  addSoldiers(1, X, 0, 0); sX[0] = X; sD[0] = 0;\n  if (LV === 1) kitApplyUpgrades();", 1),
    ("saveBest(st);", "saveBest(st); const kitChip = LV === 1 ? kitWin(st) : '';", 1),
    ("'</b></div></div>', LV === 1 ? 'NEXT STAGE'", "'</b></div>' + kitChip + '</div>', LV === 1 ? 'NEXT STAGE'", 1),
    ("} else showOverlay('DEFEATED', 'lose',", "} else { if (LV === 1) kitLose(); showOverlay('DEFEATED', 'lose',", 1),
    ("'RETRY');", "'RETRY'); }", 1),
    # ---- endless progression + stars
    ("const st = LV === 1 ? (N >= 300 ? 3 : N >= 150 ? 2 : 1)", "const st = LV === 1 ? (N >= L.stars[1] ? 3 : N >= L.stars[0] ? 2 : 1)", 1),
    # a win on the bridge moves on to the next kit level; the original's stage 2 stays in its stage menu
    ("function primary() { if (state === 'won' && LV === 1) startLevel(2); else startGame(); }",
     "function primary() { if (state === 'won' && LV === 1) LI = kitNext(); startGame(); }", 1),
    ("<b>THE BRIDGE</b><span>GATES &middot; CAGE &middot; LASERS</span>", "<b>THE BRIDGE</b><span>ENDLESS &middot; 9 WEAPONS</span>", 1),
    ("get s() { return { LV,",
     "get s() { return { level: LI, name: L.name, weapon: wName, frenzyT, shieldT, hazards: hazards.map(h => ({ type: h.type, x: h.x, d: h.d, x0: h.x0, x1: h.x1, hp: h.hp })), LV,", 1),
    (".map(g => ({ d: g.d, val: g.val }))", ".map(g => ({ d: g.d, val: g.val, kind: g.kind, label: g.label }))", 1),
    # ---- levels.js loads before the game
    ("<script>\n(function(){\n  var fill=", "<script src=\"levels.js\"></script>\n<script>\n(function(){\n  var fill=", 1),
]

for old, new, n in PATCHES:
    got = src.count(old)
    if got != n:
        sys.exit(f"patch anchor found {got}x (expected {n}): {old[:70]!r}")
    src = src.replace(old, new)

out.mkdir(parents=True, exist_ok=True)
(out / "index.html").write_text(src)
print("wrote", out / "index.html", f"({len(PATCHES)} patches)")

# the same patches as data, for web/index.html, which patches the original game in the browser
import json
(out / "patches.json").write_text(json.dumps(PATCHES))
print("wrote", out / "patches.json")

# syntax-check the patched game script when Node is available
import re, shutil, subprocess, tempfile
if shutil.which("node"):
    body = re.search(r'<script type="text/plain" id="main">(.*?)</script>', src, re.S).group(1)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(body)
    r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    if r.returncode:
        sys.exit("patched game has a syntax error:\n" + r.stderr)
    print("syntax OK")
