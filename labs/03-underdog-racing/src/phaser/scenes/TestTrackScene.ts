import Phaser from "phaser";
import { readRacingActions, createRacingKeys, type RacingKeys } from "../adapters/keyboard";
import { renderDuelHud } from "../../ui/hud";
import { createDuelRaceState, updateDuelRace, type DuelRaceState } from "../../game/simulation/race";
import { TEST_TRACK, insideGate } from "../../game/simulation/track";
import { fromAngle } from "../../game/simulation/vector";
import { loadProfile, normalizeProfile, saveProfile, type CampaignProfile } from "../../game/progression/profile";
import { specFromProfile } from "../../game/progression/upgrades";
import { completeDuelEvent, eventById } from "../../game/progression/campaign";

interface VehicleDisplay {
  container: Phaser.GameObjects.Container;
  body: Phaser.GameObjects.Rectangle;
  frontTires: Phaser.GameObjects.Rectangle[];
}

export class TestTrackScene extends Phaser.Scene {
  private keys!: RacingKeys;
  private state!: DuelRaceState;
  private car!: Phaser.GameObjects.Container;
  private rivalCar!: Phaser.GameObjects.Container;
  private carBody!: Phaser.GameObjects.Rectangle;
  private playerFrontTires: Phaser.GameObjects.Rectangle[] = [];
  private rivalFrontTires: Phaser.GameObjects.Rectangle[] = [];
  private speedLabel!: Phaser.GameObjects.Text;
  private currentSteer = 0;
  private debugEnabled = false;
  private profile!: CampaignProfile;
  private eventSettled = false;

  constructor() {
    super("TestTrackScene");
  }

  create(): void {
    this.keys = createRacingKeys(this);
    this.profile = loadProfile();
    this.state = createDuelRaceState(TEST_TRACK, specFromProfile(this.profile), this.profile.difficulty);
    this.state.player.bestLapMs = this.profile.bestLapMs;
    this.cameras.main.setBounds(0, 0, TEST_TRACK.width, TEST_TRACK.height);
    this.drawTrack();
    const playerDisplay = this.createVehicleDisplay(0xfacc15, 0xef4444);
    this.car = playerDisplay.container;
    this.carBody = playerDisplay.body;
    this.playerFrontTires = playerDisplay.frontTires;
    const rivalDisplay = this.createVehicleDisplay(0x38bdf8, 0x1d4ed8);
    this.rivalCar = rivalDisplay.container;
    this.rivalFrontTires = rivalDisplay.frontTires;
    this.speedLabel = this.add.text(0, 0, "0 px/s", {
      fontFamily: "monospace",
      fontSize: "14px",
      color: "#f8fafc",
      backgroundColor: "#020617"
    }).setOrigin(0.5);
    this.syncCars();
    this.cameras.main.startFollow(this.car, true, 0.12, 0.12);
    this.cameras.main.setZoom(1.15);
    renderDuelHud(this.state, this.debugEnabled, this.profile);
  }

  update(_time: number, delta: number): void {
    const actions = readRacingActions(this.keys);
    if (actions.back) {
      this.scene.start("GarageScene");
      return;
    }
    if (actions.reset) {
      this.state = createDuelRaceState(TEST_TRACK, specFromProfile(this.profile), this.profile.difficulty);
      this.eventSettled = false;
    }
    if (actions.debug) {
      this.debugEnabled = !this.debugEnabled;
    }

    this.currentSteer = actions.steer;
    this.state = updateDuelRace(
      this.state,
      {
        throttle: actions.throttle,
        brake: actions.brake,
        steer: actions.steer,
        handbrake: actions.handbrake
      },
      delta
    );
    this.settleFinishedRace();
    this.syncCars();
    renderDuelHud(this.state, this.debugEnabled, this.profile);
  }

