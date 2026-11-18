#!/usr/bin/env python3
"""Turn the single-level Bridge Squad page into a data-driven game with any number of levels.

Usage:  python3 build.py path/to/original/bridge.html  [out_dir]

Adds: levels from levels.js, a seeded generator for every level past the hand-made ones,
weapons (rifle, laser, rapid, spread, rocket, rail), gate types (+N, xN, -N, weapon) and
enemy types (grunt, brute, runner).

Every patch is an exact string replacement that must match the expected number of
times, so if the original game changes the build fails loudly instead of producing a
half-patched game.
"""
import pathlib, sys

src = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else pathlib.Path(__file__).parent)

RUNTIME = r"""
// ================================================================== level kit (patched in by build.py)
// ---- weapons. type = projectile type; int = seconds between shots per soldier; shots/fan = spread pattern
const WEAPONS = {
  rifle:  { type: 0, int: 0.34, shots: 1, fan: 0,    label: 'RIFLE',     ring: 0xffd060 },
  laser:  { type: 1, int: 0.34, shots: 1, fan: 0,    label: 'ATK+150%',  ring: 0xff66e0 },
  rapid:  { type: 4, int: 0.15, shots: 1, fan: 0,    label: 'RAPID FIRE', ring: 0xb8ff40 },
  spread: { type: 5, int: 0.40, shots: 3, fan: 0.2,  label: 'SPREAD',    ring: 0x40e0ff },
  rocket: { type: 6, int: 0.60, shots: 1, fan: 0,    label: 'ROCKETS',   ring: 0xff8a20 },
  rail:   { type: 7, int: 0.80, shots: 1, fan: 0,    label: 'RAILGUN',   ring: 0xa0c8ff },
};
// per projectile type: 0 rifle, 1 laser, 2 hero, 3 hero+ATK, 4 rapid, 5 spread, 6 rocket, 7 rail
const PDMG = [1, 2.5, 5, 12.5, 1.2, 1.0, 5, 7];
const PHW = [0.42, 0.42, 0.55, 0.55, 0.4, 0.42, 0.6, 0.5];   // hit half-width
const PSPL = [0, 0, 0, 0, 0, 0, 1.6, 0];                    // splash radius (rockets)
let W = WEAPONS.rifle, wName = 'rifle';

// ---- enemy types: 0 grunt, 1 brute (tanky; survives several melee trades), 2 runner (fast, aggros early)
const ETYPE = { grunt: 0, brute: 1, runner: 2 };
const EHP = [1, 5, 1], ESPD = [1, 1, 1.75], EAGG = [0, 0, 5], ESCL = [1, 1.42, 0.86];
const ECOL = [[1, 1, 1], [0.6, 0.48, 0.78], [1.4, 1.15, 0.45]];

// ---- gate styles
const GATE_STYLE = {
  add:  { glass: [0.03, 0.2, 0.95], glow: [0.05, 0.3, 1.0], edge: '#0b41c4' },
  big:  { glass: [1.0, 0.5, 0.02],  glow: [1.0, 0.5, 0.04], edge: '#b05a00' },
  x:    { glass: [0.55, 0.08, 0.95], glow: [0.6, 0.1, 1.0], edge: '#5a0ca8' },
  '-':  { glass: [0.95, 0.04, 0.05], glow: [1.0, 0.08, 0.05], edge: '#8a0010' },
  w:    { glass: [0.02, 0.8, 0.45],  glow: [0.05, 1.0, 0.5],  edge: '#04664a' },
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
  const op = spec.weapon ? 'w' : (spec.op || '+'), v = spec.val || 1;
  const kind = op === 'w' ? 'w' : op === 'x' ? 'x' : op === '-' ? '-' : '';
  const style = GATE_STYLE[kind || (v < 10 ? 'add' : 'big')];
  const label = op === 'w' ? (WEAPONS[spec.weapon] || WEAPONS.laser).label.split(' ')[0] : op === 'x' ? '×' + v : op === '-' ? '−' + v : '+' + v;
  return { x: LANE_X, d: REL * t, t, val: v, kind, weapon: spec.weapon, label, glass: style.glass, glow: style.glow, mesh: gateMeshFor(label, style.edge), alive: true };
}
function setWeapon(name) {
  wName = WEAPONS[name] ? name : 'laser'; W = WEAPONS[wName];
  atk = wName !== 'rifle'; setSoldierLook(atk);
  popup(W.label, clamp(X, -2, 2), 3.4, D + 2, '#ffe23a', '#3a1d00', 2.7, 1.6, 1.4);
}
function gateSpecial(g) {
  if (g.kind === 'x') {
    addSoldiers(Math.max(0, Math.min(MAXS - N, Math.round(N * (g.val - 1)))), g.x - 0.6, g.d, 1.3);
    sfx.gate99(); popup(g.label, g.x - 0.6, 3.0, g.d, '#f0c8ff', '#3a0a5a', 3.4, 1.0, 2.2);
    burst(g.x, 1, g.d, 60, 10, 1.6, 0.5, 2.4, 1.1, 0.5, -5, 3); ring(g.x, g.d, 0.5, 6, 0.4, 0xc070ff); shake = Math.max(shake, 0.25);
  } else if (g.kind === '-') {
    const k = Math.min(N, g.val);
    for (let n = 0; n < k; n++) { let best = 0, bd = 1e9; for (let i = 0; i < N; i++) { const q = Math.abs(sX[i] - g.x) + Math.abs(sD[i] - g.d); if (q < bd) { bd = q; best = i; } } killSoldier(best); }
    popup(g.label, g.x - 0.6, 3.0, g.d, '#ff8080', '#4a0000', 3.2, 1.0, 2.2); burst(g.x, 1, g.d, 40, 8, 2.4, 0.3, 0.2, 1.0, 0.5, -5, 3);
    ring(g.x, g.d, 0.5, 6, 0.4, 0xff3030); shake = Math.max(shake, 0.35);
    if (N <= 0) loseMsg = 'A red gate took your last soldiers.<br>Steer off the belt when a minus gate comes!';
  } else if (g.kind === 'w') {
    setWeapon(g.weapon); sfx.power(); fovK = 1;
    burst(X, 0.8, D, 60, 9, 0.4, 2.4, 1.4, 1.2, 0.6, -4, 3); ring(X, D, 0.5, 6.5, 0.5, W.ring);
  }
}
function splash(x, d, r, dmg) { // rocket blast: damages every enemy in the radius
  const r2 = r * r;
  for (let j = 0; j < E; j++) { if (eHp[j] <= 0) continue; const dx = eX[j] - x, dd = eD[j] - d; if (dx * dx + dd * dd < r2) { eHp[j] -= dmg; if (eHp[j] <= 0) killEnemy(j, true); } }
  if (PT < MAXPT - 250) burst(x, 0.8, d, 8, 7, 2.4, 1.1, 0.2, 1.0, 0.3, -6, 2);
  if (thr('boom', 70)) noise(0.16, 0.05, 2500, 200);
}

// ---- levels
const STOCK_LEVEL = {
  name: 'STAGE 1',
  gates: [{ t: 2.0, every: 0.4, count: 49, val: 1 }, { t: 23.0, every: 1.1, count: 3, val: 99 }],
  horde: [{ x0: -6.05, x1: 2.85, d0: 17.5, d1: 62.6, gap: 0.62, type: 'grunt' }],
  cage: { x: -4.6, d: 16.2, hp: 30, weapon: 'laser' },
  bosses: [{ kind: 0, at: 12.6, ahead: 26 }, { kind: 1, at: 21.0, ahead: 26 }],
  final: { hp: 9999, cap: 36, speed: 2.2, wakeAt: 29 },
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
  return o;
}
function checkLevel(Lv) { // the engine's hard limits; a broken level still loads, but says why in the console
  const w = [], times = [];
  for (const g of Lv.gates) {
    if (g.weapon && !WEAPONS[g.weapon]) w.push('unknown weapon "' + g.weapon + '" (have: ' + Object.keys(WEAPONS) + ')');
    if (!g.weapon && !(g.val >= 1)) w.push('gate values must be >= 1 (use op: "-" for minus gates)');
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
  for (const b of Lv.bosses) if (b.kind !== 0 && b.kind !== 1) w.push('mid-bosses must be kind 0 or 1 (kind 2 is the final boss and ends the level)');
  if (Lv.cage.weapon && !WEAPONS[Lv.cage.weapon]) w.push('unknown cage weapon "' + Lv.cage.weapon + '"');
  if (Lv.cage.x > -2) w.push('keep the cage at x <= -2: the squad is pushed to its right side, and the belt is at x = ' + LANE_X);
  if (Lv.final.wakeAt > D_MAX) w.push('final.wakeAt must be <= ' + D_MAX + ' (the squad stops advancing there)');
  return w;
}

// ---- generator: every level past the hand-made ones. Seeded, so level N is always the same level.
function rng(seed) { let a = seed >>> 0; return () => { a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function generateLevel(n) {
  const R = rng(n * 9973 + 17), pick = a => a[Math.floor(R() * a.length)], k = Math.min(1, (n - 1) / 30); // k: difficulty 0..1 over 30 levels
  const unlocked = ['laser'].concat(n >= 3 ? ['rapid'] : [], n >= 4 ? ['spread'] : [], n >= 5 ? ['rocket'] : [], n >= 7 ? ['rail'] : []);
  const wakeAt = Math.round(29 + k * 9), tWake = wakeAt / V_SQUAD;
  const cage = { x: -4.6 + R() * 0.8, d: 13 + R() * 5, hp: Math.min(60, 30 + Math.round(n * 1.5)), weapon: n < 4 ? 'laser' : pick(unlocked) };
  // gate timeline: a stream of small gates, some of them swapped for multipliers, traps and a weapon; big gates near the boss
  const bigT = tWake - 1.2 - R() * 0.6, every = 0.38 + R() * 0.15 + k * 0.08, sv = n >= 6 && R() < 0.5 ? 2 : 1;
  const slots = []; for (let t = 1.8; t < bigT - 1.4 && slots.length < 62; t += every) slots.push({ t: +t.toFixed(2), val: sv });
  const at = f => slots[Math.min(slots.length - 1, Math.floor(slots.length * f))];
  if (n >= 2) Object.assign(at(0.42 + R() * 0.1), { op: 'x', val: 2 });
  if (n >= 8 && R() < 0.6) Object.assign(at(0.7 + R() * 0.08), { op: 'x', val: 2 });
  if (n >= 3) { const traps = Math.min(4, 1 + Math.floor(n / 6)); for (let i = 0; i < traps; i++) { const s = at(0.2 + R() * 0.75); if (!s.op) s.op = '-'; } }   // trap sizes are set below
  if (n >= 3) { const wpn = pick(unlocked.filter(w => w !== cage.weapon)); const s = at(0.55 + R() * 0.1); delete s.op; s.val = 1; s.weapon = wpn; }
  const bigN = 2 + Math.floor(R() * 3), bigV = pick([50, 99]), bigE = 1.0 + R() * 0.2;
  for (let i = 0; i < bigN; i++) slots.push({ t: +(bigT + i * bigE).toFixed(2), val: bigV });
  // expected squad if every gate is taken (traps included), used to size the boss and the stars
  let ex = 1; for (const s of slots) {
    if (s.weapon) continue;
    if (s.op === '-') s.val = Math.max(2, Math.round(ex * (0.12 + 0.13 * k)));   // a trap costs a share of the squad you should have by then
    ex = s.op === 'x' ? ex * s.val : s.op === '-' ? Math.max(1, ex - s.val) : ex + s.val; ex = Math.min(MAXS, ex);
  }
  // horde: bands along the bridge, tougher types unlock as levels go on
  const types = ['grunt'].concat(n >= 2 ? ['runner'] : [], n >= 3 ? ['brute'] : []), d0 = cage.d + 1.3, d1 = 62.6, bands = 2 + Math.floor(R() * 2);
  const horde = []; let cells = 0;
  for (let i = 0; i < bands; i++) {
    const a = d0 + (d1 - d0) * i / bands, b = d0 + (d1 - d0) * (i + 1) / bands - 0.6, type = i === 0 ? 'grunt' : pick(types);
    const h = { x0: -6.05, x1: 2.85, d0: +a.toFixed(1), d1: +b.toFixed(1), gap: type === 'brute' ? 0.9 : 0.62, type };
    if (type === 'brute') h.hp = 4 + Math.floor(n / 6);
    horde.push(h); cells += ((b - a) / h.gap + 1) * (8.9 / h.gap + 1);
  }
  if (cells > 1250) for (const h of horde) h.gap = +(h.gap * Math.sqrt(cells / 1250)).toFixed(2);
  const nb = Math.min(3, 1 + Math.floor(n / 4)), bosses = [];
  for (let i = 0; i < nb; i++) { const kind = i % 2; bosses.push({ kind, at: +(12 + (wakeAt - 19) * (nb > 1 ? i / (nb - 1) : 0)).toFixed(1), ahead: 24 + Math.floor(R() * 3), hp: Math.round((kind ? 1200 : 520) * (1 + k * 0.7)) }); }
  const soak = 3.4 + k * 0.9;  // seconds of full-squad fire the final boss soaks
  return { name: 'STAGE ' + n, generated: true, gates: slots, horde, cage, bosses, final: { hp: Math.max(4000, Math.round(ex * 0.85 * 7.4 * soak / 100) * 100), wakeAt }, stars: [Math.round(ex * 0.45), Math.round(ex * 0.8)] };
}
const HAND_LEVELS = (() => {
  try { const m = location.hash.match(/lvl=([^&]+)/); if (m) return [JSON.parse(decodeURIComponent(escape(atob(m[1].replace(/-/g, '+').replace(/_/g, '/')))))]; } catch (e) { console.warn('bad #lvl= level', e); }
  return (window.BRIDGE_LEVELS && window.BRIDGE_LEVELS.length) ? window.BRIDGE_LEVELS : [STOCK_LEVEL];
})();
const levelCache = [];
function getLevel(i) {
  if (!levelCache[i]) {
    const lv = normLevel(i < HAND_LEVELS.length ? HAND_LEVELS[i] : generateLevel(i + 1), i);
    checkLevel(lv).forEach(m => console.warn('[level ' + (i + 1) + ' ' + lv.name + '] ' + m));
    levelCache[i] = lv;
  }
  return levelCache[i];
}
window.__bridgeLevel = i => getLevel(i - 1);   // inspect any level from the console: __bridgeLevel(12)
let LI = Math.max(0, (parseInt(new URLSearchParams(location.search).get('level'), 10) || 1) - 1);
let L = null, bossQ = [];
"""

