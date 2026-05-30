from __future__ import annotations

import pygame

from .config import GameConfig
from .domain import GamePhase, GameState, HazardPhase, Point
from .modules import SLOT_ORDER, ModuleDefinition, ModuleSlot
from .profile import PlayerProfile


LOADOUT_PHASES = {GamePhase.READY, GamePhase.GAME_OVER, GamePhase.WON}


class Renderer:
    def __init__(self, screen: pygame.Surface, config: GameConfig) -> None:
        self.screen = screen
        self.config = config
        self.font_large = pygame.font.Font(None, 54)
        self.font = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 22)

    def draw(
        self,
        state: GameState,
        profile: PlayerProfile | None = None,
        catalog: dict[str, ModuleDefinition] | None = None,
        selected_slot: ModuleSlot | None = None,
        last_scrap_earned: int = 0,
    ) -> None:
        self.screen.fill(self.config.background_color)
        self._draw_grid()
        self._draw_hazards(state)
        self._draw_food(state)
        self._draw_boss(state)
        self._draw_snake(state)
        self._draw_panel(state, profile, catalog, selected_slot, last_scrap_earned)
        self._draw_overlay(state)
        pygame.display.flip()

    def _draw_grid(self) -> None:
        for x in range(0, self.config.play_width + 1, self.config.cell_size):
            pygame.draw.line(self.screen, self.config.grid_color, (x, 0), (x, self.config.play_height))
        for y in range(0, self.config.play_height + 1, self.config.cell_size):
            pygame.draw.line(self.screen, self.config.grid_color, (0, y), (self.config.play_width, y))

    def _draw_food(self, state: GameState) -> None:
        if state.food is None:
            return
        pygame.draw.rect(self.screen, self.config.food_color, self._cell_rect(state.food).inflate(-6, -6))

    def _draw_hazards(self, state: GameState) -> None:
        for hazard in state.hazards:
            color = (
                self.config.hazard_warning_color
                if hazard.phase == HazardPhase.WARNING
                else self.config.hazard_active_color
            )
            for cell in hazard.cells:
                rect = self._cell_rect(cell).inflate(-4, -4)
                if hazard.phase == HazardPhase.WARNING:
                    pygame.draw.rect(self.screen, color, rect, width=2, border_radius=4)
                else:
                    pygame.draw.rect(self.screen, color, rect, border_radius=4)

    def _draw_boss(self, state: GameState) -> None:
        if state.boss is None:
            return
        pygame.draw.rect(self.screen, self.config.boss_color, self._cell_rect(state.boss.position).inflate(-5, -5), border_radius=8)

    def _draw_snake(self, state: GameState) -> None:
        for index, segment in enumerate(state.snake.body):
            color = self.config.snake_head_color if index == 0 else self.config.snake_body_color
            pygame.draw.rect(self.screen, color, self._cell_rect(segment).inflate(-3, -3), border_radius=4)

    def _draw_panel(
        self,
        state: GameState,
        profile: PlayerProfile | None,
        catalog: dict[str, ModuleDefinition] | None,
        selected_slot: ModuleSlot | None,
        last_scrap_earned: int,
    ) -> None:
        panel_rect = pygame.Rect(self.config.play_width, 0, self.config.side_panel_width, self.config.play_height)
        pygame.draw.rect(self.screen, self.config.panel_color, panel_rect)

        x = self.config.play_width + 22
        self._blit("ULAR", self.font_large, self.config.snake_head_color, x, 28)
        self._blit("Cyber-Roguelite", self.font, self.config.text_color, x, 78)
        self._blit(f"Score: {state.score}", self.font, self.config.text_color, x, 134)
        self._blit(f"Length: {len(state.snake.body)}", self.font, self.config.text_color, x, 168)
        self._blit(f"Heat: {state.heat_level}", self.font_small, self.config.warning_color, x, 204)
        self._blit(f"Shield: {state.shield_charges}", self.font_small, self.config.muted_text_color, x, 228)
        self._blit(f"State: {state.phase.value}", self.font_small, self.config.muted_text_color, x, 252)

        boss_text = "Boss: defeated" if state.boss_defeated else "Boss: dormant"
        if state.boss is not None:
            boss_text = f"Boss: {state.boss.hp}/{state.boss.max_hp}"
        self._blit(boss_text, self.font_small, self.config.boss_color, x, 278)
        self._blit(_clip_text(state.status_message, 28), self.font_small, self.config.muted_text_color, x, 304)

        if profile and catalog:
            self._draw_profile(profile, x, 336)
            self._draw_loadout(state, catalog, selected_slot, x, 404)
            if last_scrap_earned:
                self._blit(f"+{last_scrap_earned} scrap saved", self.font_small, self.config.warning_color, x, 548)

        self._blit(_control_hint(state), self.font_small, self.config.muted_text_color, x, self.config.play_height - 28)

    def _draw_profile(self, profile: PlayerProfile, x: int, y: int) -> None:
        self._blit(f"Scrap: {profile.scrap}", self.font_small, self.config.text_color, x, y)
        self._blit(f"Runs: {profile.total_runs}", self.font_small, self.config.muted_text_color, x, y + 24)
        self._blit(f"Best: {profile.best_score}", self.font_small, self.config.muted_text_color, x, y + 48)

    def _draw_loadout(
        self,
        state: GameState,
        catalog: dict[str, ModuleDefinition],
        selected_slot: ModuleSlot | None,
        x: int,
        y: int,
    ) -> None:
        self._blit("Loadout", self.font, self.config.text_color, x, y)
        y += 34
        for slot in SLOT_ORDER:
            module_id = state.loadout.get(slot.value)
            if module_id not in catalog:
                continue
            module = catalog[module_id]
            prefix = ">" if slot == selected_slot and state.phase in LOADOUT_PHASES else " "
            color = self.config.warning_color if prefix == ">" else self.config.text_color
            self._blit(_clip_text(f"{prefix} {slot.value}: {module.name}", 30), self.font_small, color, x, y)
            y += 22

    def _draw_overlay(self, state: GameState) -> None:
        if state.phase == GamePhase.RUNNING:
            return
        if state.phase == GamePhase.REWARD:
            self._draw_reward_overlay(state)
            return

        messages = {
            GamePhase.READY: ("Choose Loadout", "Left/Right modules, Space to launch"),
            GamePhase.PAUSED: ("Paused", "Press P to resume"),
            GamePhase.GAME_OVER: ("Run Ended", "Press Space to restart"),
            GamePhase.WON: ("Grid Cleared", "Press Space to restart"),
        }
        title, subtitle = messages.get(state.phase, ("", ""))
        if not title:
            return

        overlay = pygame.Surface((self.config.play_width, self.config.play_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        title_surface = self.font_large.render(title, True, self.config.warning_color)
        subtitle_surface = self.font.render(subtitle, True, self.config.text_color)
        self.screen.blit(
            title_surface,
            (
                self.config.play_width // 2 - title_surface.get_width() // 2,
                self.config.play_height // 2 - 48,
            ),
        )
        self.screen.blit(
            subtitle_surface,
            (
                self.config.play_width // 2 - subtitle_surface.get_width() // 2,
                self.config.play_height // 2 + 4,
            ),
        )

    def _cell_rect(self, point: Point) -> pygame.Rect:
        return pygame.Rect(
            point[0] * self.config.cell_size,
            point[1] * self.config.cell_size,
            self.config.cell_size,
            self.config.cell_size,
        )

    def _blit(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        x: int,
        y: int,
    ) -> None:
        self.screen.blit(font.render(text, True, color), (x, y))

    def _draw_reward_overlay(self, state: GameState) -> None:
        overlay = pygame.Surface((self.config.play_width, self.config.play_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title_surface = self.font_large.render("Choose Reward", True, self.config.warning_color)
        self.screen.blit(
            title_surface,
            (
                self.config.play_width // 2 - title_surface.get_width() // 2,
                self.config.play_height // 2 - 106,
            ),
        )

        y = self.config.play_height // 2 - 38
        for index, choice in enumerate(state.reward_choices, start=1):
            label = f"{index}. {choice.name}: {choice.summary}"
            surface = self.font.render(label, True, self.config.text_color)
            self.screen.blit(surface, (self.config.play_width // 2 - surface.get_width() // 2, y))
            y += 42


def _clip_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)] + "..."


def _control_hint(state: GameState) -> str:
    if state.phase == GamePhase.REWARD:
        return "Choose: 1 / 2 / 3"
    if state.phase in LOADOUT_PHASES:
        return "Select modules, Space launch"
    if state.phase == GamePhase.PAUSED:
        return "P resume | Esc quit"
    return "WASD turn | P pause"
