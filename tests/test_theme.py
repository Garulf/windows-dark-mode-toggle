import pytest

from conftest import FakeRegistry
from theme import APPS, DARK, LIGHT, PERSONALIZE_KEY, SYSTEM, Theme, WindowsRegistry


@pytest.mark.parametrize(
    "system, apps, expected",
    [
        (LIGHT, LIGHT, DARK),
        (LIGHT, DARK, DARK),
        (DARK, LIGHT, DARK),
        (DARK, DARK, LIGHT),
    ],
)
def test_toggle_goes_dark_if_anything_is_light(system, apps, expected):
    registry = FakeRegistry(system=system, apps=apps)

    Theme(registry).toggle()

    assert registry.writes == [(SYSTEM, expected), (APPS, expected)]


@pytest.mark.parametrize("current, expected", [(LIGHT, DARK), (DARK, LIGHT)])
def test_toggle_apps_only_touches_apps(current, expected):
    registry = FakeRegistry(system=LIGHT, apps=current)

    Theme(registry).toggle_apps()

    assert registry.writes == [(APPS, expected)]


@pytest.mark.parametrize("current, expected", [(LIGHT, DARK), (DARK, LIGHT)])
def test_toggle_system_only_touches_system(current, expected):
    registry = FakeRegistry(system=current, apps=LIGHT)

    Theme(registry).toggle_system()

    assert registry.writes == [(SYSTEM, expected)]


def test_set_dark_and_light_write_both_values():
    registry = FakeRegistry()
    theme = Theme(registry)

    theme.set_dark()
    theme.set_light()

    assert registry.writes == [(SYSTEM, DARK), (APPS, DARK), (SYSTEM, LIGHT), (APPS, LIGHT)]


def test_windows_registry_reads_personalize_key(fake_winreg):
    assert WindowsRegistry().read(SYSTEM) == 1
    assert WindowsRegistry().read(APPS) == 0

    assert fake_winreg.calls[:3] == [
        ("open", ("HKCU", PERSONALIZE_KEY)),
        ("query", SYSTEM),
        ("close", ("HKCU", PERSONALIZE_KEY)),
    ]


def test_windows_registry_reads_a_missing_value_as_light(fake_winreg, monkeypatch):
    monkeypatch.setattr(fake_winreg, "QueryValueEx", missing_value)

    assert WindowsRegistry().read(APPS) == LIGHT


def missing_value(key, name):
    raise FileNotFoundError(2, "The system cannot find the file specified")


def test_windows_registry_writes_dword_to_personalize_key(fake_winreg):
    WindowsRegistry().write(APPS, 1)

    key = ("HKCU", PERSONALIZE_KEY, 0, "KEY_ALL_ACCESS")
    assert fake_winreg.calls == [
        ("open", key),
        ("set", "AppsUseLightTheme", 0, "REG_DWORD", 1),
        ("close", key),
    ]


def test_personalize_key_is_unchanged():
    assert PERSONALIZE_KEY == r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    assert (SYSTEM, APPS) == ("SystemUsesLightTheme", "AppsUseLightTheme")
    assert (LIGHT, DARK) == (1, 0)
