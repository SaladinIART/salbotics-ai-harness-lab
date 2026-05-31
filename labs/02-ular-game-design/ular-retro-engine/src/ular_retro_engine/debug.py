from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DebugConsole:
    enabled: bool = False

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        return self.enabled
