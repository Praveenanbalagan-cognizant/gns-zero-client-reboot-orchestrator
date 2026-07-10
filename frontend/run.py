from __future__ import annotations

import sys
from pathlib import Path

try:
    import streamlit as st
except ModuleNotFoundError as exc:
    raise SystemExit("Streamlit is not installed. Run: python -m pip install streamlit") from exc


repo_root = Path(__file__).resolve().parents[1]
backend_path = repo_root / "backend"
sys.path.insert(0, str(backend_path))

from run import invoke_agent  # noqa: E402


st.set_page_config(page_title="GNS AP Reboot Orchestrator", layout="wide")
st.title("GNS Zero-Client Reboot Orchestrator")

site_tag = st.text_input("Site tag", value="BLR-CAMPUS")
min_uptime_days = st.number_input("Minimum uptime days", min_value=1, value=100)
dry_run = st.checkbox("Dry run", value=True)

if st.button("Generate Reboot Plan"):
    report = invoke_agent(site_tag=site_tag, min_uptime_days=int(min_uptime_days), dry_run=dry_run)
    st.markdown(report)
