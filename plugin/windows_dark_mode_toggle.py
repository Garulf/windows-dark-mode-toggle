from os import path
from subprocess import Popen, PIPE

from flox import Flox



REG_PATH = r'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
ICON_PATH = path.join(path.abspath(path.dirname(path.dirname(__file__))), "icon")
LIGHT_DARK_ICON = path.join(ICON_PATH, "light-dark.png")
DARK_ICON = path.join(ICON_PATH, "dark.png")
LIGHT_ICON = path.join(ICON_PATH, "light.png")


class WindowsDarkModeToggle(Flox):

    def run_cmd(self, cmd):
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, creationflags=0x08000000)
        output, err = p.communicate()
        exit_code = p.wait()
        if exit_code != 0:
            self.logger.error(err)
        return output.decode('utf-8').strip()

    def get_theme_value(self, key):
        cmd = self.run_cmd(['powershell.exe', '-command', f'(Get-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name {key}).{key}'])
        if cmd == "0":
            return False
        else:
            return True        

    def system_uses_light_theme(self):
        return self.get_theme_value('SystemUsesLightTheme')

    def apps_use_light_theme(self):
        return self.get_theme_value('AppsUseLightTheme')

    def set_theme_state(self, key, value):
        self.run_cmd(['powershell.exe', '-command', f'Set-ItemProperty -Path {REG_PATH} -Name {key} -Value {value}'])

    def toggle_system_theme(self):
        if self.system_uses_light_theme():
            self.set_theme_state('SystemUsesLightTheme', '0')
        else:
            self.set_theme_state('SystemUsesLightTheme', '1')
    def toggle_app_theme(self):
        if self.apps_use_light_theme():
            self.set_theme_state('AppsUseLightTheme', '0')
        else:
            self.set_theme_state('AppsUseLightTheme', '1')

    def dark_mode_on(self):
        self.set_theme_state('SystemUsesLightTheme', '0')
        self.set_theme_state('AppsUseLightTheme', '0')

    def dark_mode_off(self):
        self.set_theme_state('SystemUsesLightTheme', '1')
        self.set_theme_state('AppsUseLightTheme', '1')

    def toggle_dark_mode(self):
        if self.system_uses_light_theme() or self.apps_use_light_theme():
            self.dark_mode_on()
        else:
            self.dark_mode_off()

    def query(self, query):
        self.logger.info(ICON_PATH)
        self.add_item(
            title="Toggle Dark Mode",
            subtitle="Toggles System theme between Dark & Light.",
            icon=LIGHT_DARK_ICON,
            method="toggle_dark_mode"
        )

    def context_menu(self, data):
        self.add_item(
            title="Toggle Application theme",
            subtitle="Toggles Application theme between Light & Dark modes.",
            icon=LIGHT_DARK_ICON,
            method="toggle_app_theme"
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