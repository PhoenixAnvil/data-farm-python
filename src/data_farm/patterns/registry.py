from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from data_farm.patterns.base import Pattern


@dataclass(slots=True)
class PatternRegistry:
    patterns_dir: Path
    _cache: dict[str, Pattern] = field(default_factory=lambda: {})

    def get(self, pattern_name: str) -> Pattern:
        key = self._norm_key(pattern_name)
        if key in self._cache:
            return self._cache[key]

        pattern = self._load_pattern_file(key)
        self._cache[key] = pattern
        return pattern

    def exists(self, pattern_name: str) -> bool:
        key = self._norm_key(pattern_name)
        if key in self._cache:
            return True
        return self._pattern_path(key).exists()

    def _load_pattern_file(self, key: str) -> Pattern:
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

        return Pattern(classification=key, choices=values)

    def _pattern_path(self, key: str) -> Path:
        # Allows "emails" -> patterns/emails.txt
        return self.patterns_dir / f"{key}.pat"

    @staticmethod
    def _norm_key(name: str) -> str:
        return name.strip().lower().replace(" ", "_")
