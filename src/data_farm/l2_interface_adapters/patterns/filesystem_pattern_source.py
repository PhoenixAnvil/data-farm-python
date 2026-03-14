from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from data_farm.l1_application.ports.pattern_source import PatternSource


@dataclass(slots=True)
class FilesystemPatternSource(PatternSource):
    patterns_dir: Path
    _cache: dict[str, list[str]] = field(default_factory=lambda: {})

    def get_choices(self, pattern_name: str) -> list[str]:
        key = self._norm_key(pattern_name)
        if key in self._cache:
            return self._cache[key]

        choices = self._load_pattern_file(key)
        self._cache[key] = choices
        return choices

    def exists(self, pattern_name: str) -> bool:
        key = self._norm_key(pattern_name)
        if key in self._cache:
            return True
        return self._pattern_path(key).exists()

    def _load_pattern_file(self, key: str) -> list[str]:
        path = self._pattern_path(key)
        if not path.exists():
            raise FileNotFoundError(f"Pattern file not found: {path}")

        values: list[str] = []
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            v = line.strip()
            if not v:
                continue
            if v.startswith("#"):
                continue
            values.append(v)

        if not values:
            raise ValueError(f"Pattern file is empty: {path}")

        return values

    def _pattern_path(self, key: str) -> Path:
        # Allows "emails" -> patterns/emails.txt
        return self.patterns_dir / f"{key}.pat"

    @staticmethod
    def _norm_key(name: str) -> str:
        return name.strip().lower().replace(" ", "_")
