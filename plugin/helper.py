import winreg as reg
import os

LIGHT = 1
DARK = 0

SUB_KEY_THEME_PERSONALIZE = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
REG_NAME_APP_THEME = "AppsUseLightTheme"
REG_NAME_SYSTEM_THEME = "SystemUsesLightTheme"

class WinTheme(object):

    def _set_reg_key(self, key, value):
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, SUB_KEY_THEME_PERSONALIZE, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(reg_key, key, 0, reg.REG_DWORD, value)
        reg.CloseKey(reg_key)
    
    def _get_reg_key(self, key):
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, SUB_KEY_THEME_PERSONALIZE, 0, reg.KEY_READ)
        value = reg.QueryValueEx(reg_key, key)[0]
        reg.CloseKey(reg_key)
        return value

    def get_apps_theme(self):
        value = self._get_reg_key(REG_NAME_APP_THEME)
        if value == LIGHT:
            return True
        else:
            return False

    def get_system_theme(self):
        value = self._get_reg_key(REG_NAME_SYSTEM_THEME)
        if value == LIGHT:
            return True
        else:
            return False

    def _set_system_theme(self, value):
        self._set_reg_key(REG_NAME_SYSTEM_THEME, value)

    def _set_app_theme(self, value):
        self._set_reg_key(REG_NAME_APP_THEME, value)

    def toggle_apps_theme(self):
        if self.get_apps_theme():
            self._set_app_theme(DARK)
        else:
            self._set_app_theme(LIGHT)

    def toggle_system_theme(self):
        if self.get_system_theme():
            self._set_system_theme(DARK)
        else:
            self._set_system_theme(LIGHT)

    def set_dark_mode(self):
        self._set_system_theme(DARK)
        self._set_app_theme(DARK)
        self.restart_explorer()

    def set_light_mode(self):
        self._set_system_theme(LIGHT)
        self._set_app_theme(LIGHT)
        self.restart_explorer()

    def toggle_theme(self):
        if self.get_system_theme() or self.get_apps_theme():
            self.set_dark_mode()
        else:
            self.set_light_mode()