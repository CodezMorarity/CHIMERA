"""Logistic Map chaos generation for CHIMERA."""

from __future__ import annotations

import hashlib


R = 3.99
WARMUP_ROUNDS = 128


def _seed_to_x(seed_hex: str) -> float:
    digest = hashlib.sha256(bytes.fromhex(seed_hex)).digest()
    value = int.from_bytes(digest[:8], "big")
    # Keep the initial state away from exactly 0 or 1.
    return ((value % 10**12) + 1) / (10**12 + 2)


def logistic_map_keystream(seed_hex: str, length: int) -> bytes:
    if length < 0:
        raise ValueError("length must be non-negative")

    x = _seed_to_x(seed_hex)
    for _ in range(WARMUP_ROUNDS):
        x = R * x * (1.0 - x)

    out = bytearray()
    for _ in range(length):
        x = R * x * (1.0 - x)
        value = int((x * 1_000_000) % 256)
        out.append(value)
    return bytes(out)
