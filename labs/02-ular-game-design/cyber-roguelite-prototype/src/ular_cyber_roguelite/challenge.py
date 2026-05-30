from __future__ import annotations

import random
from collections.abc import Iterable

from .config import GameConfig
from .domain import BossState, GamePhase, GameState, HazardPatch, HazardPhase, Point, RewardChoice


REWARD_INTERVAL = 8
BOSS_SCORE_THRESHOLD = 8
BOSS_MAX_HP = 3
HAZARD_WARNING_TICKS = 4
HAZARD_ACTIVE_TICKS = 4

REWARD_POOL: tuple[RewardChoice, ...] = (
    RewardChoice(
        reward_id="emergency_shield",
        name="Emergency Shield",
        summary="+1 shield charge.",
    ),
    RewardChoice(
        reward_id="servo_trim",
        name="Servo Trim",
        summary="Remove up to 2 tail segments.",
    ),
    RewardChoice(
        reward_id="coolant_bloom",
        name="Coolant Bloom",
        summary="Clear all current hazard zones.",
    ),
)


def active_hazard_cells(state: GameState) -> set[Point]:
    return {
        cell
        for hazard in state.hazards
        if hazard.phase == HazardPhase.ACTIVE
        for cell in hazard.cells
    }


def all_hazard_cells(state: GameState) -> set[Point]:
    return {cell for hazard in state.hazards for cell in hazard.cells}


def occupied_cells(state: GameState) -> set[Point]:
    occupied = set(state.snake.body) | all_hazard_cells(state)
    if state.food is not None:
        occupied.add(state.food)
    if state.boss is not None:
        occupied.add(state.boss.position)
    return occupied


def free_cells(
    config: GameConfig,
    occupied: Iterable[Point],
) -> list[Point]:
    blocked = set(occupied)
    return [
        (x, y)
        for y in range(config.grid_rows)
        for x in range(config.grid_columns)
        if (x, y) not in blocked
    ]


def advance_challenge(state: GameState, config: GameConfig, rng: random.Random) -> None:
    if state.phase != GamePhase.RUNNING:
        return

    state.heat_level = max(state.heat_level, min(6, state.score // 7 + state.ticks // 240))
    state.hazards = _advance_hazards(state.hazards)

    if state.score >= BOSS_SCORE_THRESHOLD and not state.boss_defeated and state.boss is None:
        spawn_boss(state, config, rng)

    interval = max(10, 34 - state.heat_level * 3)
    if state.ticks % interval == 0:
        spawn_hazard(state, config, rng)


def spawn_hazard(state: GameState, config: GameConfig, rng: random.Random) -> HazardPatch | None:
    cells = free_cells(config, occupied_cells(state))
    if not cells:
        return None

    patch_size = min(len(cells), 1 + state.heat_level // 2)
    selected = tuple(rng.sample(cells, patch_size))
    hazard = HazardPatch(cells=selected, phase=HazardPhase.WARNING, ticks_remaining=HAZARD_WARNING_TICKS)
    state.hazards.append(hazard)
    state.status_message = "Hazard warning: move before it arms."
    return hazard


def spawn_boss(state: GameState, config: GameConfig, rng: random.Random) -> BossState | None:
    cells = free_cells(config, occupied_cells(state))
    if not cells:
        return None

    boss = BossState(
        name="Circuit Warden",
        position=rng.choice(cells),
        hp=BOSS_MAX_HP,
        max_hp=BOSS_MAX_HP,
    )
    state.boss = boss
    state.status_message = "Circuit Warden online: bite the blue node."
    return boss


def damage_boss(state: GameState, config: GameConfig, rng: random.Random) -> None:
    if state.boss is None:
        return

    state.boss.hp -= 1
    state.score += state.boss.score_reward
    if state.boss.hp <= 0:
        state.boss = None
        state.boss_defeated = True
        state.status_message = "Circuit Warden cracked. Choose a reward."
        offer_reward_choices(state, rng)
        return

    cells = free_cells(config, occupied_cells(state))
    if cells:
        state.boss.position = rng.choice(cells)
    state.status_message = f"Circuit Warden hit. HP {state.boss.hp}/{state.boss.max_hp}."


def maybe_offer_reward(state: GameState, rng: random.Random) -> None:
    if state.phase != GamePhase.RUNNING:
        return
    if state.score < state.next_reward_score:
        return

    state.next_reward_score += REWARD_INTERVAL
    state.status_message = "Milestone reached. Choose a reward."
    offer_reward_choices(state, rng)


def offer_reward_choices(state: GameState, rng: random.Random) -> None:
    choice_count = min(3, len(REWARD_POOL))
    state.reward_choices = list(rng.sample(REWARD_POOL, choice_count))
    state.phase = GamePhase.REWARD


def apply_reward_choice(state: GameState, choice_index: int) -> None:
    if state.phase != GamePhase.REWARD or not state.reward_choices:
        return
    if choice_index < 0 or choice_index >= len(state.reward_choices):
        return

    choice = state.reward_choices[choice_index]
    state.rewards_taken.append(choice.reward_id)

    if choice.reward_id == "emergency_shield":
        state.shield_charges += 1
        state.status_message = "Reward installed: +1 shield charge."
    elif choice.reward_id == "servo_trim":
        target_length = max(2, len(state.snake.body) - 2)
        state.snake.body = state.snake.body[:target_length]
        state.status_message = "Reward installed: tail trimmed."
    elif choice.reward_id == "coolant_bloom":
        state.hazards.clear()
        state.status_message = "Reward installed: hazards cleared."

    state.reward_choices.clear()
    state.phase = GamePhase.RUNNING


def _advance_hazards(hazards: list[HazardPatch]) -> list[HazardPatch]:
    advanced: list[HazardPatch] = []
    for hazard in hazards:
        ticks_remaining = hazard.ticks_remaining - 1
        if ticks_remaining > 0:
            advanced.append(
                HazardPatch(
                    cells=hazard.cells,
                    phase=hazard.phase,
                    ticks_remaining=ticks_remaining,
                )
            )
            continue

        if hazard.phase == HazardPhase.WARNING:
            advanced.append(HazardPatch(cells=hazard.cells, phase=HazardPhase.ACTIVE, ticks_remaining=HAZARD_ACTIVE_TICKS))

    return advanced
