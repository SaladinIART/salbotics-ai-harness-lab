import { buildRating } from "./upgrades";
import type { CampaignProfile } from "./profile";
import { championshipById, recordChampionshipResult } from "./championship";

export const CAMPAIGN_EVENTS = [
  {
    id: "backlot-shakedown",
    name: "Backlot Shakedown",
    tier: "Street",
    description: "Local test loop. Low stakes, steady cash.",
    requiredReputation: 0,
    requiredLicense: "street",
    targetLapMs: 95_000,
    baseMoney: 45,
    reputationReward: 1,
    driverXpReward: 8
  },
  {
    id: "dockside-sprint",
    name: "Dockside Sprint",
    tier: "Street",
    description: "Faster crowd, rougher surface, better payout.",
    requiredReputation: 4,
    requiredLicense: "street",
    targetLapMs: 82_000,
    baseMoney: 75,
    reputationReward: 2,
    driverXpReward: 14
  },
  {
    id: "club-license-trial",
    name: "Club License Trial",
    tier: "License",
    description: "Clean time trial that proves you belong on legal grids.",
    requiredReputation: 8,
    requiredLicense: "street",
    targetLapMs: 76_000,
    baseMoney: 95,
    reputationReward: 3,
    driverXpReward: 20,
    grantsLicense: "club"
  },
  {
    id: "club-rookie-cup",
    name: "Club Rookie Cup",
    tier: "Club",
    description: "First sanctioned event. Build quality starts to matter.",
    requiredReputation: 12,
    requiredLicense: "club",
    targetLapMs: 70_000,
    baseMoney: 130,
    reputationReward: 4,
    driverXpReward: 28
  }
] as const;

export type CampaignEventId = (typeof CAMPAIGN_EVENTS)[number]["id"];
export type LicenseTier = "street" | "club";

export interface CampaignEvent {
  id: CampaignEventId;
  name: string;
  tier: string;
  description: string;
  requiredReputation: number;
  requiredLicense: LicenseTier;
  targetLapMs: number;
  baseMoney: number;
  reputationReward: number;
  driverXpReward: number;
  grantsLicense?: LicenseTier;
}

export interface EventResult {
  event: CampaignEvent;
  lapMs: number;
  won: boolean;
  money: number;
  reputation: number;
  driverXp: number;
  licenseGranted?: LicenseTier;
  championshipPoints?: number;
  championshipComplete?: boolean;
  championshipWon?: boolean;
}

export function eventById(id: CampaignEventId): CampaignEvent {
  return CAMPAIGN_EVENTS.find((event) => event.id === id) ?? CAMPAIGN_EVENTS[0];
}

export function isEventUnlocked(profile: CampaignProfile, event: CampaignEvent): boolean {
  return profile.reputation >= event.requiredReputation && licenseRank(profile.license) >= licenseRank(event.requiredLicense);
}

export function nextUnlockedEvent(profile: CampaignProfile, selectedId: CampaignEventId): CampaignEvent {
  const currentIndex = CAMPAIGN_EVENTS.findIndex((event) => event.id === selectedId);
  for (let offset = 0; offset < CAMPAIGN_EVENTS.length; offset += 1) {
    const event = CAMPAIGN_EVENTS[(currentIndex + offset + 1) % CAMPAIGN_EVENTS.length];
    if (isEventUnlocked(profile, event)) {
      return event;
    }
  }
  return CAMPAIGN_EVENTS[0];
}

export function previousUnlockedEvent(profile: CampaignProfile, selectedId: CampaignEventId): CampaignEvent {
  const currentIndex = CAMPAIGN_EVENTS.findIndex((event) => event.id === selectedId);
  for (let offset = 0; offset < CAMPAIGN_EVENTS.length; offset += 1) {
    const index = (currentIndex - offset - 1 + CAMPAIGN_EVENTS.length) % CAMPAIGN_EVENTS.length;
    const event = CAMPAIGN_EVENTS[index];
    if (isEventUnlocked(profile, event)) {
      return event;
    }
  }
  return CAMPAIGN_EVENTS[0];
}

