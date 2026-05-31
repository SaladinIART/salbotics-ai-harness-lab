import { STOCK_COMPACT, type VehicleSpec } from "../simulation/vehicle";
import { driverBrakeBonus, driverGripBonus } from "./driverSkills";
import type { CampaignProfile } from "./profile";

export const UPGRADE_CATEGORIES = ["tires", "engine", "brakes", "gearbox", "aero", "weight"] as const;

export type UpgradeCategory = (typeof UPGRADE_CATEGORIES)[number];

export type UpgradeLevels = Record<UpgradeCategory, number>;

export interface UpgradeDef {
  id: UpgradeCategory;
  name: string;
  description: string;
  maxLevel: number;
  baseCost: number;
}

export const UPGRADE_DEFS: Record<UpgradeCategory, UpgradeDef> = {
  tires: {
    id: "tires",
    name: "Tires",
    description: "Grip, slide recovery, tire wear",
    maxLevel: 5,
    baseCost: 60
  },
  engine: {
    id: "engine",
    name: "Engine",
    description: "Acceleration and top speed",
    maxLevel: 5,
    baseCost: 75
  },
  brakes: {
    id: "brakes",
    name: "Brakes",
    description: "Shorter braking zones",
    maxLevel: 5,
    baseCost: 55
  },
  gearbox: {
    id: "gearbox",
    name: "Gearbox",
    description: "Launch and speed balance",
    maxLevel: 5,
    baseCost: 65
  },
  aero: {
    id: "aero",
    name: "Aero",
    description: "Fast-corner stability",
    maxLevel: 5,
    baseCost: 70
  },
  weight: {
    id: "weight",
    name: "Weight",
    description: "Lighter shell, sharper response",
    maxLevel: 5,
    baseCost: 80
  }
};

export function defaultUpgradeLevels(): UpgradeLevels {
  return {
    tires: 0,
    engine: 0,
    brakes: 0,
    gearbox: 0,
    aero: 0,
    weight: 0
  };
}

export function upgradeCost(category: UpgradeCategory, levels: UpgradeLevels): number | null {
  const def = UPGRADE_DEFS[category];
  const level = levels[category];
  if (level >= def.maxLevel) {
    return null;
  }
  return Math.round(def.baseCost * (level + 1) ** 1.35);
}

export function applyUpgrades(levels: UpgradeLevels, base: VehicleSpec = STOCK_COMPACT): VehicleSpec {
  const tires = levels.tires;
  const engine = levels.engine;
  const brakes = levels.brakes;
  const gearbox = levels.gearbox;
  const aero = levels.aero;
  const weight = levels.weight;

  return {
    enginePower: base.enginePower * (1 + engine * 0.09 + gearbox * 0.025 + weight * 0.025),
    brakePower: base.brakePower * (1 + brakes * 0.11 + weight * 0.02),
    maxSpeed: base.maxSpeed * (1 + engine * 0.035 + gearbox * 0.05 - aero * 0.01),
    reverseMaxSpeed: base.reverseMaxSpeed,
    steeringRate: base.steeringRate * (1 + tires * 0.025 + weight * 0.035),
    tireGrip: base.tireGrip * (1 + tires * 0.09 + aero * 0.045),
    drag: Math.max(0.08, base.drag * (1 - aero * 0.055 - weight * 0.02)),
    rollingResistance: Math.max(0.45, base.rollingResistance * (1 - weight * 0.035)),
    tireWearRate: base.tireWearRate * Math.max(0.55, 1 - tires * 0.055 + weight * 0.018)
  };
}

export function specFromProfile(profile: CampaignProfile, base: VehicleSpec = STOCK_COMPACT): VehicleSpec {
  const spec = applyUpgrades(profile.upgrades, base);
  const gripBonus = driverGripBonus(profile);
  const brakeBonus = driverBrakeBonus(profile);
  return {
    ...spec,
    tireGrip: spec.tireGrip * (1 + gripBonus),
    brakePower: spec.brakePower * (1 + brakeBonus)
  };
}

export function buildRating(levels: UpgradeLevels): number {
  return UPGRADE_CATEGORIES.reduce((total, category) => total + levels[category], 0);
}
