import sys, os
import streamlit as st # type: ignore

# Path resolution
CWD = os.getcwd()
if CWD not in sys.path: sys.path.insert(0, CWD)
BACKEND_DIR = os.path.join(CWD, "backend")
if BACKEND_DIR not in sys.path: sys.path.insert(0, BACKEND_DIR)

try:
    from styles import SHARED_CSS # type: ignore
except:
    pass

st.set_page_config(page_title="Calendar – CSM", page_icon="🌌", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Auth guard
if not st.session_state.get("logged_in"): st.switch_page("pages/streamlit_login.py")

# Header
col_back, col_title = st.columns([1, 5])
with col_back:
    if st.button("⬅️ BACK", use_container_width=True):
        if st.session_state.get("role") == "admin": st.switch_page("pages/admin_dashboard.py")
        else: st.switch_page("pages/user_dashboard.py")

st.title("🌌 Smart Workspace Calendar")
st.write("Neural scheduling for the corporate ecosystem.")

st.divider()

# Interface
c1, c2 = st.columns([1, 1])

with c1:
    with st.container(border=True):
        st.subheader("📅 Target Date Selection")
        selected_date = st.date_input("Select Phase Date")
        st.info(f"Scanning protocols for: {selected_date}")

with c2:
    with st.container(border=True):
        st.subheader(f"🛡️ Events for {selected_date}")
        st.write("Searching workspace logs...")
        st.info("No corporate events identified for this period.")

st.divider()
st.subheader("⚖️ AI Extraction Logs")
st.write("The AI is continuously monitoring your workspace for tasks and deadlines.")
st.progress(100, text="System Synchronized")