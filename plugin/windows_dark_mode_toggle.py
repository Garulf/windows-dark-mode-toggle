from os import path
from subprocess import Popen, PIPE

from flox import Flox
from helper import WinTheme


ICON_PATH = path.join(path.abspath(path.dirname(path.dirname(__file__))), "icon")
LIGHT_DARK_ICON = path.join(ICON_PATH, "light-dark.png")
DARK_ICON = path.join(ICON_PATH, "dark.png")
LIGHT_ICON = path.join(ICON_PATH, "light.png")


class WindowsDarkModeToggle(Flox):

    def __init__(self):
        self._wintheme = WinTheme()
        self.toggle_theme = self._wintheme.toggle_theme
        self.toggle_system_theme = self._wintheme.toggle_system_theme
        self.toggle_app_theme = self._wintheme.toggle_apps_theme
        super().__init__()

    def __getattr__(self, name):
       return self._wintheme.__getattribute__(name)

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
            method="dark_mode_off"
        )
        self.add_item(
            title="Force Dark Mode",
            subtitle="Toggles System theme to Dark mode.",
            icon=DARK_ICON,
            method="dark_mode_on"
        )

if __name__ == "__main__":
    WindowsDarkModeToggle()