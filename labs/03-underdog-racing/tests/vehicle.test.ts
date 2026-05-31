import { describe, expect, it } from "vitest";
import { SURFACES, STOCK_COMPACT, createVehicleState, readTelemetry, updateVehicle } from "../src/game/simulation/vehicle";

describe("vehicle physics", () => {
  it("accelerates forward when throttle is applied", () => {
    const start = createVehicleState({ x: 0, y: 0 }, 0);

    const next = updateVehicle(start, { throttle: 1, brake: 0, steer: 0, handbrake: false }, STOCK_COMPACT, SURFACES.asphalt, 0.5);

    expect(next.velocity.x).toBeGreaterThan(0);
    expect(next.position.x).toBeGreaterThan(start.position.x);
  });

  it("braking reduces forward speed", () => {
    const moving = createVehicleState({ x: 0, y: 0 }, 0);
    moving.velocity = { x: 220, y: 0 };

    const next = updateVehicle(moving, { throttle: 0, brake: 1, steer: 0, handbrake: false }, STOCK_COMPACT, SURFACES.asphalt, 0.2);

    expect(next.velocity.x).toBeLessThan(moving.velocity.x);
  });

  it("lateral grip reduces sideways velocity", () => {
    const sliding = createVehicleState({ x: 0, y: 0 }, 0);
    sliding.velocity = { x: 160, y: 120 };

    const next = updateVehicle(sliding, { throttle: 0, brake: 0, steer: 0, handbrake: false }, STOCK_COMPACT, SURFACES.asphalt, 0.1);

    expect(Math.abs(next.velocity.y)).toBeLessThan(Math.abs(sliding.velocity.y));
  });

  it("grass preserves more lateral slide than asphalt", () => {
    const asphaltSlide = createVehicleState({ x: 0, y: 0 }, 0);
    asphaltSlide.velocity = { x: 160, y: 120 };
    const grassSlide = createVehicleState({ x: 0, y: 0 }, 0);
    grassSlide.velocity = { x: 160, y: 120 };

    const asphalt = updateVehicle(asphaltSlide, { throttle: 0, brake: 0, steer: 0, handbrake: false }, STOCK_COMPACT, SURFACES.asphalt, 0.1);
    const grass = updateVehicle(grassSlide, { throttle: 0, brake: 0, steer: 0, handbrake: false }, STOCK_COMPACT, SURFACES.grass, 0.1);

    expect(Math.abs(grass.velocity.y)).toBeGreaterThan(Math.abs(asphalt.velocity.y));
  });

  it("tire wear reduces telemetry grip", () => {
    const fresh = createVehicleState({ x: 0, y: 0 }, 0);
    const worn = createVehicleState({ x: 0, y: 0 }, 0);
    worn.tireWear = 0.7;

    const freshTelemetry = readTelemetry(fresh, STOCK_COMPACT, SURFACES.asphalt);
    const wornTelemetry = readTelemetry(worn, STOCK_COMPACT, SURFACES.asphalt);

    expect(wornTelemetry.grip).toBeLessThan(freshTelemetry.grip);
  });
});
