from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

from .input import ActionSnapshot


class Renderer(Protocol):
    def clear(self, color: int) -> None:
        ...

    def rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        ...

    def rectb(self, x: int, y: int, w: int, h: int, color: int) -> None:
        ...

    def text(self, x: int, y: int, value: str, color: int) -> None:
        ...


@dataclass(frozen=True)
class SceneContext:
    replace_scene: Callable[["Scene"], None]
    push_scene: Callable[["Scene"], None]
    pop_scene: Callable[[], None]
    quit_app: Callable[[], None]
    profile: object
    profile_store: object
    content_registry: object
    debug_console: object


class Scene(Protocol):
    name: str

    def enter(self, context: SceneContext) -> None:
        ...

    def handle_input(self, actions: ActionSnapshot) -> None:
        ...

    def update(self, dt_ticks: int) -> None:
        ...

    def draw(self, renderer: Renderer) -> None:
        ...

    def exit(self) -> None:
        ...


class BaseScene:
    name = "base"

    def enter(self, context: SceneContext) -> None:
        self.context = context

    def handle_input(self, actions: ActionSnapshot) -> None:
        return None

    def update(self, dt_ticks: int) -> None:
        return None

    def draw(self, renderer: Renderer) -> None:
        return None

    def exit(self) -> None:
        return None


class SceneStack:
    def __init__(self, context_factory: Callable[[], SceneContext]) -> None:
        self._context_factory = context_factory
        self._scenes: list[Scene] = []

    @property
    def active(self) -> Scene | None:
        if not self._scenes:
            return None
        return self._scenes[-1]

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(scene.name for scene in self._scenes)

    def push(self, scene: Scene) -> None:
        self._scenes.append(scene)
        scene.enter(self._context_factory())

    def pop(self) -> Scene | None:
        if not self._scenes:
            return None
        scene = self._scenes.pop()
        scene.exit()
        return scene

    def replace(self, scene: Scene) -> None:
        self.pop()
        self.push(scene)
