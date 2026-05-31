import { describe, expect, it } from "vitest";
import { completeDuelEvent, eventById } from "../src/game/progression/campaign";
import {
  championshipStandings,
  currentChampionshipRound,
  recordChampionshipResult
} from "../src/game/progression/championship";
import { createDefaultProfile, normalizeProfile } from "../src/game/progression/profile";

describe("championship loop", () => {
  it("records the current calendar round and points table", () => {
    const profile = createDefaultProfile();

    const recorded = recordChampionshipResult(profile.championship, "backlot-shakedown", "player");

    expect(recorded.recorded).toBe(true);
    expect(championshipStandings(recorded.progress)).toEqual({ player: 10, rival: 6 });
    expect(currentChampionshipRound(recorded.progress)?.eventId).toBe("dockside-sprint");
  });

  it("ignores events outside the current championship round", () => {
    const profile = createDefaultProfile();

    const recorded = recordChampionshipResult(profile.championship, "dockside-sprint", "player");

    expect(recorded.recorded).toBe(false);
    expect(recorded.progress.roundResults).toHaveLength(0);
  });

  it("awards campaign advancement hooks when the player wins the cup", () => {
    let profile = { ...createDefaultProfile(), reputation: 20 };

    profile = completeDuelEvent(profile, eventById("backlot-shakedown"), 80_000, "player").profile;
    profile = completeDuelEvent(profile, eventById("dockside-sprint"), 75_000, "player").profile;
    const completed = completeDuelEvent(profile, eventById("club-license-trial"), 72_000, "player");

    expect(completed.result.championshipComplete).toBe(true);
    expect(completed.result.championshipWon).toBe(true);
    expect(completed.profile.championship.completedIds).toContain("street-underdog-cup");
    expect(completed.profile.sponsorId).toBe("local-parts-shop");
    expect(completed.profile.teamFacilities["crew-notebook"]).toBe(1);
  });

  it("normalizes old saves with championship and team defaults", () => {
    const profile = normalizeProfile({
      money: 300,
      reputation: 4
    });

    expect(profile.championship.activeId).toBe("street-underdog-cup");
    expect(profile.sponsorId).toBeNull();
    expect(profile.teamFacilities["home-garage"]).toBe(1);
  });
});
