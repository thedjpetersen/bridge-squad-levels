// Bridge Squad hand-made levels. Format: see README.md.
// Any level number past the end of this list is generated (seeded, so level N is always the same).
// Units: x = across the bridge (-6.6..6.6), d = distance along it, t = seconds after start
// (the squad advances 1.2 d per second, so it is at d = 1.2 * t).
window.BRIDGE_LEVELS = [
  { // the original stage, exactly as shipped
    name: 'STAGE 1',
    gates: [{ t: 2.0, every: 0.4, count: 49, val: 1 }, { t: 23.0, every: 1.1, count: 3, val: 99 }],
    horde: [{ x0: -6.05, x1: 2.85, d0: 17.5, d1: 62.6, gap: 0.62, type: 'grunt' }],
    cage: { x: -4.6, d: 16.2, hp: 30, weapon: 'laser' },
    bosses: [{ kind: 0, at: 12.6, ahead: 26 }, { kind: 1, at: 21.0, ahead: 26 }],
    final: { hp: 9999, cap: 36, speed: 2.2, wakeAt: 29 },
    stars: [150, 300],
  },
  { // introduces the x2 gate, a spread-gun gate and runners
    name: 'STAGE 2', theme: 'day',
    gates: [
      { t: 2.0, every: 0.45, count: 20, val: 2 },
      { t: 11.0, op: 'x', val: 2 },
      { t: 11.6, every: 0.45, count: 12, val: 2 },
      { t: 17.4, weapon: 'spread' },
      { t: 18.0, every: 0.45, count: 6, val: 2 },
      { t: 22.0, every: 1.0, count: 3, val: 50 },
    ],
    horde: [
      { x0: -6.05, x1: 2.85, d0: 17.5, d1: 30, gap: 0.62, type: 'grunt' },
      { x0: -6.05, x1: 2.85, d0: 30.6, d1: 44, gap: 0.62, type: 'runner' },
      { x0: -6.05, x1: 2.85, d0: 44.6, d1: 62.6, gap: 0.62, type: 'grunt' },
    ],
    cage: { x: -4.2, d: 14.0, hp: 45, weapon: 'laser' },
    bosses: [{ kind: 0, at: 10.0, ahead: 24 }, { kind: 1, at: 19.0, ahead: 26, hp: 1500 }],
    final: { hp: 8000, wakeAt: 31 },
    stars: [180, 320],
  },
  { // red trap gates to dodge, brutes, and rockets from the cage
    name: 'STAGE 3', theme: 'sunset',
    gates: [
      { t: 1.5, every: 0.35, count: 18, val: 1 },
      { t: 7.9, op: '-', val: 6, shoot: true, step: 4, cap: 3 },   // shoot it to turn it blue
      { t: 8.3, every: 0.35, count: 14, val: 1 },
      { t: 13.4, op: 'x', val: 2 },
      { t: 13.8, every: 0.35, count: 10, val: 1 },
      { t: 17.4, op: '-', val: 12, shoot: true, step: 5, cap: 4 },
      { t: 17.8, every: 0.35, count: 10, val: 1 },
      { t: 24.0, every: 1.0, count: 4, val: 99 },
    ],
    horde: [
      { x0: -6.05, x1: 2.85, d0: 19.4, d1: 36, gap: 0.6, type: 'grunt' },
      { x0: -6.05, x1: 2.85, d0: 36.6, d1: 48, gap: 0.9, type: 'brute', hp: 5 },
      { x0: -6.05, x1: 2.85, d0: 48.6, d1: 62.6, gap: 0.62, type: 'runner' },
    ],
    cage: { x: -4.6, d: 18.0, hp: 45, weapon: 'rocket' },
    bosses: [
      { kind: 0, at: 9.0, ahead: 24, hp: 700 },
      { kind: 1, at: 16.0, ahead: 26, hp: 1500 },
      { kind: 1, at: 24.0, ahead: 26, hp: 1800, cap: 12 },
    ],
    final: { hp: 14000, cap: 48, wakeAt: 34 },
    stars: [220, 400],
  },
  { // saw blades sweep the belt and the deck; a shield gate gets you through, a tesla gate chains through runners
    name: 'STAGE 4', theme: 'neon',
    gates: [
      { t: 1.8, every: 0.4, count: 16, val: 1 },
      { t: 8.4, buff: 'shield', secs: 5 },
      { t: 8.8, every: 0.4, count: 8, val: 2 },
      { t: 12.4, op: 'x', val: 2 },
      { t: 12.8, every: 0.4, count: 8, val: 2 },
      { t: 16.4, weapon: 'shock' },
      { t: 16.8, every: 0.4, count: 8, val: 2 },
      { t: 21.0, buff: 'dmg' },
      { t: 23.0, every: 1.1, count: 3, val: 99 },
    ],
    horde: [
      { x0: -6.05, x1: 2.85, d0: 17.5, d1: 30, gap: 0.62, type: 'grunt' },
      { x0: -6.05, x1: 2.85, d0: 30.6, d1: 46, gap: 0.62, type: 'runner' },
      { x0: -6.05, x1: 2.85, d0: 46.6, d1: 62.6, gap: 0.62, type: 'grunt' },
    ],
    cage: { x: -4.4, d: 15.0, hp: 40, weapon: 'laser' },
    hazards: [
      { type: 'saw', d: 11.0, x0: 1.5, x1: 6.2, speed: 1.6 },
      { type: 'saw', d: 22.0, x0: -6.0, x1: 0.5, speed: 2.0, phase: 1.5 },
    ],
    bosses: [{ kind: 0, at: 12.0, ahead: 24 }, { kind: 1, at: 20.0, ahead: 26, hp: 1400 }],
    final: { hp: 10000, wakeAt: 31 },
    stars: [160, 300],
  },
  { // explosive barrels in a horde of green bombers: one good shot sets off a chain reaction. Flamer from the cage
    name: 'STAGE 5', theme: 'toxic',
    gates: [
      { t: 1.8, every: 0.4, count: 22, val: 1 },
      { t: 10.8, op: 'x', val: 2 },
      { t: 11.2, every: 0.4, count: 16, val: 1 },
      { t: 18.0, op: '-', val: 10 },
      { t: 18.4, every: 0.4, count: 8, val: 1 },
      { t: 21.5, weapon: 'rocket' },
      { t: 22.0, buff: 'frenzy', secs: 7 },
      { t: 23.0, every: 1.0, count: 3, val: 99 },
    ],
    horde: [
      { x0: -6.05, x1: 2.85, d0: 17.5, d1: 28, gap: 0.62, type: 'grunt' },
      { x0: -6.05, x1: 2.85, d0: 28.6, d1: 46, gap: 0.62, type: 'bomber' },
      { x0: -6.05, x1: 2.85, d0: 46.6, d1: 62.6, gap: 0.62, type: 'grunt' },
    ],
    cage: { x: -4.6, d: 15.5, hp: 35, weapon: 'flame' },
    hazards: [
      { type: 'barrel', x: -2.0, d: 21.0 }, { type: 'barrel', x: 1.4, d: 25.0 }, { type: 'barrel', x: -4.6, d: 30.0 },
      { type: 'barrel', x: -0.8, d: 35.0 }, { type: 'barrel', x: 1.8, d: 41.0 }, { type: 'barrel', x: -3.2, d: 49.0 },
    ],
    bosses: [{ kind: 0, at: 11.0, ahead: 24 }, { kind: 1, at: 19.0, ahead: 26, hp: 1500 }],
    final: { hp: 10000, wakeAt: 30 },
    stars: [170, 320],
  },
  { // frost and a boss rush: freeze slows the horde and bosses, then swap to the railgun; watch the ÷2 gate
    name: 'STAGE 6', theme: 'frost',
    gates: [
      { t: 1.8, every: 0.38, count: 20, val: 1 },
      { t: 9.4, op: 'x', val: 2 },
      { t: 9.8, every: 0.38, count: 10, val: 2 },
      { t: 13.8, op: '/', val: 2 },
      { t: 14.2, every: 0.38, count: 10, val: 2 },
      { t: 18.2, buff: 'shield', secs: 6 },
      { t: 18.6, weapon: 'rail' },
      { t: 19.0, every: 0.38, count: 6, val: 2 },
      { t: 23.5, every: 1.0, count: 4, val: 50 },
    ],
    horde: [
      { x0: -6.05, x1: 2.85, d0: 17.5, d1: 36, gap: 0.75, type: 'grunt' },
      { x0: -6.05, x1: 2.85, d0: 36.6, d1: 62.6, gap: 0.95, type: 'brute', hp: 5 },
    ],
    cage: { x: -4.6, d: 14.5, hp: 35, weapon: 'freeze' },
    bosses: [
      { kind: 0, at: 9.0, ahead: 24, hp: 600 },
      { kind: 1, at: 13.0, ahead: 26, hp: 1300 },
      { kind: 0, at: 18.0, ahead: 24, hp: 900, cap: 7 },
      { kind: 1, at: 23.0, ahead: 26, hp: 1600 },
    ],
    final: { hp: 10000, wakeAt: 31 },
    stars: [150, 280],
  },
  { // ? gates you can shoot open, prisoner pods in the horde, splitters, and overdrive to finish
    name: 'STAGE 7', theme: 'aurora',
    gates: [
      { t: 1.8, every: 0.4, count: 14, val: 1 },
      { t: 7.6, mystery: true, inside: { op: 'x', val: 2 } },
      { t: 8.2, every: 0.4, count: 10, val: 2 },
      { t: 12.4, mystery: true },
      { t: 13.0, every: 0.4, count: 8, val: 2 },
      { t: 16.4, buff: 'rate' },
      { t: 17.0, mystery: true },
      { t: 17.6, every: 0.4, count: 6, val: 2 },
      { t: 23.0, every: 1.1, count: 3, val: 99 },
    ],
    horde: [
      { x0: -6.05, x1: 2.85, d0: 17.5, d1: 32, gap: 0.62, type: 'grunt' },
      { x0: -6.05, x1: 2.85, d0: 32.6, d1: 46, gap: 0.8, type: 'splitter' },
      { x0: -6.05, x1: 2.85, d0: 46.6, d1: 62.6, gap: 0.62, type: 'grunt' },
    ],
    cage: { x: -4.4, d: 15.0, hp: 40, weapon: 'laser' },
    hazards: [
      { type: 'pod', x: -1.2, d: 21.0, hp: 14, n: 12 }, { type: 'pod', x: 1.6, d: 28.0, hp: 18, n: 15 },
      { type: 'pod', x: -3.0, d: 37.0, hp: 22, n: 20 },
    ],
    bosses: [{ kind: 0, at: 11.0, ahead: 24 }, { kind: 1, at: 20.0, ahead: 26, hp: 1500 }],
    final: { hp: 11000, wakeAt: 31 },
    stars: [170, 320],
  },
];

