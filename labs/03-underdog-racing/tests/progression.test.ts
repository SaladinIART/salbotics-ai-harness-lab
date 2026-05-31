import { describe, expect, it } from "vitest";
import { difficultyById, rivalDifficultySpec } from "../src/game/progression/difficulty";
import { canPurchase, createDefaultProfile, loadProfile, normalizeProfile, purchaseUpgrade, saveProfile } from "../src/game/progression/profile";
import { applyUpgrades, defaultUpgradeLevels, upgradeCost } from "../src/game/progression/upgrades";
import { STOCK_COMPACT } from "../src/game/simulation/vehicle";

class MemoryStorage implements Storage {
  private values = new Map<string, string>();

  get length(): number {
    return this.values.size;
  }

  clear(): void {
    this.values.clear();
  }

  getItem(key: string): string | null {
    return this.values.get(key) ?? null;
  }

  key(index: number): string | null {
    return Array.from(this.values.keys())[index] ?? null;
  }

  removeItem(key: string): void {
    this.values.delete(key);
  }

  setItem(key: string, value: string): void {
    this.values.set(key, value);
  }
}

describe("garage upgrades", () => {
  it("calculates rising upgrade costs and maxes at cap", () => {
    const levels = defaultUpgradeLevels();

    expect(upgradeCost("tires", levels)).toBe(60);

    levels.tires = 5;
    expect(upgradeCost("tires", levels)).toBeNull();
  });

  it("applies upgrade levels to vehicle specs", () => {
    const levels = defaultUpgradeLevels();
    levels.engine = 2;
    levels.tires = 2;
    levels.brakes = 1;

    const spec = applyUpgrades(levels, STOCK_COMPACT);

    expect(spec.enginePower).toBeGreaterThan(STOCK_COMPACT.enginePower);
    expect(spec.maxSpeed).toBeGreaterThan(STOCK_COMPACT.maxSpeed);
    expect(spec.tireGrip).toBeGreaterThan(STOCK_COMPACT.tireGrip);
    expect(spec.brakePower).toBeGreaterThan(STOCK_COMPACT.brakePower);
  });

  it("purchases upgrades only when profile has enough money", () => {
    const profile = createDefaultProfile();

    const purchased = purchaseUpgrade(profile, "tires");

    expect(purchased.money).toBe(profile.money - 60);
    expect(purchased.upgrades.tires).toBe(1);
    expect(canPurchase({ ...profile, money: 0 }, "engine")).toBe(false);
  });

  it("saves and loads campaign profile", () => {
    const storage = new MemoryStorage();
    const profile = purchaseUpgrade(createDefaultProfile(), "engine");
    saveProfile(profile, storage);

    const loaded = loadProfile(storage);

    expect(loaded.upgrades.engine).toBe(1);
    expect(loaded.money).toBe(profile.money);
  });

  it("normalizes and applies race difficulty", () => {
    const easy = normalizeProfile({ difficulty: "easy" });
    const invalid = normalizeProfile({ difficulty: "impossible" } as unknown as Parameters<typeof normalizeProfile>[0]);
    const easyRival = rivalDifficultySpec(STOCK_COMPACT, "easy");
    const hardRival = rivalDifficultySpec(STOCK_COMPACT, "hard");

    expect(easy.difficulty).toBe("easy");
    expect(invalid.difficulty).toBe("normal");
    expect(difficultyById("hard").name).toBe("Hard");
    expect(hardRival.enginePower).toBeGreaterThan(easyRival.enginePower);
  });

});
