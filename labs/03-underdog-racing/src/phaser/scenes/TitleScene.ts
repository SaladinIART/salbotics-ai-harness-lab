import Phaser from "phaser";
import { createRacingKeys, readRacingActions, type RacingKeys } from "../adapters/keyboard";
import { renderTitleHud } from "../../ui/hud";

export class TitleScene extends Phaser.Scene {
  private keys!: RacingKeys;

  constructor() {
    super("TitleScene");
  }

  create(): void {
    this.keys = createRacingKeys(this);
    renderTitleHud();
    const { width, height } = this.scale;
    this.add.rectangle(width / 2, height / 2, width, height, 0x080b0f);
    this.add.text(width / 2, height / 2 - 80, "UNDERDOG", {
      fontFamily: "monospace",
      fontSize: "54px",
      color: "#facc15"
    }).setOrigin(0.5);
    this.add.text(width / 2, height / 2 - 20, "street-to-pro racing lab", {
      fontFamily: "monospace",
      fontSize: "20px",
      color: "#dbeafe"
    }).setOrigin(0.5);
    this.add.text(width / 2, height / 2 + 42, "SPACE / ENTER", {
      fontFamily: "monospace",
      fontSize: "18px",
      color: "#94a3b8"
    }).setOrigin(0.5);
  }

  update(): void {
    const actions = readRacingActions(this.keys);
    if (actions.confirm) {
      this.scene.start("GarageScene");
    }
  }
}
