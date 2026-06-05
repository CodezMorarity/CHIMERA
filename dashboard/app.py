from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))

from analysis import read_chimera
from visualization import histogram_figure, keystream_preview_figure


st.set_page_config(page_title="CHIMERA Dashboard", layout="wide")
st.title("CHIMERA Analysis Dashboard")

st.caption(
    "CHIMERA is an experimental academic encryption framework combining Rust systems programming "
    "and Python-driven chaos analytics. It is intended for educational and research purposes only "
    "and is not a replacement for audited production cryptographic systems such as AES or ChaCha20."
)

uploaded = st.file_uploader("Open a .chimera file", type=["chimera"])

if uploaded:
    temp_path = Path(".streamlit_uploaded.chimera")
    temp_path.write_bytes(uploaded.getvalue())
    parsed = read_chimera(temp_path)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Version", parsed["version"])
    col2.metric("Original bytes", parsed["original_length"])
    col3.metric("Entropy", f"{parsed['entropy_score']:.4f}")
    col4.metric("Randomness", f"{parsed['randomness_score']:.4f}")

    metrics = parsed["metadata"].get("python_metrics", {})
    analysis = metrics.get("analysis", {})
    keygen = metrics.get("keygen", {})
    avalanche = analysis.get("avalanche_score")
    if avalanche is not None:
        st.metric("Avalanche effect", f"{avalanche:.2f}%")

    entropy_cols = st.columns(3)
    entropy_cols[0].metric("Original entropy", f"{analysis.get('original_entropy', 0.0):.4f}")
    entropy_cols[1].metric("Encrypted entropy", f"{analysis.get('encrypted_entropy', 0.0):.4f}")
    entropy_cols[2].metric("Encryption time", f"{metrics.get('elapsed_ms', 0)} ms")

    left, right = st.columns(2)
    with left:
        st.pyplot(histogram_figure(analysis.get("original_histogram", [0] * 256), "Original byte histogram"))
    with right:
        st.pyplot(histogram_figure(analysis.get("encrypted_histogram", parsed["metadata"].get("histogram", [0] * 256)), "Encrypted payload histogram"))

    st.pyplot(keystream_preview_figure(keygen.get("keystream_preview", []), "Mutated chaotic keystream preview"))

    st.subheader("Embedded Python metrics")
    st.json(metrics)
else:
    st.info("Upload an encrypted CHIMERA file to inspect entropy, randomness, avalanche metrics, and histogram data.")
