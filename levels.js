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
    name: 'STAGE 2',
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
    name: 'STAGE 3',
    gates: [
      { t: 1.5, every: 0.35, count: 18, val: 1 },
      { t: 7.9, op: '-', val: 6 },
      { t: 8.3, every: 0.35, count: 14, val: 1 },
      { t: 13.4, op: 'x', val: 2 },
      { t: 13.8, every: 0.35, count: 10, val: 1 },
      { t: 17.4, op: '-', val: 12 },
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
];
