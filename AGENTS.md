# AGENTS.md

This repository is for CHIMERA, a final-year academic cryptography/systems/data-science project.

## Engineering Role

Act as a senior cryptography engineer, Rust systems developer, and Python data science engineer. Keep Rust and Python deeply integrated in the encryption pipeline itself.

## Non-Negotiable Architecture

- Rust and Python must both participate in encryption.
- Rust and Python must both participate in decryption.
- Python must not be limited to dashboard or visualization work.
- Rust must launch Python over JSON stdin/stdout for the initial implementation.

## Rust Responsibilities

Rust code lives in `rust_core/` and owns:

- CLI entry point
- File IO
- SHA-256 password hashing
- DNA encode/decode
- XOR engine
- Deterministic matrix scrambling and unscrambling
- `.chimera` file format read/write
- Python subprocess bridge
- End-to-end orchestration

## Python Responsibilities

Python code lives in `python_engine/` and owns:

- Logistic Map chaotic keystream generation
- Entropy analysis
- Entropy-based deterministic stream mutation
- Randomness scoring
- Avalanche statistics
- Histogram generation
- JSON API consumed by Rust

## Testing Expectations

At minimum, maintain tests that prove:

- `decrypt(encrypt(data, password), password) == data`
- Empty files round-trip.
- Text, binary, and image-like byte payloads round-trip.
- Wrong passwords fail.
- Rust DNA, XOR, permutation, and file-format components are deterministic and reversible.

Python-dependent Rust integration tests should skip cleanly if no Python interpreter is available, but the application itself should fail clearly when Python cannot be launched.

## Security Posture

Always include the project disclaimer in user-facing documentation:

"CHIMERA is an experimental academic encryption framework combining Rust systems programming and Python-driven chaos analytics. It is intended for educational and research purposes only and is not a replacement for audited production cryptographic systems such as AES or ChaCha20."
