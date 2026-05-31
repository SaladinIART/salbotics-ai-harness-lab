from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol


class ButtonApi(Protocol):
    def btn(self, key: int) -> bool:
        ...

    def btnp(self, key: int) -> bool:
        ...


@dataclass(frozen=True)
class ActionSnapshot:
    pressed_actions: frozenset[str]
    held_actions: frozenset[str]

    def pressed(self, action: str) -> bool:
        return action in self.pressed_actions

    def held(self, action: str) -> bool:
        return action in self.held_actions


class InputMapper:
    def __init__(self, bindings: Mapping[str, tuple[int, ...]]) -> None:
        self.bindings = dict(bindings)

    def snapshot(self, api: ButtonApi) -> ActionSnapshot:
        pressed = {
            action
            for action, keys in self.bindings.items()
            if any(api.btnp(key) for key in keys)
        }
        held = {
            action
            for action, keys in self.bindings.items()
            if any(api.btn(key) for key in keys)
        }
        return ActionSnapshot(frozenset(pressed), frozenset(held))


def default_bindings(pyxel_api: object) -> dict[str, tuple[int, ...]]:
    def key(*names: str) -> int:
        for name in names:
            if hasattr(pyxel_api, name):
                return getattr(pyxel_api, name)
        raise AttributeError(f"Pyxel key constant missing: {'/'.join(names)}")

    return {
        "move_up": (key("KEY_UP"), key("KEY_W")),
        "move_down": (key("KEY_DOWN"), key("KEY_S")),
        "move_left": (key("KEY_LEFT"), key("KEY_A")),
        "move_right": (key("KEY_RIGHT"), key("KEY_D")),
        "confirm": (key("KEY_SPACE"), key("KEY_RETURN", "KEY_ENTER")),
        "cancel": (key("KEY_ESCAPE"), key("KEY_X")),
        "pause": (key("KEY_P"),),
        "cycle_left": (key("KEY_LEFT"), key("KEY_A")),
        "cycle_right": (key("KEY_RIGHT"), key("KEY_D")),
        "speed_down": (key("KEY_LEFT_BRACKET", "KEY_LEFTBRACKET"), key("KEY_MINUS")),
        "speed_up": (key("KEY_RIGHT_BRACKET", "KEY_RIGHTBRACKET"), key("KEY_EQUAL", "KEY_EQUALS")),
        "debug_toggle": (key("KEY_F1"),),
        "reward_1": (key("KEY_1"),),
        "reward_2": (key("KEY_2"),),
        "reward_3": (key("KEY_3"),),
        "debug_boss": (key("KEY_B"),),
        "debug_hazard": (key("KEY_H"),),
        "debug_score": (key("KEY_G"),),
        "debug_reward": (key("KEY_R"),),
        "debug_shield": (key("KEY_V"),),
        "debug_clear": (key("KEY_C"),),
        "buy_unlock": (key("KEY_U"),),
    }
