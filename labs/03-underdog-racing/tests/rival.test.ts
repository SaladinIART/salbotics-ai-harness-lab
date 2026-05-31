import { describe, expect, it } from "vitest";
import { completeDuelEvent, eventById } from "../src/game/progression/campaign";
import { createDefaultProfile } from "../src/game/progression/profile";
import { createDuelRaceState, resolveFinishOrder, updateDuelRace } from "../src/game/simulation/race";
import { createRivalState, driveTowardWaypoint, racingLine, updateRival } from "../src/game/simulation/rival";
import { TEST_TRACK } from "../src/game/simulation/track";

describe("rival AI", () => {
  it("builds a racing line from track checkpoints and start gate", () => {
    const line = racingLine(TEST_TRACK);

    expect(line.length).toBe(TEST_TRACK.checkpoints.length + 1);
    expect(line[0].x).toBeGreaterThan(0);
  });

  it("steers toward the next waypoint", () => {
    const rival = createRivalState(TEST_TRACK);
    const target = racingLine(TEST_TRACK)[0];

    const controls = driveTowardWaypoint(rival, target);

    expect(controls.throttle).toBeGreaterThan(0);
    expect(Math.abs(controls.steer)).toBeLessThanOrEqual(1);
  });

  it("advances waypoint progress when close to target", () => {
    const line = racingLine(TEST_TRACK);
    const rival = createRivalState(TEST_TRACK);
    rival.vehicle.position = { ...line[0] };

    const next = updateRival(rival, TEST_TRACK, 16, 16);

    expect(next.nextWaypointIndex).toBe(1);
  });

  it("resolves finish order from finish times", () => {
    expect(resolveFinishOrder(true, 70_000, true, 72_000)).toBe("player");
    expect(resolveFinishOrder(true, 74_000, true, 72_000)).toBe("rival");
    expect(resolveFinishOrder(false, null, false, null)).toBeNull();
  });

  it("updates duel race with rival telemetry", () => {
    const state = createDuelRaceState();

    const next = updateDuelRace(state, { throttle: 1, brake: 0, steer: 0, handbrake: false }, 100);

    expect(next.elapsedMs).toBe(100);
    expect(next.rival.telemetry.speed).toBeGreaterThanOrEqual(0);
  });

  it("creates tougher rival specs on hard difficulty", () => {
    const easy = createDuelRaceState(TEST_TRACK, undefined, "easy");
    const hard = createDuelRaceState(TEST_TRACK, undefined, "hard");

    expect(hard.rival.spec.enginePower).toBeGreaterThan(easy.rival.spec.enginePower);
    expect(hard.rival.spec.maxSpeed).toBeGreaterThan(easy.rival.spec.maxSpeed);
  });

  it("duel event win grants bonus rewards", () => {
    const profile = createDefaultProfile();
    const event = eventById("backlot-shakedown");

    const result = completeDuelEvent(profile, event, 80_000, "player");

    expect(result.profile.money).toBeGreaterThan(profile.money + event.baseMoney);
    expect(result.profile.reputation).toBeGreaterThan(profile.reputation + event.reputationReward);
  });

  it("duel event loss still grants participation progress", () => {
    const profile = createDefaultProfile();
    const event = eventById("backlot-shakedown");

    const result = completeDuelEvent(profile, event, 90_000, "rival");

    expect(result.result.won).toBe(false);
    expect(result.profile.money).toBeGreaterThan(profile.money);
    expect(result.profile.reputation).toBeGreaterThan(profile.reputation);
  });
});