export function completeEvent(profile: CampaignProfile, event: CampaignEvent, lapMs: number): { profile: CampaignProfile; result: EventResult } {
  const won = lapMs <= event.targetLapMs;
  const buildBonus = Math.floor(buildRating(profile.upgrades) * 2);
  const timeBonus = won ? Math.floor(Math.max(0, event.targetLapMs - lapMs) / 1_000) : 0;
  const money = Math.max(15, event.baseMoney + buildBonus + timeBonus - (won ? 0 : 20));
  const reputation = won ? event.reputationReward : 1;
  const driverXp = event.driverXpReward + (won ? 8 : 2);
  const licenseGranted = won ? event.grantsLicense : undefined;

  const nextProfile: CampaignProfile = {
    ...profile,
    money: profile.money + money,
    reputation: profile.reputation + reputation,
    driverXp: profile.driverXp + driverXp,
    bestLapMs: profile.bestLapMs === null ? lapMs : Math.min(profile.bestLapMs, lapMs),
    totalLaps: profile.totalLaps + 1,
    license: licenseGranted ?? profile.license,
    completedEvents: Array.from(new Set([...profile.completedEvents, ...(won ? [event.id] : [])]))
  };

  return {
    profile: nextProfile,
    result: {
      event,
      lapMs,
      won,
      money,
      reputation,
      driverXp,
      licenseGranted
    }
  };
}

export function completeDuelEvent(
  profile: CampaignProfile,
  event: CampaignEvent,
  lapMs: number,
  finishOrder: "player" | "rival"
): { profile: CampaignProfile; result: EventResult } {
  const base = completeEvent(profile, event, lapMs);
  const championship = championshipById(base.profile.championship.activeId);
  const championshipUpdate = recordChampionshipResult(base.profile.championship, event.id, finishOrder);
  const championBonus = championshipUpdate.justCompleted && championshipUpdate.playerChampion ? championship.championBonus : null;
  if (finishOrder === "player") {
    const boostedProfile: CampaignProfile = {
      ...base.profile,
      money: base.profile.money + 40 + (championBonus?.money ?? 0),
      reputation: base.profile.reputation + 2 + (championBonus?.reputation ?? 0),
      driverXp: base.profile.driverXp + 10 + (championBonus?.driverXp ?? 0),
      championship: championshipUpdate.progress,
      sponsorId: championBonus ? "local-parts-shop" : base.profile.sponsorId,
      teamFacilities: championBonus
        ? { ...base.profile.teamFacilities, "crew-notebook": Math.max(base.profile.teamFacilities["crew-notebook"], 1) }
        : base.profile.teamFacilities
    };
    return {
      profile: boostedProfile,
      result: {
        ...base.result,
        won: true,
        money: base.result.money + 40 + (championBonus?.money ?? 0),
        reputation: base.result.reputation + 2 + (championBonus?.reputation ?? 0),
        driverXp: base.result.driverXp + 10 + (championBonus?.driverXp ?? 0),
        championshipPoints: championshipUpdate.recorded ? championship.points.winner : undefined,
        championshipComplete: championshipUpdate.justCompleted,
        championshipWon: championshipUpdate.playerChampion
      }
    };
  }
  return {
    profile: {
      ...base.profile,
      money: base.profile.money + (championBonus?.money ?? 0),
      reputation: base.profile.reputation + 1 + (championBonus?.reputation ?? 0),
      driverXp: base.profile.driverXp + 4 + (championBonus?.driverXp ?? 0),
      championship: championshipUpdate.progress,
      sponsorId: championBonus ? "local-parts-shop" : base.profile.sponsorId,
      teamFacilities: championBonus
        ? { ...base.profile.teamFacilities, "crew-notebook": Math.max(base.profile.teamFacilities["crew-notebook"], 1) }
        : base.profile.teamFacilities
    },
    result: {
      ...base.result,
      won: false,
      money: base.result.money + (championBonus?.money ?? 0),
      reputation: base.result.reputation + 1 + (championBonus?.reputation ?? 0),
      driverXp: base.result.driverXp + 4 + (championBonus?.driverXp ?? 0),
      championshipPoints: championshipUpdate.recorded ? championship.points.runnerUp : undefined,
      championshipComplete: championshipUpdate.justCompleted,
      championshipWon: championshipUpdate.playerChampion
    }
  };
}

function licenseRank(license: LicenseTier): number {
  return license === "club" ? 1 : 0;
}
