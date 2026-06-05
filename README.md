# CHIMERA

Chaotic Hybrid Matrix Encryption with Randomized DNA Encoding: an academic Rust/Python encryption framework that keeps both runtimes inside the encryption and decryption pipeline.

CHIMERA is an experimental academic encryption framework combining Rust systems programming and Python-driven chaos analytics. It is intended for educational and research purposes only and is not a replacement for audited production cryptographic systems such as AES or ChaCha20.

## Highlights

- **Hybrid encryption pipeline:** Rust orchestrates the CLI and byte-level transforms while Python generates and analyzes chaotic streams.
- **Python participates in encryption and decryption:** Rust launches `python_engine/keystream_api.py` over JSON stdin/stdout for keystream generation during both directions.
- **DNA-inspired encoding:** Rust maps every byte into four symbolic bases using `00 -> A`, `01 -> T`, `10 -> G`, and `11 -> C`.
- **Deterministic reversible transforms:** XOR and matrix permutation are password-derived and tested for round-trip correctness.
- **Custom `.chimera` container:** Encrypted files carry a `CHIMERA1` header, original length, entropy/randomness scores, JSON metadata, histogram data, and encrypted payload.
- **Academic analysis tooling:** Python computes Shannon entropy, randomness score, avalanche statistics, and byte histograms for encrypted outputs.
- **Streamlit dashboard:** Upload a `.chimera` file to inspect embedded metrics and visualization plots.

## Contents

- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [CLI Usage](#cli-usage)
- [Repository Layout](#repository-layout)
- [Architecture](#architecture)
- [Encryption Flow](#encryption-flow)
- [Decryption Flow](#decryption-flow)
- [`.chimera` File Format](#chimera-file-format)
- [Testing](#testing)
- [Dashboard](#dashboard)
- [Development Notes](#development-notes)
- [Research Materials](#research-materials)
- [Security Posture](#security-posture)
- [License](#license)

## Requirements

- Rust toolchain with Cargo
- Python 3.10 or newer available as `python`, `python3`, `py`, or through `CHIMERA_PYTHON`
- Optional dashboard dependencies from `python_engine/requirements.txt`

If your default `python` is older than 3.10, point `CHIMERA_PYTHON` at a newer interpreter before running the Rust CLI or integration tests. On Windows, the Python launcher usually works well:

```powershell
$env:CHIMERA_PYTHON="py"
```

## Quick Start

Build the Rust CLI and run an encrypt/decrypt round-trip from the repository root:

```powershell
cd D:\CHIMERA
New-Item -ItemType Directory -Force Result | Out-Null
cd rust_core
cargo run -- encrypt ..\PROJECT_CONTEXT.md ..\Result\project_context.chimera "research-password"
cargo run -- decrypt ..\Result\project_context.chimera ..\Result\project_context.restored.md "research-password"
```

Successful encryption prints entropy, randomness, and avalanche scores. Successful decryption prints `Decrypted.` and writes the restored file.

On Windows, `startup.bat` provides an interactive launcher for building the Rust core, encrypting files, decrypting `.chimera` files, running a demo round-trip, starting the dashboard, and running tests:

```powershell
cd D:\CHIMERA
.\startup.bat
```

## CLI Usage

Run commands from `rust_core/`. The CLI accepts `encrypt` with an input path, output `.chimera` path, and password, or `decrypt` with an input `.chimera` path, restored output path, and password.

```powershell
cd D:\CHIMERA\rust_core
cargo run -- encrypt ..\PROJECT_CONTEXT.md ..\Result\context.chimera "correct horse battery staple"
cargo run -- decrypt ..\Result\context.chimera ..\Result\context.restored.md "correct horse battery staple"
```

Wrong passwords should fail during integrity verification with a clear CHIMERA error instead of producing trusted plaintext.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `rust_core/` | Rust crate and CLI for file IO, hashing, DNA encode/decode, XOR, permutation, file-format handling, Python bridge, and end-to-end orchestration. |
| `python_engine/` | Python chaos and analysis engine used by Rust through JSON stdin/stdout. |
| `dashboard/` | Streamlit dashboard for reading `.chimera` files and visualizing entropy, randomness, avalanche, histogram, and keystream metadata. |
| `Documentation/` | Research paper content and project PDF drafts. |
| `PROJECT_CONTEXT.md` | Detailed architecture notes and current implementation scope. |
| `CLI_USAGE.md` | Short command reference for the Rust CLI and dashboard. |
| `TODO.md` | Completed scaffold items and future improvement ideas. |
| `startup.bat` | Windows menu launcher for common project actions. |

## Architecture

CHIMERA intentionally splits responsibilities between Rust and Python.

Rust owns:

- CLI entry point in `rust_core/src/main.rs`
- File IO and end-to-end orchestration in `rust_core/src/chimera.rs`
- SHA-256 password hashing
- DNA encoding and decoding in `rust_core/src/dna.rs`
- XOR in `rust_core/src/xor_engine.rs`
- Deterministic matrix scrambling and unscrambling in `rust_core/src/permutation.rs`
- `.chimera` file read/write in `rust_core/src/fileformat.rs`
- Python subprocess bridge in `rust_core/src/python_bridge.rs`

Python owns:

- Logistic Map chaotic keystream generation in `python_engine/chaos.py`
- Entropy-based deterministic stream mutation in `python_engine/mutation.py`
- Shannon entropy, randomness score, and histogram helpers in `python_engine/entropy.py`
- Avalanche statistics in `python_engine/avalanche.py`
- JSON API consumed by Rust in `python_engine/keystream_api.py`

## Encryption Flow

1. Rust reads the input file and hashes the password with SHA-256.
2. Rust DNA-encodes the plaintext bytes into an `A/T/G/C` byte sequence.
3. Rust sends a JSON `keygen` request to Python with the password-derived seed and required stream length.
4. Python generates a Logistic Map keystream with `r = 3.99`, mutates it deterministically using entropy feedback, and returns it as hex.
5. Rust XORs the DNA payload with the Python-generated keystream.
6. Rust applies deterministic matrix scrambling in 256-byte blocks.
7. Rust sends an `analyze` request to Python for entropy, randomness, avalanche, and histogram metrics.
8. Rust writes the final `.chimera` file with header metadata and scrambled encrypted payload.

## Decryption Flow

1. Rust validates the `CHIMERA1` file header and reads embedded metadata.
2. Rust hashes the supplied password with SHA-256.
3. Rust asks Python to regenerate the exact mutated chaotic keystream.
4. Rust reverses matrix scrambling.
5. Rust reverses XOR with the Python-generated stream.
6. Rust DNA-decodes the recovered payload.
7. Rust verifies the restored byte length and original SHA-256 hash.

## `.chimera` File Format

Encrypted files use a compact binary container:

| Field | Type | Description |
| --- | --- | --- |
| Magic bytes | 8 bytes | `CHIMERA1` |
| Version | `u8` | Current version is `1` |
| Original length | little-endian `u64` | Plaintext byte length |
| Entropy score | little-endian `f64` | Python-computed encrypted payload entropy |
| Randomness score | little-endian `f64` | Python-computed randomness score |
| Metadata length | little-endian `u32` | Length of the following JSON metadata |
| Metadata JSON | bytes | Original SHA-256 hash, DNA length, block size, Python metrics, and histogram |
| Payload | bytes | Scrambled encrypted payload |

## Testing

Run Rust unit and integration tests from the Rust crate:

```powershell
cd D:\CHIMERA\rust_core
cargo test
```

The test suite covers DNA mapping, XOR reversibility, permutation reversibility, `.chimera` file-format round-trips, text/binary/image-like payload round-trips, empty file round-trips, wrong-password failure, and deterministic decryption. Python-dependent integration tests skip cleanly if no Python interpreter is available, while the application itself fails clearly when Python cannot be launched.

## Dashboard

Install dashboard dependencies and start Streamlit from the repository root:

```powershell
cd D:\CHIMERA
py -m pip install -r python_engine\requirements.txt
py -m streamlit run dashboard\app.py
```

Upload a `.chimera` file to view version, original byte length, entropy, randomness, avalanche effect, original/encrypted histograms, a mutated keystream preview, and embedded Python metrics.

## Development Notes

- `CHIMERA_PYTHON` controls which Python interpreter Rust launches.
- Rust expects the Python API script at `python_engine/keystream_api.py` relative to `rust_core/`.
- Generated outputs such as `Result/`, `*.chimera`, `rust_core/target/`, and Streamlit upload scratch files are ignored by git.
- Python dependencies are only required for the dashboard; the core bridge currently uses standard-library Python modules.
- The current bridge sends JSON over stdin/stdout and hex-encodes byte arrays, which is simple and inspectable but not optimized for very large files.

## Research Materials

Project write-ups and paper drafts live under `Documentation/`, including `CHIMERA_RESEARCH_PAPER_CONTENT.txt` and several PDF drafts. `PROJECT_CONTEXT.md` is the best concise source for the implemented architecture and should stay aligned with the code as the project evolves.

## Security Posture

CHIMERA is built for academic exploration of hybrid runtime architecture, deterministic reversibility, DNA-inspired symbolic transforms, chaotic keystream generation, and statistical analysis. It has not undergone formal cryptographic proof work, third-party cryptanalysis, or production security auditing.

Use AES, ChaCha20, or another audited standard cryptographic system for real confidentiality requirements.

## License

No license file is currently included in this repository. Add a license before publishing, distributing, or reusing the code outside the academic project context.
