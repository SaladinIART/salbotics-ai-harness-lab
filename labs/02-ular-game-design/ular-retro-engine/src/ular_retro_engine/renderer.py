from __future__ import annotations


class PyxelRenderer:
    def __init__(self, pyxel_api: object) -> None:
        self._pyxel = pyxel_api

    def clear(self, color: int) -> None:
        self._pyxel.cls(color)

    def rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        self._pyxel.rect(x, y, w, h, color)

    def rectb(self, x: int, y: int, w: int, h: int, color: int) -> None:
        self._pyxel.rectb(x, y, w, h, color)

    def text(self, x: int, y: int, value: str, color: int) -> None:
        self._pyxel.text(x, y, value, color)
