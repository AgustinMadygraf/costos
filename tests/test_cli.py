import os

import pytest

import src.cli as cli


def test_run_cli_default_ejecuta_equilibrio(monkeypatch):
    called = {"equilibrio": 0, "mix": 0}

    def _equilibrio():
        called["equilibrio"] += 1

    def _mix():
        called["mix"] += 1

    monkeypatch.setattr(cli, "equilibrio_main", _equilibrio)
    monkeypatch.setattr(cli, "mix_main", _mix)

    old_level = os.environ.get("LOG_LEVEL")
    code = cli.run_cli([])
    if old_level is None:
        os.environ.pop("LOG_LEVEL", None)
    else:
        os.environ["LOG_LEVEL"] = old_level
    assert code == 0
    assert called["equilibrio"] == 1
    assert called["mix"] == 0


def test_run_cli_mix_ejecuta_mix(monkeypatch):
    called = {"equilibrio": 0, "mix": 0}

    def _equilibrio():
        called["equilibrio"] += 1

    def _mix():
        called["mix"] += 1

    monkeypatch.setattr(cli, "equilibrio_main", _equilibrio)
    monkeypatch.setattr(cli, "mix_main", _mix)

    old_level = os.environ.get("LOG_LEVEL")
    code = cli.run_cli(["mix"])
    if old_level is None:
        os.environ.pop("LOG_LEVEL", None)
    else:
        os.environ["LOG_LEVEL"] = old_level
    assert code == 0
    assert called["equilibrio"] == 0
    assert called["mix"] == 1


def test_run_cli_debug_setea_log_level(monkeypatch):
    monkeypatch.setattr(cli, "equilibrio_main", lambda: None)
    old_level = os.environ.get("LOG_LEVEL")
    code = cli.run_cli(["--debug"])
    assert code == 0
    assert os.environ["LOG_LEVEL"] == "DEBUG"
    if old_level is None:
        os.environ.pop("LOG_LEVEL", None)
    else:
        os.environ["LOG_LEVEL"] = old_level


def test_cli_help_devuelve_system_exit():
    with pytest.raises(SystemExit) as exc:
        cli.run_cli(["--help"])
    assert exc.value.code == 0
