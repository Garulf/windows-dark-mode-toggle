import winreg as reg
import ctypes

ON = 1
OFF = 0
SUBKEY = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"


class WinTheme(object):

    def get_apps_theme(self):
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, SUBKEY)
        value = reg.QueryValueEx(key, "AppsUseLightTheme")[0]
        if value == ON:
            return True
        else:
            return False

    def get_system_theme(self):
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, SUBKEY)
        value = reg.QueryValueEx(key, "SystemUsesLightTheme")[0]
        if value == ON:
            return True
        else:
            return False
 
    def _apply_changes(self):
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A
        SMTO_ABORTIFHUNG = 0x0002  # Prevent hanging
        TIMEOUT = 10
        ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "ImmersiveColorSet", SMTO_ABORTIFHUNG, TIMEOUT, None)

    def _set_system_theme(self, value):
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, SUBKEY, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(key, "SystemUsesLightTheme", 0, reg.REG_DWORD, value)
        reg.CloseKey(key)

    def _set_app_theme(self, value):
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(key, "AppsUseLightTheme", 0, reg.REG_DWORD, value)
        reg.CloseKey(key)
        self._apply_changes()

    def toggle_apps_theme(self):
        if self.get_apps_theme():
            self._set_app_theme(OFF)
        else:
            self._set_app_theme(ON)

    def toggle_system_theme(self):
        if self.get_system_theme():
            self._set_system_theme(OFF)
        else:
            self._set_system_theme(ON)
        self._apply_changes()

    def set_dark_mode(self):
        self._set_system_theme(OFF)
        self._set_app_theme(OFF)

    def set_light_mode(self):
        self._set_system_theme(ON)
        self._set_app_theme(ON)

    def toggle_theme(self):
        if self.get_system_theme() or self.get_apps_theme():
            self.set_dark_mode()
        else:
            self.set_light_mode()
