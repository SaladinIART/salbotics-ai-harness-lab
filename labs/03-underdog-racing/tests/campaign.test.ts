import { describe, expect, it } from "vitest";
import { completeEvent, eventById, isEventUnlocked, nextUnlockedEvent } from "../src/game/progression/campaign";
import { driverBrakeBonus, driverGripBonus, unlockedDriverSkills } from "../src/game/progression/driverSkills";
import { createDefaultProfile, normalizeProfile } from "../src/game/progression/profile";

describe("street-to-pro campaign shell", () => {
  it("locks events behind reputation and license gates", () => {
    const profile = createDefaultProfile();

    expect(isEventUnlocked(profile, eventById("backlot-shakedown"))).toBe(true);
    expect(isEventUnlocked(profile, eventById("dockside-sprint"))).toBe(false);
    expect(isEventUnlocked(profile, eventById("club-rookie-cup"))).toBe(false);
  });

  it("cycles only to unlocked events", () => {
    const profile = { ...createDefaultProfile(), reputation: 5 };

    const next = nextUnlockedEvent(profile, "backlot-shakedown");

    expect(next.id).toBe("dockside-sprint");
  });

  it("completing license trial grants club license", () => {
    const profile = { ...createDefaultProfile(), reputation: 9 };
    const event = eventById("club-license-trial");

    const result = completeEvent(profile, event, 74_000);

    expect(result.result.won).toBe(true);
    expect(result.profile.license).toBe("club");
    expect(result.profile.completedEvents).toContain("club-license-trial");
  });

  it("driver XP unlocks passive bonuses", () => {
    const profile = { ...createDefaultProfile(), driverXp: 75 };

    expect(unlockedDriverSkills(profile)).toContain("smooth_inputs");
    expect(unlockedDriverSkills(profile)).toContain("brake_discipline");
    expect(driverGripBonus(profile)).toBeGreaterThan(0);
    expect(driverBrakeBonus(profile)).toBeGreaterThan(0);
  });

  it("normalizes old CP4 saves with campaign defaults", () => {
    const oldSave = normalizeProfile({
      money: 200,
      reputation: 3,
      upgrades: { tires: 1 }
    } as Parameters<typeof normalizeProfile>[0]);

    expect(oldSave.license).toBe("street");
    expect(oldSave.driverXp).toBe(0);
    expect(oldSave.selectedEventId).toBe("backlot-shakedown");
  });
});
