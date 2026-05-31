export interface RacingActions {
  throttle: number;
  brake: number;
  steer: number;
  handbrake: boolean;
  confirm: boolean;
  back: boolean;
  reset: boolean;
  debug: boolean;
  menuUp: boolean;
  menuDown: boolean;
  buyUpgrade: boolean;
  cycleEventLeft: boolean;
  cycleEventRight: boolean;
  difficultyEasy: boolean;
  difficultyNormal: boolean;
  difficultyHard: boolean;
}

export const IDLE_ACTIONS: RacingActions = {
  throttle: 0,
  brake: 0,
  steer: 0,
  handbrake: false,
  confirm: false,
  back: false,
  reset: false,
  debug: false,
  menuUp: false,
  menuDown: false,
  buyUpgrade: false,
  cycleEventLeft: false,
  cycleEventRight: false,
  difficultyEasy: false,
  difficultyNormal: false,
  difficultyHard: false
};
