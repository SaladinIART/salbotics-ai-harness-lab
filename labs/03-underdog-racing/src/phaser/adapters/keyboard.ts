import Phaser from "phaser";
import type { RacingActions } from "../../game/input/actions";

export interface RacingKeys {
  up: Phaser.Input.Keyboard.Key;
  down: Phaser.Input.Keyboard.Key;
  left: Phaser.Input.Keyboard.Key;
  right: Phaser.Input.Keyboard.Key;
  w: Phaser.Input.Keyboard.Key;
  a: Phaser.Input.Keyboard.Key;
  s: Phaser.Input.Keyboard.Key;
  d: Phaser.Input.Keyboard.Key;
  space: Phaser.Input.Keyboard.Key;
  enter: Phaser.Input.Keyboard.Key;
  esc: Phaser.Input.Keyboard.Key;
  r: Phaser.Input.Keyboard.Key;
  u: Phaser.Input.Keyboard.Key;
  f1: Phaser.Input.Keyboard.Key;
  shift: Phaser.Input.Keyboard.Key;
  one: Phaser.Input.Keyboard.Key;
  two: Phaser.Input.Keyboard.Key;
  three: Phaser.Input.Keyboard.Key;
}

export function createRacingKeys(scene: Phaser.Scene): RacingKeys {
  const keyboard = scene.input.keyboard;
  if (!keyboard) {
    throw new Error("Keyboard input is unavailable");
  }
  return {
    up: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.UP),
    down: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.DOWN),
    left: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.LEFT),
    right: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.RIGHT),
    w: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W),
    a: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A),
    s: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S),
    d: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D),
    space: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE),
    enter: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.ENTER),
    esc: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.ESC),
    r: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.R),
    u: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.U),
    f1: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.F1),
    shift: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SHIFT),
    one: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.ONE),
    two: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.TWO),
    three: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.THREE)
  };
}

export function readRacingActions(keys: RacingKeys): RacingActions {
  return {
    throttle: keys.up.isDown || keys.w.isDown ? 1 : 0,
    brake: keys.down.isDown || keys.s.isDown ? 1 : 0,
    steer: (keys.right.isDown || keys.d.isDown ? 1 : 0) + (keys.left.isDown || keys.a.isDown ? -1 : 0),
    handbrake: keys.shift.isDown || keys.space.isDown,
    confirm: Phaser.Input.Keyboard.JustDown(keys.space) || Phaser.Input.Keyboard.JustDown(keys.enter),
    back: Phaser.Input.Keyboard.JustDown(keys.esc),
    reset: Phaser.Input.Keyboard.JustDown(keys.r),
    debug: Phaser.Input.Keyboard.JustDown(keys.f1),
    menuUp: Phaser.Input.Keyboard.JustDown(keys.up) || Phaser.Input.Keyboard.JustDown(keys.w),
    menuDown: Phaser.Input.Keyboard.JustDown(keys.down) || Phaser.Input.Keyboard.JustDown(keys.s),
    buyUpgrade: Phaser.Input.Keyboard.JustDown(keys.u),
    cycleEventLeft: Phaser.Input.Keyboard.JustDown(keys.left) || Phaser.Input.Keyboard.JustDown(keys.a),
    cycleEventRight: Phaser.Input.Keyboard.JustDown(keys.right) || Phaser.Input.Keyboard.JustDown(keys.d),
    difficultyEasy: Phaser.Input.Keyboard.JustDown(keys.one),
    difficultyNormal: Phaser.Input.Keyboard.JustDown(keys.two),
    difficultyHard: Phaser.Input.Keyboard.JustDown(keys.three)
  };
}
