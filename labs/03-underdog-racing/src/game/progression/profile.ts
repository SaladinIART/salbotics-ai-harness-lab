import { defaultUpgradeLevels, upgradeCost, type UpgradeCategory, type UpgradeLevels } from "./upgrades";
import type { CampaignEventId, LicenseTier } from "./campaign";
import {
  createDefaultChampionshipProgress,
  normalizeChampionshipProgress,
  type ChampionshipProgress,
  type SponsorId,
  type TeamFacilityId
} from "./championship";
import { normalizeDifficulty, type DifficultyId } from "./difficulty";

export interface CampaignProfile {
  version: number;
  money: number;
  reputation: number;
  bestLapMs: number | null;
  totalLaps: number;
  upgrades: UpgradeLevels;
  license: LicenseTier;
  driverXp: number;
  selectedEventId: CampaignEventId;
  completedEvents: CampaignEventId[];
  championship: ChampionshipProgress;
  sponsorId: SponsorId | null;
  teamFacilities: Record<TeamFacilityId, number>;
  difficulty: DifficultyId;
}

export const PROFILE_STORAGE_KEY = "underdog-racing-profile-v1";

export function createDefaultProfile(): CampaignProfile {
  return {
    version: 1,
    money: 140,
    reputation: 0,
    bestLapMs: null,
    totalLaps: 0,
    upgrades: defaultUpgradeLevels(),
    license: "street",
    driverXp: 0,
    selectedEventId: "backlot-shakedown",
    completedEvents: [],
    championship: createDefaultChampionshipProgress(),
    sponsorId: null,
    teamFacilities: {
      "home-garage": 1,
      "used-tire-rack": 0,
      "crew-notebook": 0
    },
    difficulty: "normal"
  };
}

export function normalizeProfile(raw: Partial<CampaignProfile> | null | undefined): CampaignProfile {
  const defaults = createDefaultProfile();
  return {
    version: 1,
    money: Math.max(0, Math.floor(raw?.money ?? defaults.money)),
    reputation: Math.max(0, Math.floor(raw?.reputation ?? defaults.reputation)),
    bestLapMs: typeof raw?.bestLapMs === "number" ? raw.bestLapMs : null,
    totalLaps: Math.max(0, Math.floor(raw?.totalLaps ?? defaults.totalLaps)),
    upgrades: { ...defaults.upgrades, ...(raw?.upgrades ?? {}) },
    license: raw?.license === "club" ? "club" : "street",
    driverXp: Math.max(0, Math.floor(raw?.driverXp ?? defaults.driverXp)),
    selectedEventId: raw?.selectedEventId ?? defaults.selectedEventId,
    completedEvents: Array.isArray(raw?.completedEvents) ? raw.completedEvents : defaults.completedEvents,
    championship: normalizeChampionshipProgress(raw?.championship),
    sponsorId: raw?.sponsorId === "local-parts-shop" || raw?.sponsorId === "night-market-energy" ? raw.sponsorId : null,
    teamFacilities: {
      ...defaults.teamFacilities,
      ...(raw?.teamFacilities ?? {})
    },
    difficulty: normalizeDifficulty(raw?.difficulty)
  };
}

export function loadProfile(storage: Storage | undefined = globalThis.localStorage): CampaignProfile {
  if (!storage) {
    return createDefaultProfile();
  }
  const saved = storage.getItem(PROFILE_STORAGE_KEY);
  if (!saved) {
    const profile = createDefaultProfile();
    saveProfile(profile, storage);
    return profile;
  }
  try {
    return normalizeProfile(JSON.parse(saved) as Partial<CampaignProfile>);
  } catch {
    const profile = createDefaultProfile();
    saveProfile(profile, storage);
    return profile;
  }
}

export function saveProfile(profile: CampaignProfile, storage: Storage | undefined = globalThis.localStorage): void {
  if (!storage) {
    return;
  }
  storage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(normalizeProfile(profile)));
}

export function canPurchase(profile: CampaignProfile, category: UpgradeCategory): boolean {
  const cost = upgradeCost(category, profile.upgrades);
  return cost !== null && profile.money >= cost;
}

export function purchaseUpgrade(profile: CampaignProfile, category: UpgradeCategory): CampaignProfile {
  const cost = upgradeCost(category, profile.upgrades);
  if (cost === null || profile.money < cost) {
    return profile;
  }
  return normalizeProfile({
    ...profile,
    money: profile.money - cost,
    upgrades: {
      ...profile.upgrades,
      [category]: profile.upgrades[category] + 1
    }
  });
}

export function awardTimeTrialLap(profile: CampaignProfile, lapMs: number): CampaignProfile {
  const cleanLapBonus = Math.max(0, 90_000 - lapMs);
  const money = 35 + Math.floor(cleanLapBonus / 1_000);
  const reputation = lapMs < 75_000 ? 2 : 1;
  const bestLapMs = profile.bestLapMs === null ? lapMs : Math.min(profile.bestLapMs, lapMs);

  return normalizeProfile({
    ...profile,
    money: profile.money + money,
    reputation: profile.reputation + reputation,
    bestLapMs,
    totalLaps: profile.totalLaps + 1
  });
}
