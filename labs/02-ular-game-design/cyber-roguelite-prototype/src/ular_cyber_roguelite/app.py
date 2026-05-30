from __future__ import annotations

import random

import pygame

from .challenge import apply_reward_choice, offer_reward_choices, spawn_boss, spawn_hazard
from .config import GameConfig
from .domain import Direction, GamePhase
from .modules import SLOT_ORDER, compute_run_modifiers, default_module_catalog
from .profile import (
    cycle_profile_slot,
    default_profile_path,
    load_profile,
    record_run,
    save_profile,
    adjust_speed,
)
from .renderer import Renderer
from .systems import create_initial_state, current_fps, request_direction, start_or_restart, step, toggle_pause


KEY_TO_DIRECTION = {
    pygame.K_UP: Direction.UP,
    pygame.K_w: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_s: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_a: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
    pygame.K_d: Direction.RIGHT,
}

LOADOUT_PHASES = {GamePhase.READY, GamePhase.GAME_OVER, GamePhase.WON}
REWARD_KEYS = {
    pygame.K_1: 0,
    pygame.K_2: 1,
    pygame.K_3: 2,
}


def run_game() -> None:
    pygame.init()
    config = GameConfig()
    rng = random.Random()
    catalog = default_module_catalog()
    profile_path = default_profile_path()
    profile = load_profile(profile_path, catalog)
    selected_slot_index = 0
    last_scrap_earned = 0
    run_recorded = False
    developer_mode = False

    def modifiers():
        return compute_run_modifiers(profile.loadout, catalog)

    def build_state(phase: GamePhase):
        return create_initial_state(
            config,
            rng,
            phase=phase,
            modifiers=modifiers(),
            loadout=profile.loadout,
            speed_fps=profile.snake_speed_fps,
            developer_mode=developer_mode,
        )

    screen = pygame.display.set_mode((config.window_width, config.window_height))
    pygame.display.set_caption(config.title)
    clock = pygame.time.Clock()
    renderer = Renderer(screen, config)
    state = build_state(GamePhase.READY)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F1:
                    developer_mode = not developer_mode
                    state.developer_mode = developer_mode
                    state.status_message = f"Developer mode {'ON' if developer_mode else 'OFF'}."
                elif event.key in {pygame.K_MINUS, pygame.K_KP_MINUS, pygame.K_LEFTBRACKET}:
                    adjust_speed(profile, -1)
                    save_profile(profile, profile_path)
                    state.speed_fps = profile.snake_speed_fps
                    state.status_message = f"Speed set to {profile.snake_speed_fps}."
                elif event.key in {pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_RIGHTBRACKET}:
                    adjust_speed(profile, 1)
                    save_profile(profile, profile_path)
                    state.speed_fps = profile.snake_speed_fps
                    state.status_message = f"Speed set to {profile.snake_speed_fps}."
                elif developer_mode and event.key == pygame.K_b and state.phase == GamePhase.RUNNING:
                    spawn_boss(state, config, rng)
                elif developer_mode and event.key == pygame.K_h and state.phase == GamePhase.RUNNING:
                    spawn_hazard(state, config, rng)
                elif developer_mode and event.key == pygame.K_c:
                    state.hazards.clear()
                    state.status_message = "Developer: hazards cleared."
                elif developer_mode and event.key == pygame.K_g and state.phase == GamePhase.RUNNING:
                    state.score += 1
                    state.status_message = "Developer: +1 score."
                elif developer_mode and event.key == pygame.K_r and state.phase == GamePhase.RUNNING:
                    offer_reward_choices(state, rng)
                elif developer_mode and event.key == pygame.K_v:
                    state.shield_charges += 1
                    state.status_message = "Developer: +1 shield."
                elif event.key == pygame.K_SPACE:
                    state = start_or_restart(
                        config,
                        state,
                        rng,
                        modifiers(),
                        profile.loadout,
                        profile.snake_speed_fps,
                        developer_mode,
                    )
                    run_recorded = False
                    last_scrap_earned = 0
                elif event.key == pygame.K_p:
                    toggle_pause(state)
                elif state.phase == GamePhase.REWARD and event.key in REWARD_KEYS:
                    apply_reward_choice(state, REWARD_KEYS[event.key])
                elif event.key in {pygame.K_UP, pygame.K_w} and state.phase in LOADOUT_PHASES:
                    selected_slot_index = (selected_slot_index - 1) % len(SLOT_ORDER)
                elif event.key in {pygame.K_DOWN, pygame.K_s} and state.phase in LOADOUT_PHASES:
                    selected_slot_index = (selected_slot_index + 1) % len(SLOT_ORDER)
                elif event.key in {pygame.K_LEFT, pygame.K_a} and state.phase in LOADOUT_PHASES:
                    cycle_profile_slot(profile, SLOT_ORDER[selected_slot_index], -1, catalog)
                    save_profile(profile, profile_path)
                    state = build_state(state.phase)
                elif event.key in {pygame.K_RIGHT, pygame.K_d} and state.phase in LOADOUT_PHASES:
                    cycle_profile_slot(profile, SLOT_ORDER[selected_slot_index], 1, catalog)
                    save_profile(profile, profile_path)
                    state = build_state(state.phase)
                elif event.key in KEY_TO_DIRECTION:
                    request_direction(state, KEY_TO_DIRECTION[event.key])

        previous_phase = state.phase
        step(state, config, rng)
        if (
            previous_phase == GamePhase.RUNNING
            and state.phase in {GamePhase.GAME_OVER, GamePhase.WON}
            and not run_recorded
        ):
            last_scrap_earned = record_run(profile, state)
            save_profile(profile, profile_path)
            run_recorded = True

        renderer.draw(
            state,
            profile=profile,
            catalog=catalog,
            selected_slot=SLOT_ORDER[selected_slot_index],
            last_scrap_earned=last_scrap_earned,
        )
        clock.tick(current_fps(config, state))

    pygame.quit()
