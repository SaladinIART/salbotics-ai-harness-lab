import { TEST_TRACK, type TrackModel } from "./track";
import { createVehicleState, readTelemetry, STOCK_COMPACT, updateVehicle, type VehicleControls, type VehicleSpec, type VehicleState, type VehicleTelemetry } from "./vehicle";
import { clamp, fromAngle, length, type Vec2 } from "./vector";

export interface RivalState {
  vehicle: VehicleState;
  spec: VehicleSpec;
  nextWaypointIndex: number;
  lapCount: number;
  finished: boolean;
  finishMs: number | null;
  telemetry: VehicleTelemetry;
}

export function createRivalState(track: TrackModel = TEST_TRACK, spec: VehicleSpec = STOCK_COMPACT): RivalState {
  const start = { x: track.spawn.x - 42, y: track.spawn.y + 38 };
  const vehicle = createVehicleState(start, track.spawnHeading);
  return {
    vehicle,
    spec,
    nextWaypointIndex: 0,
    lapCount: 0,
    finished: false,
    finishMs: null,
    telemetry: readTelemetry(vehicle, spec, { type: "asphalt", grip: 1, drag: 1 })
  };
}

export function racingLine(track: TrackModel): Vec2[] {
  return [
    ...track.checkpoints.map((gate) => ({ x: gate.x + gate.w / 2, y: gate.y + gate.h / 2 })),
    { x: track.startGate.x + track.startGate.w / 2, y: track.startGate.y + track.startGate.h / 2 }
  ];
}

export function driveTowardWaypoint(rival: RivalState, target: Vec2): VehicleControls {
  const dx = target.x - rival.vehicle.position.x;
  const dy = target.y - rival.vehicle.position.y;
  const desired = Math.atan2(dy, dx);
  const angleError = normalizeAngle(desired - rival.vehicle.heading);
  const distance = Math.hypot(dx, dy);
  const speed = length(rival.vehicle.velocity);
  const steer = clamp(angleError * 1.8, -1, 1);
  const cornerCaution = Math.abs(angleError) > 0.65 || distance < 95;
  return {
    throttle: cornerCaution && speed > 190 ? 0.35 : 0.86,
    brake: cornerCaution && speed > 240 ? 0.55 : 0,
    steer,
    handbrake: false
  };
}

export function updateRival(rival: RivalState, track: TrackModel, dtMs: number, elapsedMs: number): RivalState {
  if (rival.finished) {
    return rival;
  }
  const points = racingLine(track);
  const target = points[rival.nextWaypointIndex];
  const controls = driveTowardWaypoint(rival, target);
  const surface = { type: "asphalt" as const, grip: 1, drag: 1 };
  const vehicle = updateVehicle(rival.vehicle, controls, rival.spec, surface, dtMs / 1000);
  const distanceToTarget = Math.hypot(vehicle.position.x - target.x, vehicle.position.y - target.y);
  let nextWaypointIndex = rival.nextWaypointIndex;
  let lapCount = rival.lapCount;
  let finished: boolean = rival.finished;
  let finishMs = rival.finishMs;

  if (distanceToTarget < 70) {
    nextWaypointIndex += 1;
    if (nextWaypointIndex >= points.length) {
      nextWaypointIndex = 0;
      lapCount += 1;
      finished = true;
      finishMs = elapsedMs;
    }
  }

  return {
    ...rival,
    vehicle,
    nextWaypointIndex,
    lapCount,
    finished,
    finishMs,
    telemetry: readTelemetry(vehicle, rival.spec, surface)
  };
}

export function normalizeAngle(angle: number): number {
  let result = angle;
  while (result > Math.PI) {
    result -= Math.PI * 2;
  }
  while (result < -Math.PI) {
    result += Math.PI * 2;
  }
  return result;
}

export function rivalSpecForEvent(playerSpec: VehicleSpec, difficulty = 0.92): VehicleSpec {
  return {
    ...playerSpec,
    enginePower: playerSpec.enginePower * difficulty,
    maxSpeed: playerSpec.maxSpeed * (0.94 + difficulty * 0.04),
    tireGrip: playerSpec.tireGrip * (0.9 + difficulty * 0.05),
    brakePower: playerSpec.brakePower * 0.96
  };
}
