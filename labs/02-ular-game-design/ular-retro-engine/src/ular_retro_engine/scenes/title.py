from __future__ import annotations

from ..input import ActionSnapshot
from ..scene import BaseScene, Renderer
from .lab import LabScene


class TitleScene(BaseScene):
    name = "title"

    def handle_input(self, actions: ActionSnapshot) -> None:
        if actions.pressed("confirm"):
            self.context.replace_scene(LabScene())
        elif actions.pressed("cancel"):
            self.context.quit_app()

    def draw(self, renderer: Renderer) -> None:
        renderer.clear(0)
        renderer.text(70, 48, "ULAR", 11)
        renderer.text(52, 62, "RETRO ENGINE", 7)
        renderer.text(48, 86, "Space/Enter: lab", 5)
        renderer.text(66, 98, "Esc: quit", 5)
        if self.context.debug_console.enabled:
            renderer.text(4, 4, "DEV", 10)
