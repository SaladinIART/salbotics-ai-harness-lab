from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ular_retro_engine import __version__
from ular_retro_engine.app import RetroApp
from ular_retro_engine.config import AppConfig, default_config
from ular_retro_engine.content import ContentRegistry
from ular_retro_engine.input import InputMapper
from ular_retro_engine.profile import Profile, ProfileStore
from ular_retro_engine.scene import BaseScene, SceneContext, SceneStack


class FakeButtonApi:
    KEY_UP = 1
    KEY_W = 2
    KEY_SPACE = 3
    KEY_F1 = 4

    def __init__(self, pressed: set[int] | None = None, held: set[int] | None = None) -> None:
        self._pressed = pressed or set()
        self._held = held or set()

    def btnp(self, key: int) -> bool:
        return key in self._pressed

    def btn(self, key: int) -> bool:
        return key in self._held


class DummyScene(BaseScene):
    def __init__(self, name: str) -> None:
        self.name = name
        self.entered = False
        self.exited = False

    def enter(self, context: SceneContext) -> None:
        super().enter(context)
        self.entered = True

    def exit(self) -> None:
        self.exited = True


class Cp7ScaffoldTests(unittest.TestCase):
    def test_package_imports(self) -> None:
        self.assertEqual(__version__, "0.1.0")

    def test_default_config_resolves_project_dirs(self) -> None:
        config = default_config()
        self.assertEqual(config.content_dir.name, "content")
        self.assertEqual(config.saves_dir.name, "saves")
        self.assertEqual(config.width, 240)
        self.assertEqual(config.height, 160)

    def test_content_registry_resolves_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "content"
            registry = ContentRegistry(root)

            self.assertEqual(registry.resolve("modules.json"), root / "modules.json")

    def test_scene_stack_push_pop_replace(self) -> None:
        context = SceneContext(
            replace_scene=lambda scene: None,
            push_scene=lambda scene: None,
            pop_scene=lambda: None,
            quit_app=lambda: None,
            profile=object(),
            profile_store=object(),
            content_registry=object(),
            debug_console=object(),
        )
        stack = SceneStack(lambda: context)
        title = DummyScene("title")
        play = DummyScene("play")

        stack.push(title)
        self.assertEqual(stack.names, ("title",))
        self.assertTrue(title.entered)

        stack.replace(play)
        self.assertTrue(title.exited)
        self.assertEqual(stack.names, ("play",))
        self.assertTrue(play.entered)

        popped = stack.pop()
        self.assertIs(popped, play)
        self.assertEqual(stack.names, ())
        self.assertTrue(play.exited)

    def test_input_mapper_creates_action_snapshot(self) -> None:
        mapper = InputMapper(
            {
                "move_up": (FakeButtonApi.KEY_UP, FakeButtonApi.KEY_W),
                "confirm": (FakeButtonApi.KEY_SPACE,),
                "debug_toggle": (FakeButtonApi.KEY_F1,),
            }
        )
        api = FakeButtonApi(
            pressed={FakeButtonApi.KEY_SPACE, FakeButtonApi.KEY_F1},
            held={FakeButtonApi.KEY_UP},
        )

        snapshot = mapper.snapshot(api)

        self.assertTrue(snapshot.held("move_up"))
        self.assertTrue(snapshot.pressed("confirm"))
        self.assertTrue(snapshot.pressed("debug_toggle"))
        self.assertFalse(snapshot.pressed("move_up"))

    def test_profile_store_creates_default_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = ProfileStore(Path(tmp) / "profile.json")

            profile = store.load()

            self.assertIsInstance(profile, Profile)
            self.assertEqual(profile.version, 1)
            self.assertEqual(profile.snake_speed_fps, 8)
            self.assertTrue(store.path.exists())

    def test_retro_app_boots_to_title_scene_without_pyxel_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = AppConfig(
                content_dir=root / "content",
                saves_dir=root / "saves",
            )
            app = RetroApp(config=config, pyxel_api=None)

            app.boot()

            self.assertEqual(app.scene_stack.names, ("title",))
            self.assertTrue((root / "saves" / "profile.json").exists())


if __name__ == "__main__":
    unittest.main()
