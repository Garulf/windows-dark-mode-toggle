import asyncio
import sys
import types

import pytest

import toggle
from theme import APPS, SYSTEM, Theme


class FakeRegistry:
    def __init__(self, system=1, apps=1):
        self.values = {SYSTEM: system, APPS: apps}
        self.writes = []

    def read(self, name):
        return self.values[name]

    def write(self, name, value):
        self.writes.append((name, value))
        self.values[name] = value


class FakeKey:
    def __init__(self, calls, args):
        self.calls = calls
        self.args = args

    def __enter__(self):
        self.calls.append(("open", self.args))
        return self

    def __exit__(self, *exc):
        self.calls.append(("close", self.args))


def make_fake_winreg(values):
    calls = []
    winreg = types.ModuleType("winreg")
    winreg.HKEY_CURRENT_USER = "HKCU"
    winreg.KEY_ALL_ACCESS = "KEY_ALL_ACCESS"
    winreg.REG_DWORD = "REG_DWORD"
    winreg.calls = calls

    def open_key(*args):
        return FakeKey(calls, args)

    def query_value_ex(key, name):
        calls.append(("query", name))
        return values[name], winreg.REG_DWORD

    def set_value_ex(key, name, reserved, kind, value):
        calls.append(("set", name, reserved, kind, value))
        values[name] = value

    winreg.OpenKey = open_key
    winreg.QueryValueEx = query_value_ex
    winreg.SetValueEx = set_value_ex
    return winreg


@pytest.fixture
def fake_winreg(monkeypatch):
    winreg = make_fake_winreg({SYSTEM: 1, APPS: 0})
    monkeypatch.setitem(sys.modules, "winreg", winreg)
    return winreg


@pytest.fixture
def registry(monkeypatch):
    fake = FakeRegistry()
    monkeypatch.setattr(toggle, "theme", lambda: Theme(fake))
    return fake


@pytest.fixture
def call():
    def call(method, *params):
        return asyncio.run(toggle.plugin._event_handler.trigger_event(method, *params))

    return call
