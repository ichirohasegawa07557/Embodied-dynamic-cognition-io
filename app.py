from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Embodied Dynamic Cognition I/O", layout="wide")
st.title("Embodied Dynamic Cognition I/O")

st.write("Closed-loop system: observe, estimate, act, receive response, update internal state.")

log_path = Path("logs/closed_loop_log.csv")
if log_path.exists():
    df = pd.read_csv(log_path)
    st.header("Closed-loop log")
    st.dataframe(df.tail(30), use_container_width=True)

    st.header("Summary")
    summary_path = Path("results/summary_metrics.csv")
    if summary_path.exists():
        st.dataframe(pd.read_csv(summary_path), use_container_width=True)

    st.header("Result figures")
    for img in [
        "distance_control_curve.png",
        "action_curve.png",
        "prediction_error_curve.png",
        "state_phase_plot.png",
    ]:
        p = Path("results") / img
        if p.exists():
            st.subheader(img)
            st.image(str(p), use_container_width=True)
else:
    st.warning("Run `python scripts/run_closed_loop.py --mode simulation --steps 240` first.")
