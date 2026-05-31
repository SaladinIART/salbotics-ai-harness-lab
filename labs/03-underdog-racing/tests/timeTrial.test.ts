import { describe, expect, it } from "vitest";
import { sampleSurface, TEST_TRACK } from "../src/game/simulation/track";
import { createTimeTrialState, formatLapTime, resetTimeTrial, updateLapProgress, updateTimeTrial } from "../src/game/simulation/timeTrial";

describe("time trial simulation", () => {
  it("updates elapsed time and vehicle telemetry", () => {
    const state = createTimeTrialState();

    const next = updateTimeTrial(state, { throttle: 1, brake: 0, steer: 0, handbrake: false }, 100);

    expect(next.elapsedMs).toBe(100);
    expect(next.telemetry.speed).toBeGreaterThan(0);
  });

  it("advances checkpoint progress in order", () => {
    let state = createTimeTrialState();

    state = { ...state, vehicle: { ...state.vehicle, position: { x: TEST_TRACK.checkpoints[0].x + 10, y: TEST_TRACK.checkpoints[0].y + 10 } } };
    state = updateLapProgress(state);

    expect(state.nextCheckpointIndex).toBe(1);
    expect(state.message).toContain("TURN-1");
  });

  it("completes a lap after all checkpoints and start gate", () => {
    let state = createTimeTrialState();
    state = { ...state, elapsedMs: 65_432, nextCheckpointIndex: TEST_TRACK.checkpoints.length };
    state = { ...state, vehicle: { ...state.vehicle, position: { x: TEST_TRACK.startGate.x + 2, y: TEST_TRACK.startGate.y + 2 } } };

    state = updateLapProgress(state);

    expect(state.lapCount).toBe(1);
    expect(state.bestLapMs).toBe(65_432);
    expect(state.nextCheckpointIndex).toBe(0);
  });

  it("reset returns the car to spawn and clears time", () => {
    const state = updateTimeTrial(createTimeTrialState(), { throttle: 1, brake: 0, steer: 0, handbrake: false }, 500);

    const reset = resetTimeTrial(state);

    expect(reset.elapsedMs).toBe(0);
    expect(reset.vehicle.position).toEqual(TEST_TRACK.spawn);
  });

  it("samples asphalt on the F1-style racing line and grass off track", () => {
    expect(sampleSurface(TEST_TRACK, TEST_TRACK.spawn).type).toBe("asphalt");
    expect(sampleSurface(TEST_TRACK, { x: 40, y: 40 }).type).toBe("grass");
  });

  it("formats lap time for HUD display", () => {
    expect(formatLapTime(null)).toBe("--:--.---");
    expect(formatLapTime(65_432)).toBe("1:05.432");
  });
});
