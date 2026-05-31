import { type SurfaceModel, SURFACES } from "./vehicle";
import type { Vec2 } from "./vector";

export interface Gate {
  id: string;
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface TrackModel {
  width: number;
  height: number;
  spawn: Vec2;
  spawnHeading: number;
  startGate: Gate;
  checkpoints: Gate[];
  centerLine: Vec2[];
  roadWidth: number;
  curbWidth: number;
}

export const TEST_TRACK: TrackModel = {
  width: 1400,
  height: 900,
  spawn: { x: 250, y: 610 },
  spawnHeading: 0,
  startGate: { id: "start", x: 196, y: 540, w: 36, h: 132 },
  checkpoints: [
    { id: "turn-1", x: 535, y: 500, w: 115, h: 115 },
    { id: "esses", x: 770, y: 420, w: 120, h: 115 },
    { id: "hairpin", x: 1065, y: 200, w: 150, h: 115 },
    { id: "back-straight", x: 1125, y: 480, w: 150, h: 100 },
    { id: "stadium", x: 735, y: 705, w: 120, h: 100 },
    { id: "final", x: 310, y: 655, w: 120, h: 100 }
  ],
  centerLine: [
    { x: 214, y: 606 },
    { x: 420, y: 606 },
    { x: 580, y: 545 },
    { x: 690, y: 455 },
    { x: 820, y: 475 },
    { x: 960, y: 395 },
    { x: 1100, y: 230 },
    { x: 1220, y: 255 },
    { x: 1285, y: 365 },
    { x: 1200, y: 515 },
    { x: 1030, y: 550 },
    { x: 900, y: 625 },
    { x: 780, y: 760 },
    { x: 615, y: 750 },
    { x: 505, y: 650 },
    { x: 360, y: 710 },
    { x: 235, y: 680 },
    { x: 214, y: 606 }
  ],
  roadWidth: 70,
  curbWidth: 14
};

export function sampleSurface(track: TrackModel, point: Vec2): SurfaceModel {
  const distance = distanceToCenterLine(track, point);
  const asphaltRadius = track.roadWidth / 2;
  const curbRadius = asphaltRadius + track.curbWidth;

  if (distance <= asphaltRadius) {
    if (distance > asphaltRadius - 8) {
      return SURFACES.curb;
    }
    return SURFACES.asphalt;
  }
  if (distance <= curbRadius) {
    return SURFACES.curb;
  }
  return SURFACES.grass;
}

export function insideGate(point: Vec2, gate: Gate): boolean {
  return point.x >= gate.x && point.x <= gate.x + gate.w && point.y >= gate.y && point.y <= gate.y + gate.h;
}

export function distanceToCenterLine(track: TrackModel, point: Vec2): number {
  let best = Number.POSITIVE_INFINITY;
  for (let index = 0; index < track.centerLine.length - 1; index += 1) {
    best = Math.min(best, distanceToSegment(point, track.centerLine[index], track.centerLine[index + 1]));
  }
  return best;
}

function distanceToSegment(point: Vec2, start: Vec2, end: Vec2): number {
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  const lengthSq = dx * dx + dy * dy;
  if (lengthSq === 0) {
    return Math.hypot(point.x - start.x, point.y - start.y);
  }
  const t = Math.max(0, Math.min(1, ((point.x - start.x) * dx + (point.y - start.y) * dy) / lengthSq));
  const projection = { x: start.x + t * dx, y: start.y + t * dy };
  return Math.hypot(point.x - projection.x, point.y - projection.y);
}
