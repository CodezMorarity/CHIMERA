"""Avalanche statistics for CHIMERA analysis."""

from __future__ import annotations


def avalanche_percentage(original: bytes, encrypted: bytes) -> float:
    if not original and not encrypted:
        return 0.0

    compared = min(len(original), len(encrypted))
    if compared == 0:
        return 100.0

    changed_bits = 0
    for left, right in zip(original[:compared], encrypted[:compared]):
        changed_bits += (left ^ right).bit_count()

    return (changed_bits / (compared * 8)) * 100.0
