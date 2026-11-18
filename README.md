# Bridge Squad: levels kit

![Bridge Squad: Endless cover art](docs/cover.svg)

**Play it:** https://thedjpetersen.com/games/bridge-squad/

This kit turns [Bridge Squad](https://noclipepe.pages.dev/bridge/), the one-level browser game by [@noclipepe](https://x.com/noclipepe), into a game with **any number of levels**. It also adds **weapons**, **gate types** and **enemy types**.

![Eight themes: dusk, day, sunset, neon, toxic, frost, desert, storm](docs/themes.png)

This repo does **not** contain the game itself. `setup.sh` downloads the original from noclipepe's site and patches it on your machine.

```sh
./setup.sh                      # download the original game and build index.html
python3 -m http.server 8731     # then open http://127.0.0.1:8731/?level=1
```

## What the kit adds

| | |
|---|---|
| **Levels** | Six hand-made stages in `levels.js`. Every level number after them is **generated** from a seed, so `?level=57` is the same level for everyone. A win leads to **NEXT STAGE**, with no end. |
| **Level archetypes** | Generated levels draw from classic, SWARM (runners), SAWS (saw blades and a shield gate), ARSENAL (several weapon gates and frenzy), BOOM (barrels and bombers), SIEGE (brutes), BOSS RUSH (up to four mid-bosses) and FROST (freeze from the cage). |
| **Weapons** | `rifle`, `laser` (the original ATK+150%), `rapid`, `spread`, `rocket` (splash damage), `rail` (pierces), `flame` (short range, burns through crowds), `shock` (Tesla: chains to 3 more enemies), `freeze` (slows enemies and bosses). The cage crate gives one, and weapon gates give others. |
| **Gates** | `+N` (blue, or gold for 10+), `×N` (purple), `−N` and `÷N` traps (red; steer off the belt), weapon gates (green), **FRENZY** (double fire rate for a few seconds) and **SHIELD** (no melee, saw or mid-boss losses for a few seconds). |
| **Enemies** | `grunt`, `brute` (big and tanky; survives several melee trades), `runner` (fast, aggros early), `bomber` (explodes when killed and takes extra soldiers with it in melee; chain reactions!). |
| **Themes** | Eight original looks for sky, water, deck and lighting: dusk (stock), day, sunset, neon, toxic, frost, desert and storm. Each archetype has a default, and any level can set `theme:`. |
| **Hazards** | **Saw blades** sweep across the belt or the deck at a fixed point. **Explosive barrels** sit in the horde: shoot one to blast everything around it. |

## Tracking the original

noclipepe's game changes over time. In November 2026 it gained a second stage, Flood Rescue, with a stage menu and reworked code. The kit drives the bridge stage (stage 1) and leaves Flood Rescue as it is; a win on the bridge moves on to the next kit level. When the original changes again, `setup.sh` fails and names the patch anchor that no longer matches, and the web page tells players and links to the original.

## Putting it on a website

`web/index.html` is a page that fetches the original game from noclipepe's site, applies `patches.json` in the browser and runs it. The original is never rehosted. If the original changes so the patches no longer fit, the page says so and links to it.

To deploy, run `./setup.sh` (which also writes `patches.json`). Then put `web/index.html` in a folder together with `patches.json`, `levels.js`, and `docs/cover.svg` and `docs/cover.jpg` (renamed to `cover.svg` and `cover.jpg`). `art/cover.py` regenerates the cover art.

## How the original works

The game is one HTML page plus `three.min.js`. The game script is stored as text in `<script type="text/plain" id="main">` and runs once three.js has loaded. It uses no image or sound files: every mesh, texture and sound is generated in code.

The original has a single level, written directly into `reset()` and `update()`. `build.py` applies 45 exact-match patches to read the level from data and to add the new mechanics. If the original page changes and an anchor no longer matches, the build fails instead of producing a broken game.

## Level format (`levels.js`)

```js
{
  name: 'STAGE 7',
  theme: 'neon',                                 // dusk, day, sunset, neon, toxic, frost, desert, storm
  gates: [                                       // conveyor timeline; t = second the gate reaches the squad
    { t: 2.0, every: 0.4, count: 20, val: 1 },   // 20 "+1" gates, one every 0.4 s
    { t: 10.2, op: 'x', val: 2 },                // ×2 multiplier
    { t: 12.0, op: '-', val: 8 },                // −8 trap
    { t: 15.0, weapon: 'rocket' },               // weapon gate
    { t: 16.0, op: '/', val: 2 },                // ÷2 trap
    { t: 17.0, buff: 'frenzy', secs: 6 },        // or buff: 'shield'
    { t: 23.0, every: 1.1, count: 3, val: 99 },  // gold +99s
  ],
  horde: [                                       // rectangles filled with a grid of enemies
    { x0: -6.05, x1: 2.85, d0: 17.5, d1: 40, gap: 0.62, type: 'grunt' },
    { x0: -6.05, x1: 2.85, d0: 40.6, d1: 62.6, gap: 0.9, type: 'brute', hp: 5 },
  ],
  cage: { x: -4.6, d: 16.2, hp: 30, weapon: 'laser' },   // shoot it open: frees the hero, drops this weapon
  hazards: [
    { type: 'saw', d: 11, x0: 1.5, x1: 6.2, speed: 1.6, phase: 0 },   // sweeps between x0 and x1 at distance d
    { type: 'barrel', x: -2, d: 21, hp: 4, radius: 3.2 },
  ],
  bosses: [ { kind: 0, at: 12.6, ahead: 26 }, { kind: 1, at: 21, hp: 1500, cap: 9 } ],
  final: { hp: 9999, cap: 36, speed: 2.2, wakeAt: 29 },
  stars: [150, 300],                             // squad size needed for 2 and 3 stars
}
```

Any field you leave out takes the stock Stage 1 value. A broken level still loads, and the browser console says what is wrong with it.

**Testing levels**
- Try a level without editing files: `#lvl=<base64url JSON>`.
- Inspect any level from the console with `__bridgeLevel(n)`, including generated ones.

**Coordinates**
- x runs across the deck, from −6.6 to 6.6. The conveyor belt is at x = 4.95 ± 1.5.
- d is distance along the bridge. The squad moves at 1.2 d/s and stops at d = 55. The fortress is at d = 68.
- Gates move at 7 d/s, so a gate's `t` is the second it reaches the squad front.

## Numbers from the code

**Weapons**

| weapon | damage per shot | seconds between shots | notes |
|---|---|---|---|
| rifle | 1 | 0.34 | start weapon |
| laser | 2.5 | 0.34 | the original ATK crate |
| rapid | 1.2 | 0.15 | |
| spread | 3 × 1.0 | 0.40 | fans out against the horde, converges on bosses |
| rocket | 5 | 0.60 | splash radius 1.6 |
| rail | 7 | 0.80 | damage carries through enemies; range +8 |
| flame | 2 × 1.2 | 0.30 | range 14; keeps full damage through a crowd. A horde weapon: the generator never hands it out last |
| shock | 2.8 | 0.40 | chains to 3 more enemies, losing 25% each hop |
| freeze | 1.6 | 0.34 | slows enemies to 35% for 2.5 s and bosses to 45% for 1.5 s; the generator never hands it out last |

Upgraded weapons all deal about 7.4–8.5 damage per second per soldier against a boss. They differ in how they deal with the horde. The hero fires every 0.25 s for 5 damage (12.5 once upgraded).

**Bosses**

| kind | default hp | smash cap | notes |
|---|---|---|---|
| 0 | 520 | 5 | |
| 1 | 1200 | 9 | |
| 2 | 9999 | 36 | final boss only; its leap slam wipes out the whole squad |

**Caps:** at most 480 soldiers, 1300 enemies, and 72 gates on screen (about 25 s of the timeline).

**Balancing rule of thumb:** an upgraded squad of N soldiers deals about 7.4 × N damage per second, and the final boss reaches the squad 4–6 s after it wakes. Keep `final.hp` at or below about 7.4 × expected squad × 4.

## The generator

`generateLevel(n)` in `build.py` builds each level from a seed.

**Difficulty ramp:** difficulty rises over the first 30 levels and then plateaus. Each level picks an archetype from those unlocked so far. Weapons unlock in this order:

| level | weapon unlocked |
|---|---|
| 3 | rapid |
| 4 | spread |
| 5 | rocket |
| 6 | flame |
| 7 | rail |
| 9 | shock |
| 11 | freeze |

**What a generated level contains**
- A stream of small gates. Some are swapped for ×2 gates, traps and one weapon gate.
- Gold gates as the boss wakes.
- 2–3 bands of horde.
- 1–3 mid-bosses.

**Boss and trap sizing:** the generator works out the squad size you should reach by taking every gate. The final boss's HP and the star thresholds come from that number. Each trap costs a share of the squad you should have at that moment.

## Play-testing

```sh
python3 -m http.server 8731 &
node playtest.mjs http://127.0.0.1:8731/ 1 2 3 10 50   # needs Playwright
```

A simple bot plays each level. It dodges traps and saws, breaks the cage, grabs the crate, collects gates and tracks the boss. The last runs all ended in a win:

| level | archetype | squad | weapon at the boss |
|---|---|---|---|
| 1 (stock) | classic | 336 | laser |
| 2 | spread gate, runners | 228 | spread |
| 3 | traps, brutes | 452 | rocket |
| 4 | saws, shield, tesla | 342 | shock |
| 5 | barrels, bombers, flamer | 342 | rocket |
| 6 | frost, boss rush, ÷2 | 268 | rail |
| 7 / 9 / 13 / 27 | ARSENAL | 473 / 433 / 310 / 252 | rocket / rocket / shock / spread |
| 8 / 14 / 60 | SWARM | 268 / 279 / 179 | laser / rocket / laser |
| 10 / 20 / 30 | BOSS RUSH | 266 / 139 / 214 | spread / rapid / spread |
| 11 / 23 / 77 | SIEGE | 358 / 191 / 210 | rocket / laser / shock |
| 16 | SAWS | 149 | spread |
| 18 / 100 | BOOM | 210 / 192 | rapid / rail |
| 33 | classic | 457 | rapid |
| 45 | FROST | 245 | spread |

These are bot results; difficulty for a human player hasn't been tuned by hand.

## Credit

Bridge Squad, its art, code and design are by [@noclipepe](https://x.com/noclipepe). This repo contains only the patcher, the level data and the tooling.
