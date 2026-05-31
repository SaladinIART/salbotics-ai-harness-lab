import { formatLapTime, type TimeTrialState } from "../game/simulation/timeTrial";
import { type DuelRaceState } from "../game/simulation/race";
import { type CampaignProfile } from "../game/progression/profile";
import { UPGRADE_CATEGORIES, UPGRADE_DEFS, buildRating, upgradeCost, type UpgradeCategory } from "../game/progression/upgrades";
import { DRIVER_SKILLS, unlockedDriverSkills } from "../game/progression/driverSkills";
import { eventById, isEventUnlocked } from "../game/progression/campaign";
import {
  SPONSOR_HOOKS,
  TEAM_FACILITY_HOOKS,
  championshipById,
  championshipStandings,
  currentChampionshipRound
} from "../game/progression/championship";
import { DIFFICULTIES, difficultyById } from "../game/progression/difficulty";

export function setHud(html: string): void {
  const hud = document.getElementById("hud");
  if (hud) {
    hud.innerHTML = html;
  }
}

export function renderTitleHud(): void {
  setHud(`
    <h1 class="hud-title">UNDERDOG</h1>
    <div class="hud-section">Street-to-pro racing lab.</div>
    <div class="hud-section"><span class="hud-label">Enter / Space</span><br />Open garage</div>
    <div class="hud-section"><span class="hud-label">CP1-CP7</span><br />Physics, Garage, rivals, and championship loop.</div>
  `);
}

export function renderGarageHud(): void {
  setHud(`
    <h1 class="hud-title">GARAGE</h1>
    <div class="hud-section"><span class="hud-label">Car</span><br /><span class="hud-value">Street Compact</span></div>
    <div class="hud-section"><span class="hud-label">Build</span><br />Stock tires, tired brakes, cheap engine.</div>
    <div class="hud-section"><span class="hud-label">Goal</span><br />Learn handling before rivals arrive.</div>
    <div class="hud-section"><span class="hud-label">Space / Enter</span><br />Start test track</div>
    <div class="hud-section"><span class="hud-label">Esc</span><br />Back to title</div>
  `);
}

export function renderGarageBuildHud(profile: CampaignProfile, selected: UpgradeCategory, message: string): void {
  const cost = upgradeCost(selected, profile.upgrades);
  const selectedDef = UPGRADE_DEFS[selected];
  const event = eventById(profile.selectedEventId);
  const eventUnlocked = isEventUnlocked(profile, event);
  const skills = unlockedDriverSkills(profile);
  const nextSkill = DRIVER_SKILLS.find((skill) => !skills.includes(skill.id));
  const championship = championshipById(profile.championship.activeId);
  const round = currentChampionshipRound(profile.championship);
  const standings = championshipStandings(profile.championship);
  const sponsor = SPONSOR_HOOKS.find((hook) => hook.id === profile.sponsorId);
  const difficulty = difficultyById(profile.difficulty);
  const difficultyRows = DIFFICULTIES.map((item, index) => {
    const marker = item.id === profile.difficulty ? ">" : "&nbsp;";
    return `<div>${marker} ${index + 1}. ${item.name}</div>`;
  }).join("");
  const facilityRows = TEAM_FACILITY_HOOKS.map((facility) => {
    const level = profile.teamFacilities[facility.id];
    return `${facility.name}: ${level > 0 ? `Lv ${level}` : "locked"}`;
  }).join("<br />");
  const rows = UPGRADE_CATEGORIES.map((category) => {
    const def = UPGRADE_DEFS[category];
    const marker = category === selected ? ">" : "&nbsp;";
    const level = profile.upgrades[category];
    return `<div>${marker} ${def.name}: <span class="hud-value">${level}/${def.maxLevel}</span></div>`;
  }).join("");

  setHud(`
    <h1 class="hud-title">GARAGE</h1>
    <div class="hud-section"><span class="hud-label">Money</span><br /><span class="hud-value">$${profile.money}</span></div>
    <div class="hud-section"><span class="hud-label">Reputation / License</span><br />${profile.reputation} / ${profile.license}</div>
    <div class="hud-section"><span class="hud-label">Event</span><br /><span class="hud-value">${event.name}</span><br />${event.tier} target ${formatLapTime(event.targetLapMs)}${eventUnlocked ? "" : "<br /><span class=\"hud-warning\">Locked</span>"}</div>
    <div class="hud-section"><span class="hud-label">Difficulty</span><br /><span class="hud-value">${difficulty.name}</span><br />${difficulty.description}<br />${difficultyRows}</div>
    <div class="hud-section"><span class="hud-label">Championship</span><br /><span class="hud-value">${championship.name}</span><br />${round ? `${round.label}: ${eventById(round.eventId).name}` : "Cup complete"}<br />You ${standings.player} / Rival ${standings.rival}</div>
    <div class="hud-section"><span class="hud-label">Sponsor / Team</span><br />${sponsor ? sponsor.name : "No sponsor yet"}<br />${facilityRows}</div>
    <div class="hud-section"><span class="hud-label">Driver XP</span><br />${profile.driverXp}${nextSkill ? ` / ${nextSkill.requiredXp} for ${nextSkill.name}` : " / max skills"}</div>
    <div class="hud-section"><span class="hud-label">Build rating</span><br />${buildRating(profile.upgrades)}</div>
    <div class="hud-section">${rows}</div>
    <div class="hud-section"><span class="hud-label">${selectedDef.name}</span><br />${selectedDef.description}</div>
    <div class="hud-section"><span class="hud-label">Upgrade cost</span><br />${cost === null ? "MAX" : `$${cost}`}</div>
    <div class="hud-section ${message.includes("Bought") ? "hud-warning" : ""}">${message}</div>
    <div class="hud-section"><span class="hud-label">Controls</span><br />Up/Down part, Left/Right event, 1/2/3 difficulty, U buy, Space test track, Esc title</div>
  `);
}

