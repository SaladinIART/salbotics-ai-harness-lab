import type { CampaignEventId } from "./campaign";

export type ChampionshipId = "street-underdog-cup";
export type SponsorId = "local-parts-shop" | "night-market-energy";
export type TeamFacilityId = "home-garage" | "used-tire-rack" | "crew-notebook";
export type EntrantId = "player" | "rival";

export interface ChampionshipRound {
  eventId: CampaignEventId;
  label: string;
}

export interface ChampionshipRoundResult {
  eventId: CampaignEventId;
  finishOrder: EntrantId;
  playerPoints: number;
  rivalPoints: number;
}

export interface ChampionshipProgress {
  activeId: ChampionshipId;
  roundResults: ChampionshipRoundResult[];
  completedIds: ChampionshipId[];
}

export interface ChampionshipDefinition {
  id: ChampionshipId;
  name: string;
  tier: "Street";
  description: string;
  rounds: ChampionshipRound[];
  points: {
    winner: number;
    runnerUp: number;
  };
  championBonus: {
    money: number;
    reputation: number;
    driverXp: number;
  };
}

export interface SponsorHook {
  id: SponsorId;
  name: string;
  description: string;
  unlockHint: string;
}

export interface TeamFacilityHook {
  id: TeamFacilityId;
  name: string;
  description: string;
  unlockHint: string;
}

export const CHAMPIONSHIPS: ChampionshipDefinition[] = [
  {
    id: "street-underdog-cup",
    name: "Street Underdog Cup",
    tier: "Street",
    description: "A three-round local ladder that proves the car and driver can survive pressure.",
    rounds: [
      { eventId: "backlot-shakedown", label: "Round 1" },
      { eventId: "dockside-sprint", label: "Round 2" },
      { eventId: "club-license-trial", label: "Final" }
    ],
    points: {
      winner: 10,
      runnerUp: 6
    },
    championBonus: {
      money: 160,
      reputation: 5,
      driverXp: 35
    }
  }
];

export const SPONSOR_HOOKS: SponsorHook[] = [
  {
    id: "local-parts-shop",
    name: "Local Parts Shop",
    description: "Starter sponsor hook for discount parts and small win bonuses.",
    unlockHint: "Win the Street Underdog Cup."
  },
  {
    id: "night-market-energy",
    name: "Night Market Energy",
    description: "Riskier later sponsor hook for streak bonuses and heat pressure.",
    unlockHint: "Reach the club tier."
  }
];

export const TEAM_FACILITY_HOOKS: TeamFacilityHook[] = [
  {
    id: "home-garage",
    name: "Home Garage",
    description: "Baseline team-management hook for repairs, setup notes, and upgrade installs.",
    unlockHint: "Available from the start."
  },
  {
    id: "used-tire-rack",
    name: "Used Tire Rack",
    description: "Future facility hook for tire compound choices and wear mitigation.",
    unlockHint: "Earn a sponsor."
  },
  {
    id: "crew-notebook",
    name: "Crew Notebook",
    description: "Future facility hook for setup presets and event scouting.",
    unlockHint: "Complete a championship."
  }
];

export function createDefaultChampionshipProgress(): ChampionshipProgress {
  return {
    activeId: "street-underdog-cup",
    roundResults: [],
    completedIds: []
  };
}

export function normalizeChampionshipProgress(raw: Partial<ChampionshipProgress> | null | undefined): ChampionshipProgress {
  const defaults = createDefaultChampionshipProgress();
  const activeId = raw?.activeId === "street-underdog-cup" ? raw.activeId : defaults.activeId;
  const validRoundIds = new Set(championshipById(activeId).rounds.map((round) => round.eventId));
  const roundResults = Array.isArray(raw?.roundResults)
    ? raw.roundResults.filter((result): result is ChampionshipRoundResult => {
        return (
          result !== null &&
          typeof result === "object" &&
          validRoundIds.has(result.eventId) &&
          (result.finishOrder === "player" || result.finishOrder === "rival") &&
          typeof result.playerPoints === "number" &&
          typeof result.rivalPoints === "number"
        );
      })
    : defaults.roundResults;
  const completedIds = Array.isArray(raw?.completedIds)
    ? raw.completedIds.filter((id): id is ChampionshipId => id === "street-underdog-cup")
    : defaults.completedIds;

  return {
    activeId,
    roundResults: roundResults.slice(0, championshipById(activeId).rounds.length),
    completedIds: Array.from(new Set(completedIds))
  };
}

export function championshipById(id: ChampionshipId): ChampionshipDefinition {
  return CHAMPIONSHIPS.find((championship) => championship.id === id) ?? CHAMPIONSHIPS[0];
}

export function currentChampionshipRound(progress: ChampionshipProgress): ChampionshipRound | null {
  const championship = championshipById(progress.activeId);
  if (progress.roundResults.length >= championship.rounds.length) {
    return null;
  }
  return championship.rounds[progress.roundResults.length];
}

export function championshipStandings(progress: ChampionshipProgress): Record<EntrantId, number> {
  return progress.roundResults.reduce(
    (standings, result) => ({
      player: standings.player + result.playerPoints,
      rival: standings.rival + result.rivalPoints
    }),
    { player: 0, rival: 0 }
  );
}

export function isChampionshipComplete(progress: ChampionshipProgress): boolean {
  return currentChampionshipRound(progress) === null;
}

export function recordChampionshipResult(
  progress: ChampionshipProgress,
  eventId: CampaignEventId,
  finishOrder: EntrantId
): { progress: ChampionshipProgress; recorded: boolean; justCompleted: boolean; playerChampion: boolean } {
  const championship = championshipById(progress.activeId);
  const currentRound = currentChampionshipRound(progress);
  if (currentRound === null || currentRound.eventId !== eventId || progress.completedIds.includes(championship.id)) {
    return { progress, recorded: false, justCompleted: false, playerChampion: isPlayerChampion(progress) };
  }

  const roundResult: ChampionshipRoundResult = {
    eventId,
    finishOrder,
    playerPoints: finishOrder === "player" ? championship.points.winner : championship.points.runnerUp,
    rivalPoints: finishOrder === "rival" ? championship.points.winner : championship.points.runnerUp
  };
  const nextProgress: ChampionshipProgress = {
    ...progress,
    roundResults: [...progress.roundResults, roundResult]
  };
  const justCompleted = isChampionshipComplete(nextProgress);
  const playerChampion = isPlayerChampion(nextProgress);

  return {
    progress: {
      ...nextProgress,
      completedIds: justCompleted
        ? Array.from(new Set([...nextProgress.completedIds, championship.id]))
        : nextProgress.completedIds
    },
    recorded: true,
    justCompleted,
    playerChampion
  };
}

export function isPlayerChampion(progress: ChampionshipProgress): boolean {
  const standings = championshipStandings(progress);
  return standings.player >= standings.rival;
}