  private settleFinishedRace(): void {
    if (this.eventSettled || this.state.finishOrder === null) {
      return;
    }
    const event = eventById(this.profile.selectedEventId);
    const completed = completeDuelEvent(
      this.profile,
      event,
      this.state.playerFinishMs ?? this.state.elapsedMs,
      this.state.finishOrder
    );
    this.profile = normalizeProfile(completed.profile);
    this.state.player.bestLapMs = this.profile.bestLapMs;
    if (completed.result.championshipComplete) {
      this.state.message = completed.result.championshipWon
        ? `Cup won. +$${completed.result.money}`
        : `Cup lost. +$${completed.result.money}`;
    } else {
      this.state.message = this.state.finishOrder === "player"
        ? `Won duel. +$${completed.result.money}`
        : `Rival won. +$${completed.result.money}`;
    }
    saveProfile(this.profile);
    this.eventSettled = true;
  }

  private drawTrack(): void {
    const g = this.add.graphics();
    g.fillStyle(0x0f3d2e, 1);
    g.fillRect(0, 0, TEST_TRACK.width, TEST_TRACK.height);
    g.fillStyle(0x164e35, 1);
    g.fillEllipse(700, 475, 520, 250);
    g.fillStyle(0x78350f, 0.55);
    g.fillEllipse(1130, 240, 250, 150);
    g.fillEllipse(780, 760, 260, 130);
    g.fillStyle(0x334155, 1);
    g.fillRect(84, 492, 210, 172);
    g.fillStyle(0x020617, 1);
    g.fillRect(102, 512, 168, 18);
    g.fillRect(102, 552, 168, 18);
    g.fillRect(102, 592, 168, 18);

    this.drawTrackRibbon(g, TEST_TRACK.roadWidth + TEST_TRACK.curbWidth * 2 + 14, 0x111827, 1);
    this.drawTrackRibbon(g, TEST_TRACK.roadWidth + TEST_TRACK.curbWidth * 2, 0xf97316, 1);
    this.drawTrackRibbon(g, TEST_TRACK.roadWidth, 0x263241, 1);
    this.drawTrackRibbon(g, 4, 0x475569, 0.75);

    g.fillStyle(0xf8fafc, 1);
    g.fillRect(TEST_TRACK.startGate.x, TEST_TRACK.startGate.y, TEST_TRACK.startGate.w, TEST_TRACK.startGate.h);
    g.fillStyle(0x111827, 1);
    for (let y = TEST_TRACK.startGate.y; y < TEST_TRACK.startGate.y + TEST_TRACK.startGate.h; y += 22) {
      g.fillRect(TEST_TRACK.startGate.x, y, TEST_TRACK.startGate.w, 11);
    }
    g.lineStyle(2, 0x38bdf8, 0.35);
    for (const gate of TEST_TRACK.checkpoints) {
      g.strokeRect(gate.x, gate.y, gate.w, gate.h);
    }
    g.lineStyle(3, 0xe2e8f0, 0.85);
    g.strokeRect(90, 500, 190, 150);
    g.lineStyle(1, 0xfacc15, 0.75);
    g.lineBetween(120, 500, 120, 650);
    g.lineBetween(250, 500, 250, 650);
  }

  private drawTrackRibbon(g: Phaser.GameObjects.Graphics, width: number, color: number, alpha: number): void {
    g.lineStyle(width, color, alpha);
    for (let index = 0; index < TEST_TRACK.centerLine.length - 1; index += 1) {
      const start = TEST_TRACK.centerLine[index];
      const end = TEST_TRACK.centerLine[index + 1];
      g.lineBetween(start.x, start.y, end.x, end.y);
    }
    g.fillStyle(color, alpha);
    for (const point of TEST_TRACK.centerLine) {
      g.fillCircle(point.x, point.y, width / 2);
    }
  }

