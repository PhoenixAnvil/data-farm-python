""" """

from __future__ import annotations

import hashlib
import random
from collections.abc import Sequence, Set
from typing import TypeVar, overload

T = TypeVar("T")


def random_int(rng: random.Random, min_value: int, max_value: int) -> int:
    return rng.randint(min_value, max_value)


def random_choice(rng: random.Random, collection: Sequence[T] | Set[T]) -> T:
    if isinstance(collection, set):
        # Convert because sets aren't indexable.
        return rng.choice(tuple(collection))

    return rng.choice(collection)


@overload
def normalize_seed(seed: None) -> None: ...
@overload
def normalize_seed(seed: int | str) -> int: ...


def normalize_seed(seed: int | str | None) -> int | None:
    if seed is None:
        return None
    if isinstance(seed, int):
        return seed

    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def create_rng(seed: int | str | None) -> random.Random:
    n = normalize_seed(seed)
    return random.Random(n) if n is not None else random.Random()
