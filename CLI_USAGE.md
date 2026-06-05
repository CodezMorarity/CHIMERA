# CHIMERA CLI Usage

Security disclaimer:

"CHIMERA is an experimental academic encryption framework combining Rust systems programming and Python-driven chaos analytics. It is intended for educational and research purposes only and is not a replacement for audited production cryptographic systems such as AES or ChaCha20."

## Prerequisites

- Rust toolchain with Cargo
- Python 3

If Python is not available on `PATH`, set `CHIMERA_PYTHON` to the full Python executable path.

PowerShell example:

```powershell
$env:CHIMERA_PYTHON="C:\Path\To\python.exe"
```

## Encrypt

```powershell
cd D:\CHIMERA\rust_core
cargo run -- encrypt input.txt output.chimera "my password"
```

## Decrypt

```powershell
cd D:\CHIMERA\rust_core
cargo run -- decrypt output.chimera restored.txt "my password"
```

## Run Tests

```powershell
cd D:\CHIMERA\rust_core
cargo test
```

Python-dependent tests skip cleanly when no Python interpreter is available. To force the bundled Codex runtime during local development:

```powershell
$env:CHIMERA_PYTHON="C:\Users\TEJAS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
cargo test
```

## Dashboard

```powershell
cd D:\CHIMERA
streamlit run dashboard\app.py
```

Upload a `.chimera` file to view entropy, randomness, avalanche, histogram, and embedded Python metrics.
