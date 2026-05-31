from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum

from .modules import LoadoutStats


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def vector(self) -> tuple[int, int]:
        return self.value

    def is_opposite(self, other: "Direction") -> bool:
        dx, dy = self.vector
        odx, ody = other.vector
        return dx + odx == 0 and dy + ody == 0


@dataclass(frozen=True, order=True)
class Cell:
    x: int
    y: int

    def moved(self, direction: Direction) -> "Cell":
        dx, dy = direction.vector
        return Cell(self.x + dx, self.y + dy)


@dataclass
class Hazard:
    cell: Cell
    phase: str = "warning"
    ticks: int = 5


@dataclass
class BossState:
    active: bool = False
    hp: int = 3
    target: Cell | None = None
    cooldown: int = 0
    defeated: bool = False


@dataclass
class RewardChoice:
    id: str
    label: str
    effect: str
    amount: int


REWARD_POOL = (
    RewardChoice("shield", "Shield +1", "shield", 1),
    RewardChoice("scrap", "Scrap +5", "bonus_scrap", 5),
    RewardChoice("coolant", "Heat -3", "heat", -3),
    RewardChoice("score", "Score +2", "score", 2),
)


@dataclass
class RunState:
    width: int = 20
    height: int = 16
    seed: int = 1
    loadout: LoadoutStats = field(default_factory=LoadoutStats)
    snake: list[Cell] = field(default_factory=list)
    direction: Direction = Direction.RIGHT
    pending_direction: Direction = Direction.RIGHT
    food: Cell | None = None
    score: int = 0
    length_target: int = 4
    phase: str = "active"
    heat: int = 0
    shield: int = 0
    scrap_preview: int = 0
    bonus_scrap: int = 0
    hazards: list[Hazard] = field(default_factory=list)
    boss: BossState = field(default_factory=BossState)
    reward_choices: list[RewardChoice] = field(default_factory=list)
    next_reward_score: int = 5

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        self.length_target = self.loadout.starting_length
        self.shield = self.loadout.shield
        if not self.snake:
            center = Cell(self.width // 2, self.height // 2)
            self.snake = [Cell(center.x - i, center.y) for i in range(self.length_target)]
        if self.food is None:
            self.food = self.spawn_food()

    @property
    def head(self) -> Cell:
        return self.snake[0]

    def set_direction(self, direction: Direction) -> None:
        if not direction.is_opposite(self.direction):
            self.pending_direction = direction

    def restart(self, seed: int | None = None) -> None:
        new_state = RunState(
            width=self.width,
            height=self.height,
            seed=self.seed + 1 if seed is None else seed,
            loadout=self.loadout,
        )
        self.__dict__.update(new_state.__dict__)

    def step(self) -> None:
        if self.phase != "active":
            return

        self._tick_pressure()
        self.direction = self.pending_direction
        next_head = self.head.moved(self.direction)
        will_eat = next_head == self.food

        if not self.in_bounds(next_head):
            self._take_hit()
            return

        body_to_check = self.snake if will_eat else self.snake[:-1]
        if next_head in body_to_check:
            self._take_hit()
            return

        active_hazard = self._active_hazard_at(next_head)
        if active_hazard is not None:
            self.snake.insert(0, next_head)
            self._take_hit()
            return

        self.snake.insert(0, next_head)
        self._check_boss_hit(next_head)

        if will_eat:
            self.score += self.loadout.score_per_food
            self.length_target += 1
            self.food = self.spawn_food()

        while len(self.snake) > self.length_target:
            self.snake.pop()

        if self.food is None:
            self.phase = "cleared"
        elif self.score >= self.next_reward_score:
            self.open_reward()
            self.next_reward_score += 5
        elif self.score >= 8 and not self.boss.active and not self.boss.defeated:
            self.spawn_boss()

    def choose_reward(self, index: int) -> None:
        if self.phase != "reward" or index >= len(self.reward_choices):
            return
        reward = self.reward_choices[index]
        if reward.effect == "shield":
            self.shield += reward.amount
        elif reward.effect == "bonus_scrap":
            self.bonus_scrap += reward.amount
        elif reward.effect == "heat":
            self.heat = max(0, self.heat + reward.amount)
        elif reward.effect == "score":
            self.score += reward.amount
        self.reward_choices = []
        self.phase = "active"

    def open_reward(self) -> None:
        self.reward_choices = list(self.rng.sample(REWARD_POOL, 3))
        self.phase = "reward"

    def spawn_hazard(self) -> None:
        cell = self._random_safe_cell()
        if cell is not None:
            self.hazards.append(Hazard(cell=cell))

    def clear_hazards(self) -> None:
        self.hazards.clear()

    def spawn_boss(self) -> None:
        self.boss.active = True
        self.boss.hp = 3
        self.boss.target = self._random_safe_cell()
        self.boss.cooldown = 3
        if self.boss.target is None:
            self.boss.active = False

    def in_bounds(self, cell: Cell) -> bool:
        return 0 <= cell.x < self.width and 0 <= cell.y < self.height

    def spawn_food(self) -> Cell | None:
        occupied = self._occupied()
        available = [
            Cell(x, y)
            for y in range(self.height)
            for x in range(self.width)
            if Cell(x, y) not in occupied
        ]
        if not available:
            return None
        return self.rng.choice(available)

    def finish_scrap(self) -> int:
        return self.score * self.loadout.scrap_multiplier + self.bonus_scrap

    def _tick_pressure(self) -> None:
        self.heat = max(0, self.heat + 1 + self.loadout.heat_rate_delta)
        if self.heat > 0 and self.heat % 12 == 0:
            self.spawn_hazard()
        self._tick_hazards()
        self._tick_boss()

    def _tick_hazards(self) -> None:
        survivors: list[Hazard] = []
        for hazard in self.hazards:
            hazard.ticks -= 1
            if hazard.ticks <= 0 and hazard.phase == "warning":
                hazard.phase = "active"
                hazard.ticks = 6
            elif hazard.ticks <= 0:
                continue
            survivors.append(hazard)
        self.hazards = survivors

    def _tick_boss(self) -> None:
        if not self.boss.active:
            return
        self.boss.cooldown -= 1
        if self.boss.cooldown <= 0:
            self.spawn_hazard()
            self.boss.cooldown = 4

    def _check_boss_hit(self, head: Cell) -> None:
        if not self.boss.active or self.boss.target != head:
            return
        self.boss.hp -= 1
        if self.boss.hp <= 0:
            self.boss.active = False
            self.boss.defeated = True
            self.bonus_scrap += 10
            self.open_reward()
        else:
            self.boss.target = self._random_safe_cell()

    def _take_hit(self) -> None:
        if self.shield > 0:
            self.shield -= 1
            if len(self.snake) > self.length_target:
                self.snake.pop()
            return
        self.phase = "game_over"

    def _active_hazard_at(self, cell: Cell) -> Hazard | None:
        for hazard in self.hazards:
            if hazard.cell == cell and hazard.phase == "active":
                return hazard
        return None

    def _random_safe_cell(self) -> Cell | None:
        occupied = self._occupied()
        available = [
            Cell(x, y)
            for y in range(self.height)
            for x in range(self.width)
            if Cell(x, y) not in occupied
        ]
        if not available:
            return None
        return self.rng.choice(available)

    def _occupied(self) -> set[Cell]:
        occupied = set(self.snake)
        if self.food is not None:
            occupied.add(self.food)
        for hazard in self.hazards:
            occupied.add(hazard.cell)
        if self.boss.target is not None:
            occupied.add(self.boss.target)
        return occupied