APPLY_LEVEL = r"""function applyLevel() {
  L = getLevel(LI);
  CAGE_X = L.cage.x; CAGE_D = L.cage.d; CAGE_HP = L.cage.hp;
  cage.group.position.set(CAGE_X, 0, -CAGE_D);
  W = WEAPONS.rifle; wName = 'rifle';
  const cw = WEAPONS[L.cage.weapon] || WEAPONS.laser, lc = lblCrate.ctx; lc.clearRect(0, 0, 640, 160);
  fancyText(lc, cw.label, 320, 80, cw.label.length > 8 ? 92 : 108, '#ffe23a', '#6a0a56', 22); lblCrate.tex.needsUpdate = true;
  $('hudL').textContent = L.name;
  try { const u = new URL(location.href); if (u.searchParams.get('level') !== String(LI + 1) && !location.hash) { u.searchParams.set('level', LI + 1); history.replaceState(null, '', u); } } catch (e) {}
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
  gates.length = 0;
  for (let j = 0; j < 49; j++) gates.push({ x: LANE_X, d: REL * (2.0 + 0.4 * j), val: 1, alive: true });
  for (let j = 0; j < 3; j++) gates.push({ x: LANE_X, d: REL * (23.0 + j * 1.1), val: 99, alive: true });
"""
HORDE_NEW = """  // horde: one grid of enemies per rectangle, leaving room around the cage
  for (const h of L.horde) for (let d = h.d0; d <= h.d1 + 0.01; d += h.gap) for (let x = h.x0; x <= h.x1 + 0.01; x += h.gap) {
    if (Math.abs(x - CAGE_X) < 2.2 && Math.abs(d - CAGE_D) < 2.6) continue;
    if (E >= MAXE) break;
    eX[E] = x + rand(-0.13, 0.13); eD[E] = d + rand(-0.13, 0.13); eHp[E] = h.hp; eTy[E] = h.ty; eSt[E] = 0; ePh[E] = Math.random() * TAU; E++;
  }
  // gates on the belt: a gate with arrival time t starts at distance REL*t and meets the squad front at t seconds
  gates.length = 0;
  for (const g of L.gates) for (let j = 0; j < g.count; j++) gates.push(makeGate(g, g.t + g.every * j));
  gates.sort((a, b) => a.d - b.d);
"""

