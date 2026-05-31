import { add, clamp, dot, fromAngle, length, rightFromAngle, scale, type Vec2 } from "./vector";

export interface VehicleSpec {
  enginePower: number;
  brakePower: number;
  maxSpeed: number;
  reverseMaxSpeed: number;
  steeringRate: number;
  tireGrip: number;
  drag: number;
  rollingResistance: number;
  tireWearRate: number;
}

export interface VehicleState {
  position: Vec2;
  velocity: Vec2;
  heading: number;
  tireWear: number;
  currentSurface: SurfaceType;
}

export interface VehicleControls {
  throttle: number;
  brake: number;
  steer: number;
  handbrake: boolean;
}

export type SurfaceType = "asphalt" | "curb" | "grass";

export interface SurfaceModel {
  type: SurfaceType;
  grip: number;
  drag: number;
}

export interface VehicleTelemetry {
  speed: number;
  forwardSpeed: number;
  lateralSpeed: number;
  grip: number;
  tireWear: number;
  surface: SurfaceType;
}

export const STOCK_COMPACT: VehicleSpec = {
  enginePower: 420,
  brakePower: 620,
  maxSpeed: 520,
  reverseMaxSpeed: 90,
  steeringRate: 2.8,
  tireGrip: 7.5,
  drag: 0.18,
  rollingResistance: 0.7,
  tireWearRate: 0.0015
};

export const SURFACES: Record<SurfaceType, SurfaceModel> = {
  asphalt: { type: "asphalt", grip: 1, drag: 1 },
  curb: { type: "curb", grip: 0.72, drag: 1.16 },
  grass: { type: "grass", grip: 0.35, drag: 2.35 }
};

export function createVehicleState(position: Vec2, heading = 0): VehicleState {
  return {
    position,
    velocity: { x: 0, y: 0 },
    heading,
    tireWear: 0,
    currentSurface: "asphalt"
  };
}

export function updateVehicle(
  state: VehicleState,
  controls: VehicleControls,
  spec: VehicleSpec,
  surface: SurfaceModel,
  dt: number
): VehicleState {
  const safeDt = clamp(dt, 0, 0.05);
  const forward = fromAngle(state.heading);
  const right = rightFromAngle(state.heading);
  const forwardSpeed = dot(state.velocity, forward);
  const lateralSpeed = dot(state.velocity, right);
  const speed = length(state.velocity);
  const wearGrip = 1 - state.tireWear * 0.48;
  const handbrakeGrip = controls.handbrake ? 0.42 : 1;
  const grip = Math.max(0.15, spec.tireGrip * surface.grip * wearGrip * handbrakeGrip);

  const throttleForce = controls.throttle > 0 && forwardSpeed < spec.maxSpeed ? spec.enginePower * controls.throttle : 0;
  const brakeForce = controls.brake > 0 ? spec.brakePower * controls.brake * Math.sign(forwardSpeed || 1) : 0;
  let velocity = add(state.velocity, scale(forward, (throttleForce - brakeForce) * safeDt));

  const newForwardSpeed = dot(velocity, forward);
  if (newForwardSpeed > spec.maxSpeed) {
    velocity = add(scale(right, dot(velocity, right)), scale(forward, spec.maxSpeed));
  } else if (newForwardSpeed < -spec.reverseMaxSpeed) {
    velocity = add(scale(right, dot(velocity, right)), scale(forward, -spec.reverseMaxSpeed));
  }

  const postLateralSpeed = dot(velocity, right);
  const lateralReduction = clamp(grip * safeDt, 0, 1);
  velocity = add(velocity, scale(right, -postLateralSpeed * lateralReduction));

  const dragAmount = (spec.drag * (speed / spec.maxSpeed) + spec.rollingResistance * surface.drag * 0.02) * safeDt;
  velocity = scale(velocity, Math.max(0, 1 - dragAmount));

  const speedFactor = clamp(Math.abs(forwardSpeed) / 180, 0.18, 1);
  const steerEffect = controls.steer * spec.steeringRate * speedFactor * safeDt * Math.sign(forwardSpeed || 1);
  const heading = state.heading + steerEffect;
  const tireWear = clamp(
    state.tireWear + (Math.abs(lateralSpeed) * 0.35 + controls.brake * 35 + Math.abs(controls.steer) * speed * 0.08) * spec.tireWearRate * safeDt,
    0,
    1
  );

  return {
    position: add(state.position, scale(velocity, safeDt)),
    velocity,
    heading,
    tireWear,
    currentSurface: surface.type
  };
}

export function readTelemetry(state: VehicleState, spec: VehicleSpec, surface: SurfaceModel): VehicleTelemetry {
  const forward = fromAngle(state.heading);
  const right = rightFromAngle(state.heading);
  const wearGrip = 1 - state.tireWear * 0.48;
  return {
    speed: length(state.velocity),
    forwardSpeed: dot(state.velocity, forward),
    lateralSpeed: dot(state.velocity, right),
    grip: Math.max(0.15, spec.tireGrip * surface.grip * wearGrip),
    tireWear: state.tireWear,
    surface: surface.type
  };
}
