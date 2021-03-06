from os import path
from subprocess import Popen, PIPE

from flox import Flox
from helper import WinTheme


ICON_PATH = path.join(path.abspath(path.dirname(path.dirname(__file__))), "icon")
LIGHT_DARK_ICON = path.join(ICON_PATH, "light-dark.png")
DARK_ICON = path.join(ICON_PATH, "dark.png")
LIGHT_ICON = path.join(ICON_PATH, "light.png")


class WindowsDarkModeToggle(Flox, WinTheme):

    def query(self, query):
        self.logger.info(ICON_PATH)
        self.add_item(
            title="Toggle Dark Mode",
            subtitle="Toggles System theme between Dark & Light.",
            icon=LIGHT_DARK_ICON,
            method="toggle_theme"
        )

    def context_menu(self, data):
        self.add_item(
            title="Toggle Application theme",
            subtitle="Toggles Application theme between Light & Dark modes.",
            icon=LIGHT_DARK_ICON,
            method="toggle_apps_theme"
        )
        self.add_item(
            title="Toggle System theme",
            subtitle="Toggles System theme between Light & Dark modes.",
            icon=LIGHT_DARK_ICON,
            method="toggle_system_theme"
        )           
        self.add_item(
            title="Force Light Mode",
            subtitle="Toggles System theme to Light mode.",
            icon=LIGHT_ICON,
            method="set_light_mode"
        )
        self.add_item(
            title="Force Dark Mode",
            subtitle="Toggles System theme to Dark mode.",
            icon=DARK_ICON,
            method="set_dark_mode"
        )

if __name__ == "__main__":
    WindowsDarkModeToggle()