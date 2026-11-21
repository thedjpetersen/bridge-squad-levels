// Headless Flood Rescue play-test: a bot plays a flood level and reports the result.
// Usage: node floodtest.mjs "http://127.0.0.1:8731/?flood=3" [runs]   (serve this folder first)
import { createRequire } from 'module'; import { execSync } from 'child_process';
const pw = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const url = process.argv[2], runs = +(process.argv[3] || 1);
const BOT = () => new Promise(done => {
  const G = window.__game, log = [];
  const steer = wx => window.dispatchEvent(new PointerEvent('pointermove', { clientX: G.screenX(wx), clientY: 300, pointerType: 'mouse' }));
  window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }));
  let last = -1;
  const tick = () => {
    const s = G.s;
    if (s.state !== "play") return done({ name: s.fname, result: s.state, t: +s.t.toFixed(1), N: s.N, kills: s.kills, tier: s.tier, log });
    let tx, why;
    const near = s.g2.filter(g => g.d < s.D + s.hd + 14);
    const pumpTime = s.tank.phase !== 3 && s.tank.phase !== 1 && s.t > 12 && s.N >= 8;
    const take = near.find(g => g.val > 0 && g.d < s.D + s.hd + (pumpTime ? 1.8 : 4));
    const bad = near.find(g => g.val <= 0 && g.d < s.D + s.hd + 2.2);
    const work = near.find(g => g.val < g.max);
    const boss = s.bosses.find(b => b.active && b.hp > 0 && b.d < s.D + 14);
    if (take) { tx = take.x; why = 'take'; }
    else if (bad) { tx = bad.x > 0 ? bad.x - 3.6 : bad.x + 3.6; why = 'dodge'; }
    else if (pumpTime) { tx = 6; why = 'pump'; }
    else if (boss && s.tier >= 1) { tx = boss.x; why = 'boss'; }
    else if (work && (s.tank.phase === 1 || s.tank.phase === 3 || s.N < 6)) { tx = work.x; why = 'gate'; }
    else if (s.tank.phase !== 3) { tx = 6; why = 'pump'; }
    else if (work) { tx = work.x; why = 'gate'; }
    else { tx = 0; why = 'lane'; }
    steer(Math.max(-7, Math.min(7, tx)));
    const sec = Math.floor(s.t);
    if (s.od >= 1 && s.odT <= 0 && s.bosses.some(b => b.active && b.d - s.D < 14)) window.dispatchEvent(new KeyboardEvent('keydown', { key: 'f' }));
    if (sec !== last && sec % 3 === 0) { last = sec; log.push(`${sec}s ${why} N=${s.N} tank=${s.tank.level.toFixed(2)}/${s.tank.phase} tier=${s.tier} E=${s.E} b=${s.bosses.map(b => b.kind + ':' + Math.round(b.hp)).join(',')}`); }
    requestAnimationFrame(tick);
  };
  tick();
});
const b = await pw.chromium.launch({ args: ['--use-angle=metal', '--ignore-gpu-blocklist'] });
const p = await b.newPage({ viewport: { width: 540, height: 900 } });
const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
for (let r = 0; r < runs; r++) {
  await p.goto(url); await p.waitForFunction(() => window.__game && document.getElementById('load')?.classList.contains('done'), null, { timeout: 90000 });
  if (!/flood=/.test(url)) { await p.click('.lvb[data-l="2"]'); await p.waitForTimeout(300); }
  const res = await p.evaluate(BOT); console.log(JSON.stringify(res));
}
console.log('errors', JSON.stringify(errs)); await b.close();
