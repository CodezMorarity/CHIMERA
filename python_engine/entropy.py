"""Entropy and randomness scoring helpers for CHIMERA."""

from __future__ import annotations

import math
from collections import Counter


def histogram(data: bytes) -> list[int]:
    counts = [0] * 256
    for value in data:
        counts[value] += 1
    return counts


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0

    total = len(data)
    entropy = 0.0
    for count in Counter(data).values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy


def randomness_score(data: bytes) -> float:
    if not data:
        return 0.0

    entropy_component = shannon_entropy(data) / 8.0
    ones = sum(value.bit_count() for value in data)
    total_bits = len(data) * 8
    balance_component = 1.0 - abs(0.5 - (ones / total_bits)) * 2.0

    if len(data) == 1:
        transition_component = 1.0
    else:
        transitions = sum(1 for a, b in zip(data, data[1:]) if a != b)
        transition_component = transitions / (len(data) - 1)

    score = 0.55 * entropy_component + 0.30 * balance_component + 0.15 * transition_component
    return max(0.0, min(1.0, score))
