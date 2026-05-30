from __future__ import annotations

import random
from collections.abc import Iterable

from .challenge import active_hazard_cells, advance_challenge, damage_boss, maybe_offer_reward, occupied_cells
from .config import GameConfig
from .domain import Direction, GamePhase, GameState, Point, Snake
from .modules import RunModifiers


def create_initial_state(
    config: GameConfig,
    rng: random.Random | None = None,
    phase: GamePhase = GamePhase.READY,
    modifiers: RunModifiers | None = None,
    loadout: dict[str, str] | None = None,
    speed_fps: int | None = None,
    developer_mode: bool = False,
) -> GameState:
    rng = rng or random.Random()
    modifiers = modifiers or RunModifiers()
    center = (config.grid_columns // 2, config.grid_rows // 2)
    starting_length = max(2, min(config.grid_columns - 1, 3 + modifiers.starting_length_bonus))
    body = [(center[0] - offset, center[1]) for offset in range(starting_length)]
    food = spawn_food(config, body, rng)
    return GameState(
        snake=Snake(body=body),
        food=food,
        phase=phase,
        loadout=loadout or {},
        modifiers=modifiers,
        speed_fps=speed_fps or config.fps,
        shield_charges=modifiers.shield_charges,
        developer_mode=developer_mode,
    )


def spawn_food(
    config: GameConfig,
    occupied: Iterable[Point],
    rng: random.Random | None = None,
) -> Point | None:
    rng = rng or random.Random()
    occupied_set = set(occupied)
    free_cells = [
        (x, y)
        for y in range(config.grid_rows)
        for x in range(config.grid_columns)
        if (x, y) not in occupied_set
    ]
    if not free_cells:
        return None
    return rng.choice(free_cells)


def request_direction(state: GameState, direction: Direction) -> None:
    if state.phase != GamePhase.RUNNING:
        return
    if direction.is_opposite(state.snake.direction):
        return
    state.snake.direction = direction


def start_or_restart(
    config: GameConfig,
    state: GameState,
    rng: random.Random | None = None,
    modifiers: RunModifiers | None = None,
    loadout: dict[str, str] | None = None,
    speed_fps: int | None = None,
    developer_mode: bool | None = None,
) -> GameState:
    if state.phase in {GamePhase.READY, GamePhase.GAME_OVER, GamePhase.WON}:
        return create_initial_state(
            config,
            rng,
            phase=GamePhase.RUNNING,
            modifiers=modifiers or state.modifiers,
            loadout=loadout or state.loadout,
            speed_fps=speed_fps or state.speed_fps,
            developer_mode=state.developer_mode if developer_mode is None else developer_mode,
        )
    return state


def toggle_pause(state: GameState) -> None:
    if state.phase == GamePhase.RUNNING:
        state.phase = GamePhase.PAUSED
    elif state.phase == GamePhase.PAUSED:
        state.phase = GamePhase.RUNNING


def step(state: GameState, config: GameConfig, rng: random.Random | None = None) -> None:
    if state.phase != GamePhase.RUNNING:
        return

    rng = rng or random.Random()
    state.ticks += 1

    dx, dy = state.snake.direction.delta
    new_head = (state.snake.head[0] + dx, state.snake.head[1] + dy)

    hit_boss = state.boss is not None and new_head == state.boss.position
    ate_food = state.food is not None and new_head == state.food
    collision_body = _collision_body(state, ate_food=ate_food, hit_boss=hit_boss)

    if is_out_of_bounds(new_head, config) or new_head in collision_body:
        if _absorb_fatal_collision(state):
            state.status_message = "Shield absorbed a fatal hit."
            return
        state.phase = GamePhase.GAME_OVER
        state.status_message = "Run ended. Fatal collision."
        return

    state.snake.body.insert(0, new_head)

    if new_head in active_hazard_cells(state):
        if _absorb_fatal_collision(state, remove_head=True):
            state.status_message = "Shield burned through an active hazard."
            return
        state.phase = GamePhase.GAME_OVER
        state.status_message = "Run ended. Active hazard hit."
        return

    if hit_boss:
        damage_boss(state, config, rng)
    elif ate_food:
        state.score += state.modifiers.score_per_food
        state.growth_pending += state.modifiers.growth_per_food - 1
        state.food = spawn_food(config, occupied_cells(state), rng)
        if state.food is None:
            state.phase = GamePhase.WON
            state.status_message = "Grid cleared."

    if ate_food:
        pass
    elif state.growth_pending > 0:
        state.growth_pending -= 1
    else:
        state.snake.body.pop()

    advance_challenge(state, config, rng)
    maybe_offer_reward(state, rng)


def is_out_of_bounds(point: Point, config: GameConfig) -> bool:
    x, y = point
    return x < 0 or y < 0 or x >= config.grid_columns or y >= config.grid_rows


def current_fps(config: GameConfig, state: GameState) -> int:
    heat_bonus = max(0, state.heat_level // 2)
    return max(config.min_fps, min(config.max_fps, state.speed_fps + state.modifiers.fps_delta + heat_bonus))


def _absorb_fatal_collision(state: GameState, remove_head: bool = False) -> bool:
    if state.shield_charges <= 0:
        return False
    state.shield_charges -= 1
    state.snake.direction = state.snake.direction.opposite()
    if remove_head and state.snake.body:
        state.snake.body.pop(0)
    return True


def _collision_body(state: GameState, ate_food: bool, hit_boss: bool) -> list[Point]:
    if ate_food or hit_boss or state.growth_pending > 0:
        return state.snake.body
    return state.snake.body[:-1]