export function renderRaceHud(state: TimeTrialState, debugEnabled: boolean, profile?: CampaignProfile): void {
  const t = state.telemetry;
  const currentLap = state.elapsedMs - state.lapStartMs;
  const event = profile ? eventById(profile.selectedEventId) : null;
  setHud(`
    <h1 class="hud-title">TEST TRACK</h1>
    <div class="hud-section"><span class="hud-label">Lap</span><br /><span class="hud-value">${formatLapTime(currentLap)}</span></div>
    <div class="hud-section"><span class="hud-label">Best</span><br /><span class="hud-value">${formatLapTime(state.bestLapMs)}</span></div>
    ${event ? `<div class="hud-section"><span class="hud-label">Event</span><br />${event.name}<br />Target ${formatLapTime(event.targetLapMs)}</div>` : ""}
    ${profile ? `<div class="hud-section"><span class="hud-label">Money</span><br />$${profile.money}</div>` : ""}
    ${profile ? `<div class="hud-section"><span class="hud-label">Build</span><br />${buildRating(profile.upgrades)}</div>` : ""}
    <div class="hud-section"><span class="hud-label">Speed</span><br />${t.speed.toFixed(0)} px/s</div>
    <div class="hud-section"><span class="hud-label">Surface</span><br />${t.surface}</div>
    <div class="hud-section"><span class="hud-label">Tire wear</span><br />${(t.tireWear * 100).toFixed(1)}%</div>
    <div class="hud-section"><span class="hud-label">Next gate</span><br />${state.nextCheckpointIndex + 1}</div>
    <div class="hud-section ${state.message.includes("complete") ? "hud-warning" : ""}">${state.message}</div>
    <div class="hud-section"><span class="hud-label">Controls</span><br />WASD/Arrows, Shift/Space handbrake, R reset, Esc garage</div>
    ${
      debugEnabled
        ? `<div class="hud-section"><span class="hud-label">Debug</span><br />Forward ${t.forwardSpeed.toFixed(1)}<br />Lateral ${t.lateralSpeed.toFixed(1)}<br />Grip ${t.grip.toFixed(2)}</div>`
        : `<div class="hud-section"><span class="hud-label">F1</span><br />Debug telemetry</div>`
    }
  `);
}

export function renderDuelHud(state: DuelRaceState, debugEnabled: boolean, profile: CampaignProfile): void {
  const event = eventById(profile.selectedEventId);
  const t = state.player.telemetry;
  const currentLap = state.player.elapsedMs - state.player.lapStartMs;
  setHud(`
    <h1 class="hud-title">RIVAL DUEL</h1>
    <div class="hud-section"><span class="hud-label">Event</span><br />${event.name}<br />Target ${formatLapTime(event.targetLapMs)}</div>
    <div class="hud-section"><span class="hud-label">Lap</span><br /><span class="hud-value">${formatLapTime(currentLap)}</span></div>
    <div class="hud-section"><span class="hud-label">Player</span><br />${state.playerFinished ? formatLapTime(state.playerFinishMs) : "racing"}</div>
    <div class="hud-section"><span class="hud-label">Rival</span><br />${state.rival.finished ? formatLapTime(state.rival.finishMs) : `Gate ${state.rival.nextWaypointIndex + 1}`}</div>
    <div class="hud-section"><span class="hud-label">Difficulty</span><br />${difficultyById(profile.difficulty).name}</div>
    <div class="hud-section"><span class="hud-label">Speed</span><br /><span class="hud-value">${t.speed.toFixed(0)} px/s</span></div>
    <div class="hud-section ${state.finishOrder === "player" ? "hud-warning" : ""}">${state.message}</div>
    <div class="hud-section"><span class="hud-label">Controls</span><br />WASD/Arrows, Shift/Space handbrake, R reset, Esc garage</div>
    ${
      debugEnabled
        ? `<div class="hud-section"><span class="hud-label">Debug</span><br />Forward ${t.forwardSpeed.toFixed(1)}<br />Lateral ${t.lateralSpeed.toFixed(1)}<br />Rival speed ${state.rival.telemetry.speed.toFixed(1)}</div>`
        : `<div class="hud-section"><span class="hud-label">F1</span><br />Debug telemetry</div>`
    }
  `);
}
