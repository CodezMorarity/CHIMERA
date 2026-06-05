# CHIMERA Project Context

CHIMERA, short for Chaotic Hybrid Matrix Encryption with Randomized DNA Encoding, is an experimental academic encryption framework that intentionally combines Rust systems programming with Python data-science computation inside the encryption and decryption pipeline.

Security disclaimer:

"CHIMERA is an experimental academic encryption framework combining Rust systems programming and Python-driven chaos analytics. It is intended for educational and research purposes only and is not a replacement for audited production cryptographic systems such as AES or ChaCha20."

## Core Idea

CHIMERA is not a Rust encryptor with a Python dashboard. Both runtimes are required for encryption, decryption, and key generation:

- Rust owns file IO, password hashing, DNA encoding/decoding, XOR application, deterministic matrix permutation, file format creation, and CLI orchestration.
- Python owns logistic-map chaos generation, entropy-driven keystream mutation, randomness scoring, avalanche analysis, and histogram/statistical output.
- Rust launches Python as a subprocess and exchanges JSON over stdin/stdout.

If Python is unavailable, the full encryption and decryption pipeline cannot complete.

## Encryption Flow

1. User provides an input file, output file, and password.
2. Rust reads the input bytes and derives a SHA-256 password seed.
3. Rust DNA-encodes each byte into four bases using `00 -> A`, `01 -> T`, `10 -> G`, `11 -> C`.
4. Rust asks Python to generate a chaotic keystream for the exact DNA payload length.
5. Python generates a Logistic Map stream with `r = 3.99`, then applies entropy-driven deterministic mutation.
6. Rust XORs the DNA payload with the Python keystream.
7. Rust matrix-scrambles the XORed payload using a deterministic permutation derived from the password hash.
8. Rust asks Python to analyze entropy, randomness, avalanche behavior, and histogram data.
9. Rust writes a `.chimera` file containing header, metrics metadata, and scrambled payload.

## Decryption Flow

1. Rust validates the `CHIMERA1` file header and extracts metadata.
2. Rust derives the SHA-256 seed from the supplied password.
3. Rust asks Python to regenerate the exact mutated chaotic keystream.
4. Rust reverses the matrix scrambling.
5. Rust reverses XOR with the Python-generated stream.
6. Rust DNA-decodes the result.
7. Rust verifies the recovered data hash and original length.

## File Format

The encrypted file begins with:

- Magic bytes: `CHIMERA1`
- Version: `1`
- Original file length as little-endian `u64`
- Entropy score as little-endian `f64`
- Randomness score as little-endian `f64`
- Metadata JSON length as little-endian `u32`
- Metadata JSON bytes
- Scrambled encrypted payload bytes

The metadata JSON stores details such as original SHA-256 hash, DNA payload length, block size, Python metrics, avalanche score, and histogram data.

## Current Academic Scope

CHIMERA is designed for demonstrable deterministic reversibility and hybrid runtime architecture. It is intentionally educational and should not be presented as production cryptography.
