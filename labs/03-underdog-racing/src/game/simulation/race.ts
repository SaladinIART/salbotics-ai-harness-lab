import { TEST_TRACK, type TrackModel } from "./track";
import { createTimeTrialState, updateTimeTrial, type TimeTrialState } from "./timeTrial";
import { createRivalState, updateRival, type RivalState } from "./rival";
import type { VehicleControls, VehicleSpec } from "./vehicle";
import { rivalDifficultySpec, type DifficultyId } from "../progression/difficulty";

export interface DuelRaceState {
  player: TimeTrialState;
  rival: RivalState;
  elapsedMs: number;
  playerFinished: boolean;
  playerFinishMs: number | null;
  finishOrder: "player" | "rival" | null;
  message: string;
}

export function createDuelRaceState(track: TrackModel = TEST_TRACK, playerSpec?: VehicleSpec, difficulty: DifficultyId = "normal"): DuelRaceState {
  const player = createTimeTrialState(track, playerSpec);
  const rival = createRivalState(track, rivalDifficultySpec(player.spec, difficulty));
  return {
    player,
    rival,
    elapsedMs: 0,
    playerFinished: false,
    playerFinishMs: null,
    finishOrder: null,
    message: "Beat the local rival."
  };
}

export function updateDuelRace(state: DuelRaceState, controls: VehicleControls, dtMs: number): DuelRaceState {
  if (state.finishOrder !== null) {
    return state;
  }
  const elapsedMs = state.elapsedMs + dtMs;
  const previousLapCount = state.player.lapCount;
  const player = updateTimeTrial(state.player, controls, dtMs);
  const rival = updateRival(state.rival, state.player.track, dtMs, elapsedMs);
  const playerFinished = state.playerFinished || player.lapCount > previousLapCount;
  const playerFinishMs = playerFinished && state.playerFinishMs === null ? elapsedMs : state.playerFinishMs;
  const finishOrder = resolveFinishOrder(playerFinished, playerFinishMs, rival.finished, rival.finishMs);

  return {
    player,
    rival,
    elapsedMs,
    playerFinished,
    playerFinishMs,
    finishOrder,
    message: finishOrder === "player" ? "You beat the rival." : finishOrder === "rival" ? "Rival crossed first." : player.message
  };
}

export function resolveFinishOrder(
  playerFinished: boolean,
  playerFinishMs: number | null,
  rivalFinished: boolean,
  rivalFinishMs: number | null
): "player" | "rival" | null {
  if (!playerFinished && !rivalFinished) {
    return null;
  }
  if (playerFinished && !rivalFinished) {
    return "player";
  }
  if (!playerFinished && rivalFinished) {
    return "rival";
  }
  return (playerFinishMs ?? Number.MAX_SAFE_INTEGER) <= (rivalFinishMs ?? Number.MAX_SAFE_INTEGER) ? "player" : "rival";
}
