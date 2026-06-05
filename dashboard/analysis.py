"""Helpers for reading CHIMERA files in the Streamlit dashboard."""

from __future__ import annotations

import json
import struct
from pathlib import Path


MAGIC = b"CHIMERA1"


def read_chimera(path: str | Path) -> dict:
    data = Path(path).read_bytes()
    if len(data) < 37 or data[:8] != MAGIC:
        raise ValueError("not a CHIMERA1 file")

    version = data[8]
    original_length = struct.unpack_from("<Q", data, 9)[0]
    entropy_score = struct.unpack_from("<d", data, 17)[0]
    randomness_score = struct.unpack_from("<d", data, 25)[0]
    metadata_len = struct.unpack_from("<I", data, 33)[0]
    metadata_start = 37
    metadata_end = metadata_start + metadata_len
    metadata = json.loads(data[metadata_start:metadata_end])
    payload = data[metadata_end:]

    return {
        "version": version,
        "original_length": original_length,
        "entropy_score": entropy_score,
        "randomness_score": randomness_score,
        "metadata": metadata,
        "payload": payload,
    }
