import sys, os
import streamlit as st # type: ignore

# Setup paths
CWD = os.getcwd()
if CWD not in sys.path: sys.path.insert(0, CWD)
BACKEND_DIR = os.path.join(CWD, "backend")
if BACKEND_DIR not in sys.path: sys.path.insert(0, BACKEND_DIR)

try:
    from styles import SHARED_CSS # type: ignore
    from auth import login_user # type: ignore
except ImportError:
    # Manual fallback for robustness
    sys.path.append(os.path.join(os.getcwd(), "backend"))
    sys.path.append(os.getcwd())
    from styles import SHARED_CSS # type: ignore
    from auth import login_user # type: ignore

st.set_page_config(page_title="CSM Login", page_icon="🏢", layout="centered")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# LOAD ASSETS
logo_path = r"C:\Users\Shanmukh\.gemini\antigravity\brain\c3b5482f-7dac-4b8f-8f4a-837dec3830d4\corporate_messenger_logo_1776631382023.png"
import base64
def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""
logo_b64 = get_b64(logo_path)

# TOP SPACING FIX
st.markdown("<div style='margin-top: -50px;'></div>", unsafe_allow_html=True)

if logo_b64:
    st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_b64}" width="120">
        </div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 2.2rem;'>CORPORATE SMART MESSENGER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: var(--exe-gold) !important; letter-spacing: 2px; font-weight: 600; margin-bottom: 2rem;'>OFFICIAL WORKSPACE PORTAL</p>", unsafe_allow_html=True)

# AUTH SECTION
with st.container():
    st.markdown("### 🔐 Secure Access")
    with st.form("login"):
        login_id = st.text_input("Corporate ID", placeholder="Enter ID")
        password = st.text_input("Access Password", type="password", placeholder="Enter Password")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("VALIDATE & ENTER"):
            if login_id and password:
                success, message, user_data = login_user(login_id, password)
                if success:
                    for k,v in user_data.items(): st.session_state[k] = v
                    st.session_state["logged_in"] = True
                    if not user_data.get("password_changed"): st.switch_page("pages/change_password.py")
                    elif user_data["role"] == "admin": st.switch_page("pages/admin_dashboard.py")
                    else: st.switch_page("pages/user_dashboard.py")
                else:
                    st.error(f"Error: {message}")
            else:
                st.warning("Please provide credentials.")

st.expander("❓ Need Assistance?", expanded=False).write("Contact system administration if you require login ID verification.")