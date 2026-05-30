from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .modules import RunModifiers

Point = tuple[int, int]


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def delta(self) -> Point:
        return self.value

    def is_opposite(self, other: "Direction") -> bool:
        return self.delta[0] + other.delta[0] == 0 and self.delta[1] + other.delta[1] == 0

    def opposite(self) -> "Direction":
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites[self]


class GamePhase(Enum):
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    REWARD = "reward"
    GAME_OVER = "game_over"
    WON = "won"


class HazardPhase(Enum):
    WARNING = "warning"
    ACTIVE = "active"


@dataclass
class Snake:
    body: list[Point]
    direction: Direction = Direction.RIGHT

    @property
    def head(self) -> Point:
        return self.body[0]


@dataclass(frozen=True)
class HazardPatch:
    cells: tuple[Point, ...]
    phase: HazardPhase = HazardPhase.WARNING
    ticks_remaining: int = 2


@dataclass
class BossState:
    name: str
    position: Point
    hp: int
    max_hp: int
    score_reward: int = 2


@dataclass(frozen=True)
class RewardChoice:
    reward_id: str
    name: str
    summary: str


@dataclass
class GameState:
    snake: Snake
    food: Point | None
    score: int = 0
    phase: GamePhase = GamePhase.READY
    ticks: int = 0
    loadout: dict[str, str] = field(default_factory=dict)
    modifiers: RunModifiers = field(default_factory=RunModifiers)
    shield_charges: int = 0
    growth_pending: int = 0
    hazards: list[HazardPatch] = field(default_factory=list)
    heat_level: int = 0
    boss: BossState | None = None
    boss_defeated: bool = False
    reward_choices: list[RewardChoice] = field(default_factory=list)
    rewards_taken: list[str] = field(default_factory=list)
    next_reward_score: int = 6
    status_message: str = "Choose loadout, then launch."
