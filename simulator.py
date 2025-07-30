import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

# Load banner image
banner = Image.open("apple_logo.png")

# Layout: Banner on the left, Title on the right
col1, col2 = st.columns([1, 30])
with col1:
    st.image(banner, width=40)
with col2:
    st.markdown("""
        <h3 style="margin-top: 0.0rem;">AppleCare BizOps</h3>
    """, unsafe_allow_html=True)

# Functional part designing

st.set_page_config(page_title="Cost Comparison Simulator", layout="wide")

# Centered title and subtitle using HTML
st.markdown("""
    <div style='text-align: center; padding-top: 0.5rem;'>
        <h1 style='font-size: 2.5rem;'>🏭 Cost Simulator: FATP vs CSD Mainline</h1>
        <p style='font-size: 1.2rem;'>Compare 📱 production cost metrics between 
        <strong>FATP(Excluding SMT)</strong> and <strong>CSD Mainline</strong>.</p>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")
# Initialize session state
if "results" not in st.session_state:
    st.session_state.results = {
        "FATP": {"UPPH": None, "Cost": None},
        "CSD": {"UPPH": None, "Cost": None},
    }

col1, col2 = st.columns(2)

with col1:
    st.header("FATP")
    fatp_uph = st.number_input("UPH (FATP)", key="fatp_uph", min_value=0.0, step=1.0, format="%.2f")
    fatp_dl = st.number_input("DL HC (FATP)", key="fatp_dl", min_value=0, step=1)
    fatp_util_pct = st.number_input("Utilization (%) (FATP)", min_value=1, max_value=100, value=85, step=1, format="%d")  # User sees %
    fatp_util = fatp_util_pct / 100.0
    st.session_state.fatp_util = fatp_util
    fatp_wage = st.number_input("Hourly Wage ($) (FATP)", key="fatp_wage", min_value=0.0, step=1.0, format="%.2f")
    if st.button("Calculate FATP"):
        upph = fatp_uph / fatp_dl if fatp_dl > 0 else 0
        cost = fatp_wage / fatp_util / upph if upph > 0 else 0

        st.session_state.results["FATP"]["UPPH"] = upph
        st.session_state.results["FATP"]["Cost"] = cost
        st.session_state["fatp_calculated"] = True
    if st.session_state.get("fatp_calculated"):
        upph = st.session_state.results["FATP"]["UPPH"]
        cost = st.session_state.results["FATP"]["Cost"]
        st.success(f"UPPH: {upph:,.2f} | DL Should Cost: ${cost:,.4f}")
with col2:
    st.header("CSD Mainline")
    csd_uph = st.number_input("UPH (CSD)", key="csd_uph", min_value=0.0, step=1.0, format="%.2f")
    csd_dl = st.number_input("DL HC (CSD)", key="csd_dl", min_value=0, step=1)
    csd_util_pct = st.number_input("Utilization (%) (CSD)", min_value=1, max_value=100, value=85, step=1, format="%d")
    csd_util = csd_util_pct / 100.0
    st.session_state.csd_util = csd_util
    csd_wage = st.number_input("Hourly Wage ($) (CSD)", key="csd_wage", min_value=0.0, step=1.0, format="%.2f")
    if st.button("Calculate CSD Mainline"):
        upph = csd_uph / csd_dl if csd_dl > 0 else 0
        cost = csd_wage / csd_util / upph if upph > 0 else 0

        st.session_state.results["CSD"]["UPPH"] = upph
        st.session_state.results["CSD"]["Cost"] = cost
        st.session_state["csd_calculated"] = True

    if st.session_state.get("csd_calculated"):
        upph = st.session_state.results["CSD"]["UPPH"]
        cost = st.session_state.results["CSD"]["Cost"]
        st.success(f"UPPH: {upph:,.2f} | DL Should Cost: ${cost:,.4f}")


st.markdown("---")
if st.button("📊 Show UPPH & DL Should Cost Charts"):
    fatp = st.session_state.results["FATP"]
    csd = st.session_state.results["CSD"]

    if None in fatp.values() or None in csd.values():
        st.warning("⚠️ Please calculate both FATP and CSD Mainline first.")
    else:
        import matplotlib.pyplot as plt
        import numpy as np

        # Use a cleaner theme
        plt.style.use("seaborn-v0_8-whitegrid")

        attributes = [
            ("UPPH", fatp["UPPH"], csd["UPPH"]),
            ("DL Should Cost", fatp["Cost"], csd["Cost"])
        ]

        fig, axes = plt.subplots(1, 2, figsize=(14, 4.2))  # More width + height

        color_styles = [("#4CAF50", "#2196F3"), ("#BC243C", "#F7CAC9")]

        for i, (attr, fatp_val, csd_val) in enumerate(attributes):
            ax = axes[i]
            values = [fatp_val, csd_val]
            labels = ["FATP", "CSD Mainline"]
            colors = color_styles[i % len(color_styles)]

            # Draw horizontal bars with edge rounding
            bars = ax.barh(labels, values, color=colors, edgecolor="black", height=0.5)

            # Set titles and labels
            ax.set_xlabel("Value", fontsize=10)
            ax.set_title(f"{attr} Comparison", fontsize=12, fontweight="bold")

            # Format value labels
            offset = max(abs(val) for val in values) * 0.02
            for j, (bar, val) in enumerate(zip(bars, values)):
                ax.text(val + offset, bar.get_y() + bar.get_height() / 2,
                        f"{val:,.3f}",
                        va='center', ha='left', fontsize=9, color="black")

            # Set x-axis limit with buffer
            max_val = max(values)
            x_buffer = max_val * 0.4
            ax.set_xlim(0, max_val + x_buffer)

            # Show delta
            delta = csd_val - fatp_val
            ax.text(max_val + (x_buffer * 0.45), 0.5,
                    f"Δ: {delta:+.3f}",
                    fontsize=10, fontweight='bold',
                    va='center', ha='left', color="darkred")

            # Reduce clutter
            ax.tick_params(axis='y', labelsize=10)
            ax.tick_params(axis='x', labelsize=9)
            ax.grid(axis='x', linestyle='--', alpha=0.5)
            ax.set_facecolor("#F9F9F9")

        plt.tight_layout()
        st.pyplot(fig)