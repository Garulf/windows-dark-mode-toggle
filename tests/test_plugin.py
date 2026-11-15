import json
from pathlib import Path

import pytest

from theme import APPS, DARK, LIGHT, SYSTEM

ROOT = Path(__file__).resolve().parents[1]


def results(response):
    return json.loads(json.dumps(response["Result"]))


def test_query_offers_one_toggle(call):
    (result,) = results(call("query", "anything"))

    assert result["Title"] == "Toggle Dark Mode"
    assert result["JsonRPCAction"]["Method"] == "toggle_theme"
    assert Path(result["IcoPath"]).is_file()


def test_context_menu_lists_actions_in_order(call):
    menu = results(call("context_menu", None))

    assert [(r["Title"], r["JsonRPCAction"]["Method"]) for r in menu] == [
        ("Toggle Application theme", "toggle_apps_theme"),
        ("Toggle System theme", "toggle_system_theme"),
        ("Force Light Mode", "set_light_mode"),
        ("Force Dark Mode", "set_dark_mode"),
    ]
    assert all(Path(r["IcoPath"]).is_file() for r in menu)


@pytest.mark.parametrize(
    "method, writes",
    [
        ("toggle_theme", [(SYSTEM, DARK), (APPS, DARK)]),
        ("toggle_apps_theme", [(APPS, DARK)]),
        ("toggle_system_theme", [(SYSTEM, DARK)]),
        ("set_light_mode", [(SYSTEM, LIGHT), (APPS, LIGHT)]),
        ("set_dark_mode", [(SYSTEM, DARK), (APPS, DARK)]),
    ],
)
def test_actions_write_the_registry(call, registry, method, writes):
    call(method)

    assert registry.writes == writes


def test_manifest_keeps_store_identity():
    manifest = json.loads((ROOT / "data" / "plugin.json").read_text(encoding="utf-8"))

    assert manifest["ID"] == "4F31D5DF26984581BDF4213D40860ADF"
    assert manifest["ActionKeyword"] == "wt"
    assert manifest["Language"] == "python_v2"
