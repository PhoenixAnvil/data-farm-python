from __future__ import annotations

from pathlib import Path

from data_farm.l1_application.ports.pattern_source import PatternSource
from data_farm.l1_application.ports.pattern_source_factory import PatternSourceFactory
from data_farm.l2_interface_adapters.patterns.filesystem_pattern_source import FilesystemPatternSource


class FilesystemPatternSourceFactory(PatternSourceFactory):
    def create(self, patterns_dir: Path) -> PatternSource:
        return FilesystemPatternSource(patterns_dir=patterns_dir)
