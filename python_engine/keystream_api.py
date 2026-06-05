"""JSON stdin/stdout API used by Rust.

Request examples:
{"mode": "keygen", "seed_hex": "...", "length": 1024}
{"mode": "analyze", "original_hex": "...", "encrypted_hex": "...", "keystream_hex": "..."}
"""

from __future__ import annotations

import json
import sys
import time

from avalanche import avalanche_percentage
from chaos import R, logistic_map_keystream
from entropy import histogram, randomness_score, shannon_entropy
from mutation import mutate_stream


def _decode_hex(name: str, value: str) -> bytes:
    try:
        return bytes.fromhex(value)
    except ValueError as exc:
        raise ValueError(f"{name} is not valid hex") from exc


def _handle_keygen(request: dict) -> dict:
    started = time.perf_counter()
    seed_hex = request["seed_hex"]
    length = int(request["length"])

    base = logistic_map_keystream(seed_hex, length)
    mutated = mutate_stream(base, seed_hex)
    elapsed_ms = (time.perf_counter() - started) * 1000

    return {
        "ok": True,
        "keystream_hex": mutated.hex(),
        "metrics": {
            "logistic_r": R,
            "length": length,
            "base_entropy": shannon_entropy(base),
            "mutated_entropy": shannon_entropy(mutated),
            "mutated_randomness": randomness_score(mutated),
            "keystream_preview": list(mutated[:512]),
            "elapsed_ms": elapsed_ms,
        },
    }


def _handle_analyze(request: dict) -> dict:
    original = _decode_hex("original_hex", request.get("original_hex", ""))
    encrypted = _decode_hex("encrypted_hex", request.get("encrypted_hex", ""))
    keystream = _decode_hex("keystream_hex", request.get("keystream_hex", ""))

    encrypted_entropy = shannon_entropy(encrypted)
    encrypted_randomness = randomness_score(encrypted)
    key_entropy = shannon_entropy(keystream)
    original_histogram = histogram(original)
    encrypted_histogram = histogram(encrypted)

    return {
        "ok": True,
        "entropy_score": encrypted_entropy,
        "randomness_score": encrypted_randomness,
        "avalanche_score": avalanche_percentage(original, encrypted),
        "histogram": encrypted_histogram,
        "metrics": {
            "original_entropy": shannon_entropy(original),
            "encrypted_entropy": encrypted_entropy,
            "keystream_entropy": key_entropy,
            "encrypted_randomness": encrypted_randomness,
            "keystream_randomness": randomness_score(keystream),
            "avalanche_score": avalanche_percentage(original, encrypted),
            "original_histogram": original_histogram,
            "encrypted_histogram": encrypted_histogram,
        },
    }


def handle(request: dict) -> dict:
    mode = request.get("mode")
    if mode == "keygen":
        return _handle_keygen(request)
    if mode == "analyze":
        return _handle_analyze(request)
    raise ValueError(f"unknown mode: {mode}")


def main() -> int:
    try:
        request = json.loads(sys.stdin.read())
        response = handle(request)
    except Exception as exc:  # Rust needs a JSON envelope even on Python failures.
        response = {"ok": False, "error": str(exc)}

    sys.stdout.write(json.dumps(response, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
