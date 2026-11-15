from __future__ import annotations

from typing import Protocol

PERSONALIZE_KEY = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
APPS = "AppsUseLightTheme"
SYSTEM = "SystemUsesLightTheme"
LIGHT = 1
DARK = 0


class Registry(Protocol):
    def read(self, name: str) -> int: ...

    def write(self, name: str, value: int) -> None: ...


class WindowsRegistry:
    def read(self, name: str) -> int:
        import winreg

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, PERSONALIZE_KEY) as key:
                return winreg.QueryValueEx(key, name)[0]
        except FileNotFoundError:
            return LIGHT

    def write(self, name: str, value: int) -> None:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, PERSONALIZE_KEY, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)


class Theme:
    def __init__(self, registry: Registry) -> None:
        self._registry = registry

    def is_light(self, name: str) -> bool:
        return self._registry.read(name) == LIGHT

    def toggle(self) -> None:
        if self.is_light(SYSTEM) or self.is_light(APPS):
            self.set_dark()
        else:
            self.set_light()

    def toggle_apps(self) -> None:
        self._flip(APPS)

    def toggle_system(self) -> None:
        self._flip(SYSTEM)

    def set_dark(self) -> None:
        self._write_all(DARK)

    def set_light(self) -> None:
        self._write_all(LIGHT)

    def _flip(self, name: str) -> None:
        self._registry.write(name, DARK if self.is_light(name) else LIGHT)

    def _write_all(self, value: int) -> None:
        self._registry.write(SYSTEM, value)
        self._registry.write(APPS, value)
