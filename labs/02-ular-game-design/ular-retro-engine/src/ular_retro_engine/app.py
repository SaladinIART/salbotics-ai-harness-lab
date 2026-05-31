from __future__ import annotations

from .config import AppConfig, default_config
from .content import ContentRegistry
from .debug import DebugConsole
from .input import InputMapper, default_bindings
from .profile import ProfileStore
from .renderer import PyxelRenderer
from .scene import Scene, SceneContext, SceneStack
from .scenes import TitleScene


class RetroApp:
    def __init__(self, config: AppConfig | None = None, pyxel_api: object | None = None) -> None:
        self.config = config or default_config()
        self.pyxel = pyxel_api
        self.profile_store = ProfileStore(self.config.saves_dir / self.config.profile_name)
        self.profile = self.profile_store.load()
        self.content_registry = ContentRegistry(self.config.content_dir)
        self.debug_console = DebugConsole(enabled=self.profile.developer_mode)
        self.scene_stack = SceneStack(self._make_context)
        self.input_mapper: InputMapper | None = None
        self.renderer: PyxelRenderer | None = None
        self.running = False

    def _make_context(self) -> SceneContext:
        return SceneContext(
            replace_scene=self.replace_scene,
            push_scene=self.push_scene,
            pop_scene=self.pop_scene,
            quit_app=self.quit,
            profile=self.profile,
            profile_store=self.profile_store,
            content_registry=self.content_registry,
            debug_console=self.debug_console,
        )

    def boot(self) -> None:
        self.scene_stack.push(TitleScene())

    def push_scene(self, scene: Scene) -> None:
        self.scene_stack.push(scene)

    def pop_scene(self) -> None:
        self.scene_stack.pop()
        if self.scene_stack.active is None:
            self.quit()

    def replace_scene(self, scene: Scene) -> None:
        self.scene_stack.replace(scene)

    def quit(self) -> None:
        self.running = False
        if self.pyxel is not None and hasattr(self.pyxel, "quit"):
            self.pyxel.quit()

    def run(self) -> None:
        try:
            import pyxel
        except ImportError as exc:
            raise SystemExit(
                "Pyxel is not installed. Run install_and_run.bat or "
                "python -m pip install -r requirements.txt."
            ) from exc

        self.pyxel = pyxel
        self.input_mapper = InputMapper(default_bindings(pyxel))
        self.renderer = PyxelRenderer(pyxel)
        pyxel.init(
            self.config.width,
            self.config.height,
            title=self.config.title,
            fps=self.config.fps,
            quit_key=pyxel.KEY_NONE,
            display_scale=self.config.display_scale,
        )
        self.running = True
        self.boot()
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        if self.pyxel is None or self.input_mapper is None:
            return

        actions = self.input_mapper.snapshot(self.pyxel)
        if actions.pressed("debug_toggle"):
            self.profile.developer_mode = self.debug_console.toggle()
            self.profile_store.save(self.profile)

        active = self.scene_stack.active
        if active is None:
            self.quit()
            return

        active.handle_input(actions)
        active.update(1)

    def draw(self) -> None:
        if self.renderer is None:
            return
        active = self.scene_stack.active
        if active is None:
            return
        active.draw(self.renderer)


def main() -> None:
    RetroApp().run()
