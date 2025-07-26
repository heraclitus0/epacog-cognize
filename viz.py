import matplotlib.pyplot as plt
import streamlit as st


def plot_rcc_trace(history, title="RCC Epistemic Trace"):
    """
    Plots ∆(t), Θ(t), E(t), and S̄(t) over time.
    Highlights rupture points.
    """

    steps = list(range(len(history)))
    deltas = [h["∆"] for h in history]
    thresholds = [h["Θ"] for h in history]
    Es = [h["E"] for h in history]
    S_bars = [h["S̄"] for h in history]
    ruptures = [i for i, h in enumerate(history) if h["rupture"]]

    fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

    # ∆ vs Θ
    axs[0].plot(steps, deltas, label='∆(t)', color='blue')
    axs[0].plot(steps, thresholds, label='Θ(t)', color='red', linestyle='--')
    axs[0].set_ylabel("Drift & Threshold")
    axs[0].legend()
    for r in ruptures:
        axs[0].axvline(x=r, color='gray', linestyle=':', alpha=0.5)

    # E(t)
    axs[1].plot(steps, Es, label='E(t)', color='purple')
    axs[1].set_ylabel("Cumulative Drift")
    for r in ruptures:
        axs[1].axvline(x=r, color='gray', linestyle=':', alpha=0.5)

    # S̄(t)
    axs[2].plot(steps, S_bars, label='S̄(t)', color='green')
    axs[2].axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    axs[2].set_ylabel("Projected Divergence")
    for r in ruptures:
        axs[2].axvline(x=r, color='gray', linestyle=':', alpha=0.5)

    # Rupture flags
    rupture_flags = [1 if h["rupture"] else 0 for h in history]
    axs[3].bar(steps, rupture_flags, color='black')
    axs[3].set_ylabel("Rupture")
    axs[3].set_xlabel("Cycle t")

    fig.suptitle(title)
    st.pyplot(fig)