// Flood Rescue levels (the second mode). Any number past the end of this list is generated.
// Units: x = across the plaza (gates sit between -4.4 and 4.4; the pump is at x = 6), d = distance up the lane
// (gates appear at d = 13.5 and roll toward the squad at 1.2 d per second), t = seconds after start.
// gates: { t, x, val (start value, negative = red), max (how high shooting can raise it), d, vx (slides side to side) }
// mix: share of each enemy type in the horde column, e.g. [['runner', 0.2]]. minis: { t, kind (0 brute, 1 big brute), hp, cap }.
// tank: water needed to fill it (stock 6.5). leak: how fast it drains. boss: { hp, speed, wake (seconds) }.
window.FLOOD_LEVELS = [
  { name: 'FLOOD 1' },   // the original stage, exactly as shipped
  {
    name: 'FLOOD 2 · LEAKY TANK', theme: 'storm', callout: 'LEAKY TANK!', leak: 0.012,
    tip: 'The tank leaks.<br>Keep the pump going or the water drains away.',
    gates: [
      { t: 0, x: -2.4, val: -4, d: 10.2, max: 4 }, { t: 5, x: 2.6, val: -4 }, { t: 9.5, x: -3.4, val: -5 }, { t: 14, x: 1.2, val: -6, max: 4 },
      { t: 18.5, x: -2.0, val: -7 }, { t: 23, x: 2.8, val: -6, max: 4 }, { t: 27.5, x: -3.6, val: -8 }, { t: 32, x: 0.6, val: -8, max: 4 },
    ],
    boss: { hp: 560 }, stars: [9, 16],
  },
  {
    name: 'FLOOD 3 · STAMPEDE', theme: 'sunset', callout: 'STAMPEDE!', march: 1.15, mix: [['runner', 0.3]],
    tip: 'Runners in the column.<br>Grow the squad fast.',
    gates: [
      { t: 0, x: -2.0, val: -3, d: 10.2, max: 4 }, { t: 4, x: 2.4, val: -4, max: 4 }, { t: 8.5, x: -3.0, val: -5, max: 4 }, { t: 13, x: 1.6, val: -5 },
      { t: 17.5, x: -1.6, val: -7, max: 4 }, { t: 22, x: 3.0, val: -6 }, { t: 26.5, x: -3.4, val: -8, max: 4 }, { t: 31, x: 0.8, val: -8 },
    ],
    boss: { hp: 620, speed: 2.2 }, stars: [10, 17],
  },
  {
    name: 'FLOOD 4 · SLIDING GATES', theme: 'neon', callout: 'SLIDING GATES!',
    tip: 'The gates slide side to side.<br>Chase them while you shoot.',
    gates: [
      { t: 0, x: -2.4, val: -4, d: 10.2, max: 4 }, { t: 5, x: 2.6, val: -4, vx: -1.0 }, { t: 9.5, x: -3.0, val: -6, vx: 1.2 }, { t: 14, x: 1.0, val: -5, max: 4, vx: -1.4 },
      { t: 18.5, x: -2.0, val: -8, max: 4, vx: 1.3 }, { t: 23, x: 2.8, val: -6, vx: -1.6 }, { t: 27.5, x: -3.8, val: -9, max: 4, vx: 1.5 }, { t: 32, x: 0.6, val: -8, vx: -1.8 },
    ],
    boss: { hp: 650 }, stars: [9, 16],
  },
  {
    name: 'FLOOD 5 · BRUTE SQUAD', theme: 'desert', callout: 'BRUTES!', mix: [['brute', 0.1]],
    tip: 'Two brutes and a tougher column.<br>Free a hero before the second one lands.',
    minis: [{ t: 13, hp: 130, cap: 4 }, { t: 25, kind: 1, hp: 220, cap: 5 }],
    gates: [
      { t: 0, x: -2.4, val: -4, d: 10.2, max: 4 }, { t: 4.5, x: 2.6, val: -4, max: 4 }, { t: 9, x: -3.4, val: -6 }, { t: 13.5, x: 1.0, val: -5, max: 4 },
      { t: 18, x: -2.0, val: -8, max: 4 }, { t: 22.5, x: 2.8, val: -6 }, { t: 27, x: -3.6, val: -9, max: 4 }, { t: 31.5, x: 0.6, val: -8, max: 4 },
    ],
    boss: { hp: 720, wake: 29 }, stars: [10, 18],
  },
  {
    name: 'FLOOD 6 · JACKPOT', theme: 'aurora', callout: 'JACKPOT GATE!', mix: [['bomber', 0.12]],
    tip: 'One deep red gate is worth a fortune.<br>Pour everything into it.',
    gates: [
      { t: 0, x: -2.4, val: -4, d: 10.2, max: 4 }, { t: 5, x: 2.6, val: -5 }, { t: 9.5, x: 0, val: -14, max: 14, d: 15 }, { t: 15, x: -3.0, val: -6, max: 4 },
      { t: 19.5, x: 2.0, val: -8 }, { t: 24, x: -2.6, val: -7, max: 4 }, { t: 28.5, x: 3.0, val: -9 }, { t: 33, x: -0.6, val: -8, max: 4 },
    ],
    boss: { hp: 800, wake: 29 }, d1: 82, stars: [14, 24],
  },
  {
    name: 'FLOOD 7 · THE TITAN', theme: 'frost', callout: 'THE TITAN!', tank: 8.5, march: 1.1, mix: [['runner', 0.08], ['brute', 0.05]],
    tip: 'A huge tank and a huge boss.<br>Free both heroes.',
    minis: [{ t: 14, hp: 160, cap: 4 }, { t: 26, kind: 1, hp: 320, cap: 5 }],
    gates: [
      { t: 0, x: -2.4, val: -4, d: 10.2, max: 4 }, { t: 4.5, x: 2.6, val: -5, max: 4 }, { t: 9, x: -3.4, val: -6, max: 4, vx: 0.9 }, { t: 13.5, x: 1.0, val: -6, max: 4 },
      { t: 18, x: -2.0, val: -8, max: 5 }, { t: 22.5, x: 2.8, val: -7, max: 4, vx: -1.1 }, { t: 27, x: -3.6, val: -9, max: 5 }, { t: 31.5, x: 0.6, val: -9, max: 4 }, { t: 36, x: -1.4, val: -10, max: 5 },
    ],
    boss: { hp: 1150, speed: 2.2, wake: 33 }, d1: 86, stars: [12, 22],
  },
];
