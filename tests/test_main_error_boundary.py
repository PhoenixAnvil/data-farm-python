from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pytest import MonkeyPatch

import data_farm.cli.main as df_main


@dataclass
class FakeArgs:
    pass


class FakeParser:
    def parse_args(self, args: list[str] | None = None) -> FakeArgs:
        return FakeArgs()


def _noop_dispatch(_parser: Any, _args: Any) -> int:
    return 0


def _boom_dispatch(_parser: Any, _args: Any) -> None:
    raise RuntimeError("boom")


def _fake_build_parser() -> FakeParser:
    return FakeParser()


def test_main_returns_int_on_success(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(df_main, "build_parser", _fake_build_parser)
    monkeypatch.setattr(df_main, "dispatch", _noop_dispatch)
    assert df_main.main([]) == 0


def test_main_unhandled_exception_returns_nonzero(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(df_main, "build_parser", _fake_build_parser)
    monkeypatch.setattr(df_main, "dispatch", _boom_dispatch)
    assert df_main.main([]) != 0
