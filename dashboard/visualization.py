"""Visualization helpers for the CHIMERA Streamlit dashboard."""

from __future__ import annotations

import matplotlib.pyplot as plt


def histogram_figure(counts: list[int], title: str = "Byte histogram"):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(256), counts, width=1.0, color="#2f6f73")
    ax.set_xlabel("Byte value")
    ax.set_ylabel("Frequency")
    ax.set_title(title)
    ax.set_xlim(0, 255)
    fig.tight_layout()
    return fig


def keystream_preview_figure(values: list[int], title: str = "Keystream preview"):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(values[:512], color="#9b3d5c", linewidth=1)
    ax.set_xlabel("Index")
    ax.set_ylabel("Byte")
    ax.set_title(title)
    fig.tight_layout()
    return fig
