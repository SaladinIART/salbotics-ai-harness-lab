import Phaser from "phaser";
import "./style.css";
import { BootScene } from "./phaser/scenes/BootScene";
import { GarageScene } from "./phaser/scenes/GarageScene";
import { TestTrackScene } from "./phaser/scenes/TestTrackScene";
import { TitleScene } from "./phaser/scenes/TitleScene";

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.CANVAS,
  parent: "game",
  backgroundColor: "#0b1218",
  pixelArt: true,
  scale: {
    mode: Phaser.Scale.RESIZE,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    width: 960,
    height: 640
  },
  scene: [BootScene, TitleScene, GarageScene, TestTrackScene]
};

new Phaser.Game(config);
