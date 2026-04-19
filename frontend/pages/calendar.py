import sys, os
import streamlit as st # type: ignore
import datetime
import base64

# Robust Path Resolution
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "backend")
if BACKEND not in sys.path: sys.path.insert(0, BACKEND)
if ROOT not in sys.path: sys.path.insert(0, ROOT)

try:
    from styles import SHARED_CSS # type: ignore
    from database import get_user_events # type: ignore
except (ImportError, ModuleNotFoundError):
    try:
        from frontend.styles import SHARED_CSS # type: ignore
        from backend.database import get_user_events # type: ignore
    except:
        pass

def get_base64_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="Calendar - CSM", page_icon="📅", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# BG VFX
bg_path = os.path.join(ROOT, "frontend", "assets", "bg.png")
if os.path.exists(bg_path):
    bin_str = get_base64_bin_file(bg_path)
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(10, 14, 26, 0.9), rgba(10, 14, 26, 0.9)), 
                    url("data:image/png;base64,{bin_str}");
        background-size: cover; background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.get("logged_in"): st.switch_page("pages/streamlit_login.py")

col_back, col_title = st.columns([1, 5])
with col_back:
    if st.button("⬅️ BACK"):
        if st.session_state.get("role") == "admin": st.switch_page("pages/admin_dashboard.py")
        else: st.switch_page("pages/user_dashboard.py")

st.markdown("<div class='vfx-fade-in'><h1>📅 Smart Schedule</h1></div>", unsafe_allow_html=True)

# Main Layout
col_cal, col_ev = st.columns([1, 1])

with col_cal:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    d = st.date_input("Select Date", datetime.date.today())
    st.markdown("</div>", unsafe_allow_html=True)

with col_ev:
    st.markdown("<div class='glass-card vfx-fade-in'>", unsafe_allow_html=True)
    st.markdown(f"### Events for {d.strftime('%B %d')}")
    
    events = get_user_events(st.session_state.get("login_id"), d.isoformat())
    if events:
        for e in events:
            st.markdown(f"""
            <div style="border-left: 3px solid var(--primary-gold); padding-left: 10px; margin-bottom: 10px;">
                <strong style="color:var(--primary-gold);">{e['title']}</strong><br>
                <span style="font-size: 0.8rem; color: var(--text-dim);">{e.get('time', 'All Day')}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No events scheduled.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
with st.container():
    st.markdown("<div class='glass-card vfx-fade-in'>", unsafe_allow_html=True)
    st.markdown("### 🤖 Extraction Logs")
    st.write("The AI is continuously monitoring your workspace for tasks and deadlines.")
    st.markdown("</div>", unsafe_allow_html=True)