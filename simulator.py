import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

# Load banner image
banner = Image.open("/Users/peterwang/Downloads/apple_731985.png")

# Layout: Banner on the left, Title on the right
col1, col2 = st.columns([1, 25])
with col1:
    st.image(banner, width=40)
with col2:
    st.markdown("""
        <h3 style="margin-top: 0.05rem;">AppleCare BizOps</h3>
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

# Initialize session state
if "results" not in st.session_state:
    st.session_state.results = {
        "FATP": {"UPPH": None, "Cost": None},
        "CSD": {"UPPH": None, "Cost": None},
    }

col1, col2 = st.columns(2)

with col1:
    st.header("📦 FATP")
    fatp_uph = st.number_input("UPH (FATP)", key="fatp_uph", min_value=0.0, step=1.0, format="%.2f")
    fatp_dl = st.number_input("DL HC (FATP)", key="fatp_dl", min_value=0, step=1)
    fatp_util_pct = st.number_input("Utilization (%) (FATP)", min_value=1, max_value=100, value=85, step=1, format="%d")  # User sees %
    fatp_util = fatp_util_pct / 100.0
    st.session_state.fatp_util = fatp_util
    fatp_wage = st.number_input("Hourly Wage ($) (FATP)", key="fatp_wage", min_value=0.0, step=1.0, format="%.2f")
    if st.button("Calculate FATP"):
        upph = fatp_uph * fatp_dl
        cost = fatp_wage / fatp_util / upph if upph > 0 else 0
        st.success(f"UPPH: {upph:,.2f} | DL Should Cost: ${cost:,.4f}")
        st.session_state.results["FATP"]["UPPH"] = upph
        st.session_state.results["FATP"]["Cost"] = cost

with col2:
    st.header("🛠️ CSD Mainline")
    csd_uph = st.number_input("UPH (CSD)", key="csd_uph", min_value=0.0, step=1.0, format="%.2f")
    csd_dl = st.number_input("DL HC (CSD)", key="csd_dl", min_value=0, step=1)
    csd_util_pct = st.number_input("Utilization (%) (CSD)", min_value=1, max_value=100, value=85, step=1, format="%d")
    csd_util = csd_util_pct / 100.0
    st.session_state.csd_util = csd_util
    csd_wage = st.number_input("Hourly Wage ($) (CSD)", key="csd_wage", min_value=0.0, step=1.0, format="%.2f")
    if st.button("Calculate CSD Mainline"):
        upph = csd_uph * csd_dl
        cost = csd_wage / csd_util / upph if upph > 0 else 0
        st.success(f"UPPH: {upph:,.2f} | DL Should Cost: ${cost:,.4f}")
        st.session_state.results["CSD"]["UPPH"] = upph
        st.session_state.results["CSD"]["Cost"] = cost

st.markdown("---")
if st.button("📊 Show Separate Comparison Charts"):
    fatp = st.session_state.results["FATP"]
    csd = st.session_state.results["CSD"]

    if None in fatp.values() or None in csd.values():
        st.warning("⚠️ Please calculate both FATP and CSD Mainline first.")
    else:
        import matplotlib.pyplot as plt

        # Define unique color pairs for each chart
        color_styles = [
            ("#FF6F61", "#6B5B95"),
            ("#88B04B", "#F7CAC9"),
            ("#92A8D1", "#955251"),
            ("#45B8AC", "#EFC050"),
            ("#5B5EA6", "#9B2335"),
            ("#BC243C", "#C3447A")
        ]

        # Attribute list
        attributes = [
            ("UPH", st.session_state.fatp_uph, st.session_state.csd_uph),
            ("DL HC", st.session_state.fatp_dl, st.session_state.csd_dl),
            ("Utilization", st.session_state.fatp_util, st.session_state.csd_util),
            ("UPPH", fatp["UPPH"], csd["UPPH"]),
            ("Hourly Wage", st.session_state.fatp_wage, st.session_state.csd_wage),
            ("DL Should Cost", fatp["Cost"], csd["Cost"])
        ]

        for i, (attr, fatp_val, csd_val) in enumerate(attributes):
            fig, ax = plt.subplots(figsize=(6, 2.5))  # Smaller height

            values = [fatp_val, csd_val]
            labels = ["FATP", "CSD Mainline"]
            colors = color_styles[i % len(color_styles)]

            # Bar chart
            ax.barh(labels, values, color=colors)

            # Axis labels and title
            ax.set_xlabel("Value")
            ax.set_ylabel(attr)
            ax.set_title(f"{attr} Comparison: FATP vs CSD Mainline")

            # Format labels
            offset = max(abs(val) for val in values) * 0.02
            for j, v in enumerate(values):
                ax.text(v + offset, j, f"{v:,.3f}", va='center')

            # Expand X-axis limits for label and delta spacing
            max_bar = max(values)
            x_buffer = max_bar * 0.35  # more buffer for tighter charts
            ax.set_xlim(0, max_bar + x_buffer)

            # Show delta
            delta = csd_val - fatp_val
            ax.text(
                max_bar + (x_buffer * 0.6),
                0.5,
                f"Δ: {delta:+.3f}",
                fontsize=9,
                fontweight='bold',
                va='center',
                ha='left',
                color="darkred"
            )

            st.pyplot(fig)