PATCHES = [  # (old, new, expected count) -- applied in order
    # ---- level data
    ("const CAGE_X = -4.6, CAGE_D = 16.2, CAGE_HP = 30;", "let CAGE_X = -4.6, CAGE_D = 16.2, CAGE_HP = 30;", 1),
    ("let E = 0;\n", "let E = 0;\nconst eTy = new Uint8Array(MAXE);\n", 1),
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
    ("if (!b.active) { if (D >= 29)", "if (!b.active) { if (D >= L.final.wakeAt)", 1),
    ("clamp(D / 29, 0, 1)", "clamp(D / L.final.wakeAt, 0, 1)", 1),
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
    ("const PSPEED = [36, 54, 36, 54], PWID = [0.34, 0.72, 0.7, 1.5], PLEN = [1.4, 5.0, 2.2, 6.4], PRANGE = [RANGE, RANGE, RANGE + 2, RANGE + 2];",
     "const PSPEED = [36, 54, 36, 54, 44, 40, 24, 70], PWID = [0.34, 0.72, 0.7, 1.5, 0.3, 0.42, 0.95, 0.5], PLEN = [1.4, 5.0, 2.2, 6.4, 1.8, 1.6, 1.3, 9.0], PRANGE = [RANGE, RANGE, RANGE + 2, RANGE + 2, RANGE, RANGE - 2, RANGE + 2, RANGE + 8];", 1),
    ("const PCOL = [[1.9, 0.95, 0.05], [1.75, 0.045, 1.02], [2.0, 1.15, 0.1], [1.9, 0.08, 1.2]];",
     "const PCOL = [[1.9, 0.95, 0.05], [1.75, 0.045, 1.02], [2.0, 1.15, 0.1], [1.9, 0.08, 1.2], [1.3, 2.0, 0.15], [0.15, 1.5, 2.1], [2.3, 0.65, 0.08], [1.2, 1.7, 2.5]];", 1),
    ("function fire(x, d, type) {", "function fire(x, d, type, ang = 0) {", 1),
    ("if (nCh > 0 && type < 2)", "if (nCh > 0 && type !== 2 && type !== 3)", 1),
    ("  pX[P] = x; pD[P] = d; pS[P] = 0; pT[P] = type; pUX[P] = ux; pUD[P] = ud;",
     "  if (ang && ux === 0) { const c = Math.cos(ang), s = Math.sin(ang), u = ux; ux = u * c + ud * s; ud = -u * s + ud * c; }\n"
     "  pX[P] = x; pD[P] = d; pS[P] = 0; pT[P] = type; pUX[P] = ux; pUD[P] = ud;", 1),
    ("pDmg[P] = type === 0 ? 1 : type === 1 ? 2.5 : type === 2 ? 5 : 12.5;", "pDmg[P] = PDMG[type];", 1),
    ("sCd[i] += FIRE_INT; sKick[i] = 1; fire(sX[i] + 0.31, sD[i] + 0.95, atk ? 1 : 0);",
     "sCd[i] += W.int; sKick[i] = 1; for (let k = 0; k < W.shots; k++) fire(sX[i] + 0.31, sD[i] + 0.95, W.type, (k - (W.shots - 1) / 2) * W.fan);", 1),
    ("const pw = (ty >= 2 ? 0.55 : 0.42)", "const pw = PHW[ty]", 1),
    ("          const h = eHp[j]; eHp[j] -= dmg; dmg -= h;",
     "          if (PSPL[ty]) { splash(eX[j], eD[j], PSPL[ty], dmg); dead = true; break scan; }\n"
     "          const h = eHp[j]; eHp[j] -= dmg; dmg -= h;", 1),
    ("pa[o + 13] = t >= 2 ? 2.4 : 0.84;", "pa[o + 13] = (t === 2 || t === 3) ? 2.4 : 0.84;", 1),
    ("  atk = true; setSoldierLook(true); fovK = 1;\n  popup('ATK+150%', clamp(X, -2, 2), 3.4, D + 2, '#ffe23a', '#3a1d00', 2.7, 1.6, 1.4);",
     "  setWeapon(L.cage.weapon); fovK = 1;", 1),
    # ---- enemy types
    ("if (eD[i] - front < 6 && Math.abs(eX[i] - X) < hw + 3.2) eSt[i] = 1;",
     "if (eD[i] - front < 6 + EAGG[eTy[i]] && Math.abs(eX[i] - X) < hw + 3.2 + EAGG[eTy[i]] * 0.5) eSt[i] = 1;", 1),
    ("st = CHARGE_V * dt;", "st = CHARGE_V * ESPD[eTy[i]] * dt;", 1),
    ("if (best >= 0) { killSoldier(best); killEnemy(i, true); }",
     "if (best >= 0) { killSoldier(best); if (eTy[i] === 1 && eHp[i] > 1) eHp[i] -= 1; else killEnemy(i, true); }", 1),
    ("eSt[i] = eSt[E]; ePh[i] = ePh[E]; }", "eSt[i] = eSt[E]; ePh[i] = ePh[E]; eTy[i] = eTy[E]; }", 1),
    ("scl = 0.94 + (ePh[i] % 1) * 0.14;", "scl = (0.94 + (ePh[i] % 1) * 0.14) * ESCL[eTy[i]], ct = ECOL[eTy[i]];", 1),
    ("fc[nfar * 3] = tint; fc[nfar * 3 + 1] = tint * 0.92; fc[nfar * 3 + 2] = tint * 0.92;",
     "fc[nfar * 3] = tint * ct[0]; fc[nfar * 3 + 1] = tint * 0.92 * ct[1]; fc[nfar * 3 + 2] = tint * 0.92 * ct[2];", 1),
    ("ec[ne * 3] = tint; ec[ne * 3 + 1] = tint * 0.92; ec[ne * 3 + 2] = tint * 0.92;",
     "ec[ne * 3] = tint * ct[0]; ec[ne * 3 + 1] = tint * 0.92 * ct[1]; ec[ne * 3 + 2] = tint * 0.92 * ct[2];", 1),
    # ---- endless progression + stars
    ("'PLAY AGAIN', N >= 300 ? 3 : N >= 150 ? 2 : 1", "'NEXT STAGE', N >= L.stars[1] ? 3 : N >= L.stars[0] ? 2 : 1", 1),
    ("function startGame() {\n  initAudio(); reset();",
     "function startGame(advance) {\n  if (advance && state === 'won') LI++;\n  initAudio(); reset();", 1),
    ("startGame(); return; }", "startGame(true); return; }", 1),
    ("state !== 'play') startGame();", "state !== 'play') startGame(true);", 1),
    ("get s() { return { state,", "get s() { return { level: LI, name: L.name, weapon: wName, state,", 1),
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
