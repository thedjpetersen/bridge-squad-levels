// Headless play-test: a simple bot plays each level and reports win/loss and the squad size over time.
// Usage: node playtest.mjs [baseUrl] [levelNumbers...]   (serve this folder first, e.g. python3 -m http.server 8731)
import { createRequire } from 'module';
import { execSync } from 'child_process';
const require = createRequire(import.meta.url);
let pw; try { pw = require('playwright'); } catch { pw = require(execSync('npm root -g').toString().trim() + '/playwright'); }

const base = process.argv[2] || 'http://127.0.0.1:8731/';
const levels = process.argv.slice(3).map(Number);

const BOT = () => new Promise(done => {
  const G = window.__game, log = [];
  const steer = wx => window.dispatchEvent(new PointerEvent('pointermove', { clientX: G.screenX(wx), clientY: 300, pointerType: 'mouse' }));
  window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }));
  let last = -1;
  const tick = () => {
    const s = G.s, lv = window.__bridgeLevel(s.level + 1);
    if (s.state !== 'play') return done({ level: s.level + 1, name: s.name, result: s.state, t: +s.t.toFixed(1), squad: s.N, weapon: s.weapon, finalHp: lv.final.hp, stars: lv.stars, hero: s.hero, kills: s.kills, log });
    let tx, why;
    const trap = s.gates.find(g => (g.kind === '-' || g.kind === '/') && g.d > s.D - 1 && g.d < s.D + s.hd + 9);
    const saw = s.hazards.find(h => h.type === 'saw' && h.d > s.D - s.hd - 1 && h.d < s.D + s.hd + 3);
    if (trap) { tx = -2; why = 'dodge'; }
    else if (saw && s.shieldT <= 0) { tx = (saw.x0 + saw.x1) / 2 > 0 ? -4.5 : 4.5; why = 'saw'; }
    else if (s.crate.state === 'idle' || s.crate.state === 'arc') { tx = s.crate.x; why = 'crate'; }
    else if (!s.cageOpen && s.N >= 6 && s.D + 19 > lv.cage.d - 1.75) { tx = lv.cage.x + 0.3; why = 'cage'; }
    else if (s.gates.length) { tx = 6; why = 'gates'; }
    else { const b = s.bosses.find(b => b.active && b.hp > 0) || s.bosses[0]; tx = b ? b.x : 0; why = 'boss'; }
    steer(tx);
    const sec = Math.floor(s.t);
    if (sec !== last && sec % 3 === 0) { last = sec; log.push(`${sec}s ${why} ${s.weapon} N=${s.N} cage=${Math.max(0, Math.round(s.cageHp))} bosses=${s.bosses.map(b => b.kind + ':' + Math.round(b.hp)).join(',')}`); }
    requestAnimationFrame(tick);
  };
  tick();
});

const browser = await pw.chromium.launch({ args: ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 540, height: 900 } });
const warnings = [];
page.on('console', m => { if (m.type() === 'warning' || m.type() === 'error') warnings.push(m.text()); });
page.on('pageerror', e => warnings.push('PAGEERROR ' + e.message));
const count = await (async () => { await page.goto(base); await page.waitForFunction(() => window.__game); return page.evaluate(() => window.BRIDGE_LEVELS.length); })(); // default: the hand-made levels
for (const n of levels.length ? levels : Array.from({ length: count }, (_, i) => i + 1)) {
  await page.goto(base + '?level=' + n);
  await page.waitForFunction(() => window.__game && document.getElementById('load').classList.contains('done'), null, { timeout: 60000 });
  const r = await page.evaluate(BOT);
  console.log(JSON.stringify(r, null, 1));
}
if (warnings.length) console.log('console warnings:\n' + [...new Set(warnings)].join('\n'));
await browser.close();
