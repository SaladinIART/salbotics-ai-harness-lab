from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    title: str = "Ular Cyber-Roguelite Prototype"
    cell_size: int = 24
    grid_columns: int = 30
    grid_rows: int = 24
    side_panel_width: int = 320
    fps: int = 10

    background_color: tuple[int, int, int] = (8, 12, 16)
    grid_color: tuple[int, int, int] = (32, 45, 54)
    snake_head_color: tuple[int, int, int] = (89, 255, 155)
    snake_body_color: tuple[int, int, int] = (30, 178, 96)
    food_color: tuple[int, int, int] = (255, 87, 87)
    text_color: tuple[int, int, int] = (226, 236, 242)
    muted_text_color: tuple[int, int, int] = (139, 154, 164)
    panel_color: tuple[int, int, int] = (18, 26, 32)
    warning_color: tuple[int, int, int] = (255, 204, 102)
    hazard_warning_color: tuple[int, int, int] = (255, 204, 102)
    hazard_active_color: tuple[int, int, int] = (255, 77, 136)
    boss_color: tuple[int, int, int] = (122, 175, 255)

    @property
    def play_width(self) -> int:
        return self.grid_columns * self.cell_size

    @property
    def play_height(self) -> int:
        return self.grid_rows * self.cell_size

    @property
    def window_width(self) -> int:
        return self.play_width + self.side_panel_width

    @property
    def window_height(self) -> int:
        return self.play_height
