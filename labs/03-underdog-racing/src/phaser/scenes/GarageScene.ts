import Phaser from "phaser";
import { createRacingKeys, readRacingActions, type RacingKeys } from "../adapters/keyboard";
import { loadProfile, purchaseUpgrade, saveProfile, type CampaignProfile } from "../../game/progression/profile";
import { UPGRADE_CATEGORIES, UPGRADE_DEFS, upgradeCost, type UpgradeCategory } from "../../game/progression/upgrades";
import { eventById, isEventUnlocked, nextUnlockedEvent, previousUnlockedEvent } from "../../game/progression/campaign";
import { currentChampionshipRound } from "../../game/progression/championship";
import type { DifficultyId } from "../../game/progression/difficulty";
import { renderGarageBuildHud } from "../../ui/hud";

export class GarageScene extends Phaser.Scene {
  private keys!: RacingKeys;
  private profile!: CampaignProfile;
  private selectedIndex = 0;
  private message = "Build the underdog. Buy smart.";

  constructor() {
    super("GarageScene");
  }

  create(): void {
    this.keys = createRacingKeys(this);
    this.profile = loadProfile();
    this.alignSelectedEventToChampionship();
    this.renderHud();
    const { width, height } = this.scale;
    this.add.rectangle(width / 2, height / 2, width, height, 0x101820);
    this.add.rectangle(width / 2, height / 2 + 45, 180, 72, 0x253041).setStrokeStyle(3, 0xfacc15);
    this.add.rectangle(width / 2 - 44, height / 2 + 45, 42, 18, 0x64748b);
    this.add.rectangle(width / 2 + 44, height / 2 + 45, 42, 18, 0x64748b);
    this.add.circle(width / 2 - 66, height / 2 + 83, 16, 0x0f172a).setStrokeStyle(4, 0x94a3b8);
    this.add.circle(width / 2 + 66, height / 2 + 83, 16, 0x0f172a).setStrokeStyle(4, 0x94a3b8);
    this.add.text(width / 2, height / 2 - 92, "GARAGE", {
      fontFamily: "monospace",
      fontSize: "38px",
      color: "#facc15"
    }).setOrigin(0.5);
    this.add.text(width / 2, height / 2 - 40, "Street Compact / Upgrade lab", {
      fontFamily: "monospace",
      fontSize: "18px",
      color: "#dbeafe"
    }).setOrigin(0.5);
    this.add.text(width / 2, height / 2 + 140, "UP/DOWN: part   U: buy   SPACE: test track", {
      fontFamily: "monospace",
      fontSize: "16px",
      color: "#94a3b8"
    }).setOrigin(0.5);
  }

  update(): void {
    const actions = readRacingActions(this.keys);
    if (actions.confirm) {
      this.startSelectedEvent();
    } else if (actions.back) {
      this.scene.start("TitleScene");
    } else if (actions.cycleEventLeft) {
      this.profile.selectedEventId = previousUnlockedEvent(this.profile, this.profile.selectedEventId).id;
      saveProfile(this.profile);
      this.message = "Event selected.";
      this.renderHud();
    } else if (actions.cycleEventRight) {
      this.profile.selectedEventId = nextUnlockedEvent(this.profile, this.profile.selectedEventId).id;
      saveProfile(this.profile);
      this.message = "Event selected.";
      this.renderHud();
    } else if (actions.menuUp) {
      this.selectedIndex = (this.selectedIndex - 1 + UPGRADE_CATEGORIES.length) % UPGRADE_CATEGORIES.length;
      this.message = this.describeSelected();
      this.renderHud();
    } else if (actions.menuDown) {
      this.selectedIndex = (this.selectedIndex + 1) % UPGRADE_CATEGORIES.length;
      this.message = this.describeSelected();
      this.renderHud();
    } else if (actions.buyUpgrade) {
      this.buySelected();
    } else if (actions.difficultyEasy) {
      this.setDifficulty("easy");
    } else if (actions.difficultyNormal) {
      this.setDifficulty("normal");
    } else if (actions.difficultyHard) {
      this.setDifficulty("hard");
    }
  }

  private selectedCategory(): UpgradeCategory {
    return UPGRADE_CATEGORIES[this.selectedIndex];
  }

  private buySelected(): void {
    const category = this.selectedCategory();
    const cost = upgradeCost(category, this.profile.upgrades);
    const next = purchaseUpgrade(this.profile, category);
    if (next === this.profile) {
      this.message = cost === null ? `${UPGRADE_DEFS[category].name} is maxed.` : `Need $${cost}.`;
    } else {
      this.profile = next;
      saveProfile(this.profile);
      this.message = `Bought ${UPGRADE_DEFS[category].name}.`;
    }
    this.renderHud();
  }

  private setDifficulty(difficulty: DifficultyId): void {
    this.profile.difficulty = difficulty;
    saveProfile(this.profile);
    this.message = `Difficulty set to ${difficulty}.`;
    this.renderHud();
  }

  private startSelectedEvent(): void {
    let event = eventById(this.profile.selectedEventId);
    if (!isEventUnlocked(this.profile, event)) {
      event = nextUnlockedEvent(this.profile, this.profile.selectedEventId);
      this.profile.selectedEventId = event.id;
      saveProfile(this.profile);
    }
    if (!isEventUnlocked(this.profile, event)) {
      this.message = "Event locked. Build rep first.";
      this.renderHud();
      return;
    }
    this.scene.start("TestTrackScene");
  }

  private alignSelectedEventToChampionship(): void {
    const round = currentChampionshipRound(this.profile.championship);
    if (round && this.profile.selectedEventId !== round.eventId) {
      this.profile.selectedEventId = round.eventId;
      saveProfile(this.profile);
    }
  }

  private describeSelected(): string {
    const category = this.selectedCategory();
    const cost = upgradeCost(category, this.profile.upgrades);
    return cost === null ? `${UPGRADE_DEFS[category].name} maxed.` : `${UPGRADE_DEFS[category].name} costs $${cost}.`;
  }

  private renderHud(): void {
    renderGarageBuildHud(this.profile, this.selectedCategory(), this.message);
  }
}
