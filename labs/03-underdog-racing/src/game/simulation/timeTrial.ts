import { insideGate, sampleSurface, TEST_TRACK, type TrackModel } from "./track";
import {
  createVehicleState,
  readTelemetry,
  STOCK_COMPACT,
  updateVehicle,
  type VehicleControls,
  type VehicleSpec,
  type VehicleState,
  type VehicleTelemetry
} from "./vehicle";

export interface TimeTrialState {
  vehicle: VehicleState;
  track: TrackModel;
  spec: VehicleSpec;
  elapsedMs: number;
  lapStartMs: number;
  bestLapMs: number | null;
  lapCount: number;
  nextCheckpointIndex: number;
  message: string;
  telemetry: VehicleTelemetry;
}

export function createTimeTrialState(track: TrackModel = TEST_TRACK, spec: VehicleSpec = STOCK_COMPACT): TimeTrialState {
  const vehicle = createVehicleState(track.spawn, track.spawnHeading);
  const surface = sampleSurface(track, vehicle.position);
  return {
    vehicle,
    track,
    spec,
    elapsedMs: 0,
    lapStartMs: 0,
    bestLapMs: null,
    lapCount: 0,
    nextCheckpointIndex: 0,
    message: "Find grip. Learn the line.",
    telemetry: readTelemetry(vehicle, spec, surface)
  };
}

export function resetTimeTrial(state: TimeTrialState): TimeTrialState {
  return createTimeTrialState(state.track, state.spec);
}

export function updateTimeTrial(state: TimeTrialState, controls: VehicleControls, dtMs: number): TimeTrialState {
  const dt = dtMs / 1000;
  const surface = sampleSurface(state.track, state.vehicle.position);
  const vehicle = updateVehicle(state.vehicle, controls, state.spec, surface, dt);
  const elapsedMs = state.elapsedMs + dtMs;
  const next = { ...state, vehicle, elapsedMs, telemetry: readTelemetry(vehicle, state.spec, surface) };
  return updateLapProgress(next);
}

export function updateLapProgress(state: TimeTrialState): TimeTrialState {
  if (state.nextCheckpointIndex < state.track.checkpoints.length) {
    const gate = state.track.checkpoints[state.nextCheckpointIndex];
    if (insideGate(state.vehicle.position, gate)) {
      return {
        ...state,
        nextCheckpointIndex: state.nextCheckpointIndex + 1,
        message: `Checkpoint ${gate.id.toUpperCase()}`
      };
    }
    return state;
  }

  if (insideGate(state.vehicle.position, state.track.startGate)) {
    const lapMs = Math.max(1, state.elapsedMs - state.lapStartMs);
    return {
      ...state,
      lapStartMs: state.elapsedMs,
      bestLapMs: state.bestLapMs === null ? lapMs : Math.min(state.bestLapMs, lapMs),
      lapCount: state.lapCount + 1,
      nextCheckpointIndex: 0,
      message: `Lap ${state.lapCount + 1} complete`
    };
  }

  return state;
}

export function formatLapTime(ms: number | null): string {
  if (ms === null) {
    return "--:--.---";
  }
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const millis = Math.floor(ms % 1000);
  return `${minutes}:${seconds.toString().padStart(2, "0")}.${millis.toString().padStart(3, "0")}`;
}
