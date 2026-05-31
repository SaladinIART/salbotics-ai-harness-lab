import type { VehicleSpec } from "../simulation/vehicle";

export type DifficultyId = "easy" | "normal" | "hard";

export interface DifficultyDef {
  id: DifficultyId;
  name: string;
  description: string;
  rivalMultiplier: number;
}

export const DIFFICULTIES: DifficultyDef[] = [
  {
    id: "easy",
    name: "Easy",
    description: "Rival leaves room for learning braking points.",
    rivalMultiplier: 0.82
  },
  {
    id: "normal",
    name: "Normal",
    description: "Balanced duel pressure for campaign runs.",
    rivalMultiplier: 0.92
  },
  {
    id: "hard",
    name: "Hard",
    description: "Rival punishes messy exits and grass mistakes.",
    rivalMultiplier: 1.04
  }
];

export function normalizeDifficulty(raw: unknown): DifficultyId {
  return raw === "easy" || raw === "hard" ? raw : "normal";
}

export function difficultyById(id: DifficultyId): DifficultyDef {
  return DIFFICULTIES.find((difficulty) => difficulty.id === id) ?? DIFFICULTIES[1];
}

export function nextDifficulty(id: DifficultyId): DifficultyId {
  const index = DIFFICULTIES.findIndex((difficulty) => difficulty.id === id);
  return DIFFICULTIES[(index + 1) % DIFFICULTIES.length].id;
}

export function previousDifficulty(id: DifficultyId): DifficultyId {
  const index = DIFFICULTIES.findIndex((difficulty) => difficulty.id === id);
  return DIFFICULTIES[(index - 1 + DIFFICULTIES.length) % DIFFICULTIES.length].id;
}

export function rivalDifficultySpec(playerSpec: VehicleSpec, difficulty: DifficultyId): VehicleSpec {
  const multiplier = difficultyById(difficulty).rivalMultiplier;
  return {
    ...playerSpec,
    enginePower: playerSpec.enginePower * multiplier,
    maxSpeed: playerSpec.maxSpeed * (0.94 + multiplier * 0.04),
    tireGrip: playerSpec.tireGrip * (0.9 + multiplier * 0.05),
    brakePower: playerSpec.brakePower * (0.92 + multiplier * 0.04)
  };
}
