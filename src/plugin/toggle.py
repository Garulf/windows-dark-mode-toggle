from __future__ import annotations

from pathlib import Path
from typing import List

from pyflowlauncher import FlowLauncherV2, Plugin, Result

from theme import Theme, WindowsRegistry

ICONS = Path(__file__).resolve().parent / "icons"
TOGGLE_ICON = ICONS / "light-dark.png"
LIGHT_ICON = ICONS / "light.png"
DARK_ICON = ICONS / "dark.png"

plugin = Plugin(launcher=FlowLauncherV2())


def theme() -> Theme:
    return Theme(WindowsRegistry())


@plugin.on_method
def toggle_theme() -> None:
    theme().toggle()


@plugin.on_method
def toggle_apps_theme() -> None:
    theme().toggle_apps()


@plugin.on_method
def toggle_system_theme() -> None:
    theme().toggle_system()


@plugin.on_method
def set_light_mode() -> None:
    theme().set_light()


@plugin.on_method
def set_dark_mode() -> None:
    theme().set_dark()


@plugin.on_method
def query(query: str) -> Result:
    return Result(
        title="Toggle Dark Mode",
        subtitle="Toggles System theme between Dark & Light.",
        icon=TOGGLE_ICON,
    ).add_action(toggle_theme)


def context_menu(context_data=None) -> List[Result]:
    return [
        Result(
            title="Toggle Application theme",
            subtitle="Toggles Application theme between Light & Dark modes.",
            icon=TOGGLE_ICON,
        ).add_action(toggle_apps_theme),
        Result(
            title="Toggle System theme",
            subtitle="Toggles System theme between Light & Dark modes.",
            icon=TOGGLE_ICON,
        ).add_action(toggle_system_theme),
        Result(
            title="Force Light Mode",
            subtitle="Toggles System theme to Light mode.",
            icon=LIGHT_ICON,
        ).add_action(set_light_mode),
        Result(
            title="Force Dark Mode",
            subtitle="Toggles System theme to Dark mode.",
            icon=DARK_ICON,
        ).add_action(set_dark_mode),
    ]


plugin.add_method(context_menu, name="context_menu")