  private createVehicleDisplay(bodyColor: number, noseColor: number): VehicleDisplay {
    const rearLeft = this.add.rectangle(-12, -13, 12, 5, 0x020617).setStrokeStyle(1, 0x94a3b8);
    const rearRight = this.add.rectangle(-12, 13, 12, 5, 0x020617).setStrokeStyle(1, 0x94a3b8);
    const frontLeft = this.add.rectangle(12, -13, 12, 5, 0x020617).setStrokeStyle(1, 0xe2e8f0);
    const frontRight = this.add.rectangle(12, 13, 12, 5, 0x020617).setStrokeStyle(1, 0xe2e8f0);
    const shadow = this.add.rectangle(-1, 2, 39, 22, 0x020617, 0.34);
    const body = this.add.rectangle(0, 0, 36, 18, bodyColor).setStrokeStyle(2, 0x111827);
    const cockpit = this.add.rectangle(-3, 0, 12, 10, 0x0f172a, 0.9);
    const nose = this.add.triangle(21, 0, 0, -9, 0, 9, 15, 0, noseColor);
    const wing = this.add.rectangle(20, 0, 4, 24, 0xe2e8f0, 0.85);
    const container = this.add.container(TEST_TRACK.spawn.x, TEST_TRACK.spawn.y, [
      shadow,
      rearLeft,
      rearRight,
      frontLeft,
      frontRight,
      body,
      cockpit,
      nose,
      wing
    ]);

    return {
      container,
      body,
      frontTires: [frontLeft, frontRight]
    };
  }

  private syncCars(): void {
    this.car.setPosition(this.state.player.vehicle.position.x, this.state.player.vehicle.position.y);
    this.car.setRotation(this.state.player.vehicle.heading);
    this.rivalCar.setPosition(this.state.rival.vehicle.position.x, this.state.rival.vehicle.position.y);
    this.rivalCar.setRotation(this.state.rival.vehicle.heading);
    this.animateFrontTires(this.playerFrontTires, this.currentSteer);
    this.animateFrontTires(this.rivalFrontTires, this.rivalSteerHint());
    this.speedLabel.setText(`${this.state.player.telemetry.speed.toFixed(0)} px/s`);
    this.speedLabel.setPosition(this.state.player.vehicle.position.x, this.state.player.vehicle.position.y - 38);
    const onStart = insideGate(this.state.player.vehicle.position, TEST_TRACK.startGate);
    this.carBody.setFillStyle(onStart ? 0x22c55e : 0xfacc15);

    if (this.debugEnabled) {
      this.drawVelocityLine();
    }
  }

  private animateFrontTires(tires: Phaser.GameObjects.Rectangle[], steer: number): void {
    const angle = Phaser.Math.Clamp(steer, -1, 1) * 0.42;
    for (const tire of tires) {
      tire.setRotation(angle);
    }
  }

  private rivalSteerHint(): number {
    const target = TEST_TRACK.checkpoints[Math.min(this.state.rival.nextWaypointIndex, TEST_TRACK.checkpoints.length - 1)]
      ?? TEST_TRACK.startGate;
    const dx = target.x + target.w / 2 - this.state.rival.vehicle.position.x;
    const dy = target.y + target.h / 2 - this.state.rival.vehicle.position.y;
    const desired = Math.atan2(dy, dx);
    let angle = desired - this.state.rival.vehicle.heading;
    while (angle > Math.PI) {
      angle -= Math.PI * 2;
    }
    while (angle < -Math.PI) {
      angle += Math.PI * 2;
    }
    return Phaser.Math.Clamp(angle * 1.8, -1, 1);
  }

  private drawVelocityLine(): void {
    const old = this.children.getByName("debug-velocity");
    if (old) {
      old.destroy();
    }
    const forward = fromAngle(this.state.player.vehicle.heading);
    const line = this.add.line(
      0,
      0,
      this.state.player.vehicle.position.x,
      this.state.player.vehicle.position.y,
      this.state.player.vehicle.position.x + forward.x * 70,
      this.state.player.vehicle.position.y + forward.y * 70,
      0x38bdf8
    );
    line.setOrigin(0, 0);
    line.setName("debug-velocity");
  }
}
