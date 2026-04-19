import sys, os
import streamlit as st # type: ignore
import base64 # type: ignore

# Proxy Resolution - Need to reach back to root
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
if ROOT not in sys.path: sys.path.insert(0, ROOT)
BACKEND = os.path.join(ROOT, "backend")
if BACKEND not in sys.path: sys.path.insert(0, BACKEND)

try:
    from styles import SHARED_CSS # type: ignore
    from auth import login_user # type: ignore
except ImportError:
    st.error("System Core Migration in Progress. Please refresh or run 'streamlit run app.py' from root.")
    st.stop()

st.set_page_config(page_title="CSM | Secure Access", page_icon="🛡️", layout="centered")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# LOAD LOGO
logo_path = r"C:\Users\Shanmukh\.gemini\antigravity\brain\c3b5482f-7dac-4b8f-8f4a-837dec3830d4\corporate_messenger_logo_1776631382023.png"
def get_b64(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""
l_b64 = get_b64(logo_path)

st.markdown("<div style='margin-top: -60px;'></div>", unsafe_allow_html=True)
if l_b64:
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{l_b64}" width="140"></div>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>CORPORATE SMART MESSENGER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: var(--lux-gold) !important; letter-spacing: 4px; font-weight: 700; margin-bottom: 2.5rem;'>OFFICIAL WORKSPACE PROTOCOL</p>", unsafe_allow_html=True)

with st.container():
    st.markdown("### 🔐 Identity Validation")
    with st.form("login_form"):
        lid = st.text_input("Corporate Identifier", placeholder="e.g. finman000001")
        pwd = st.text_input("Security Protocol Key", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("VALIDATE & SECURE ACCESS"):
            if lid and pwd:
                success, message, user_data = login_user(lid, pwd)
                if success:
                    for k, v in user_data.items(): st.session_state[k] = v
                    st.session_state["logged_in"] = True
                    # CORRECTED PATHS for the frontend/pages/ location
                    if not user_data.get("password_changed"): st.switch_page("../../pages/change_password.py")
                    elif user_data["role_code"] == "adm": st.switch_page("../../pages/admin_dashboard.py")
                    else: st.switch_page("../../pages/user_dashboard.py")
                else:
                    st.error(f"Validation Failure: {message}")

st.info("💡 Note: The system has been upgraded. For the best experience, please run 'streamlit run app.py' from the root.")
