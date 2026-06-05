"""Entropy-driven deterministic keystream mutation for CHIMERA."""

from __future__ import annotations

from entropy import shannon_entropy


WINDOW = 64


def mutate_stream(stream: bytes, seed_hex: str) -> bytes:
    seed = bytes.fromhex(seed_hex)
    if not stream:
        return b""

    mutated = bytearray(len(stream))
    rolling = bytearray()
    entropy_bucket = 0

    for i, value in enumerate(stream):
        rolling.append(value)
        if len(rolling) > WINDOW:
            del rolling[0]

        if i % 8 == 0:
            entropy_bucket = int(shannon_entropy(bytes(rolling)) * 32) & 0xFF

        seed_byte = seed[i % len(seed)]
        dynamic = (entropy_bucket + seed_byte + ((i * 73) & 0xFF)) & 0xFF
        rotated = ((value << (i % 5)) | (value >> (8 - (i % 5)))) & 0xFF if i % 5 else value
        mutated[i] = rotated ^ dynamic

    return bytes(mutated)
