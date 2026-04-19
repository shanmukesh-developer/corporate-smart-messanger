import sys, os
import streamlit as st # type: ignore

# Enhanced Path Resolution for broad compatibility
CWD = os.getcwd()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "backend")
if BACKEND not in sys.path: sys.path.insert(0, BACKEND)
if ROOT not in sys.path: sys.path.insert(0, ROOT)
if CWD not in sys.path: sys.path.insert(0, CWD)

try:
    from styles import SHARED_CSS # type: ignore
    from auth import login_user # type: ignore
except ImportError:
    # Fallback for complex IDE environments
    sys.path.append(os.path.join(os.getcwd(), "backend"))
    sys.path.append(os.getcwd())
    from styles import SHARED_CSS # type: ignore
    from auth import login_user # type: ignore

st.set_page_config(
    page_title="Corporate Smart Messenger",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(SHARED_CSS, unsafe_allow_html=True)

# LOAD BACKGROUND
bg_path = r"C:\Users\Shanmukh\.gemini\antigravity\brain\c3b5482f-7dac-4b8f-8f4a-837dec3830d4\premium_corporate_background_1776631368914.png"
logo_path = r"C:\Users\Shanmukh\.gemini\antigravity\brain\c3b5482f-7dac-4b8f-8f4a-837dec3830d4\corporate_messenger_logo_1776631382023.png"

import base64
def img_to_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

bg_b64 = img_to_b64(bg_path)
logo_b64 = img_to_b64(logo_path)

if bg_b64:
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(10, 14, 26, 0.8), rgba(10, 14, 26, 0.8)), 
                    url("data:image/png;base64,{bg_b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# Redirect if already logged in
if st.session_state.get("logged_in"):
    if st.session_state.get("role") == "admin":
        st.switch_page("pages/admin_dashboard.py")
    else:
        st.switch_page("pages/user_dashboard.py")

# Main Container
st.markdown("<div class='vfx-fade-in'>", unsafe_allow_html=True)

if logo_b64:
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 0;">
            <img src="data:image/png;base64,{logo_b64}" width="120" class="vfx-pulse">
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<h1 style='font-size: 3rem; margin-bottom: 0; text-align: center;'>🏢 CSM</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; margin-bottom: 2rem; color: var(--primary-gold); letter-spacing: 2px; font-weight: 600;'>CORPORATE SMART MESSENGER</p>", unsafe_allow_html=True)

# Login Card
with st.container():
    st.markdown("<div class='glass-card vfx-glow'>", unsafe_allow_html=True)
    
    st.markdown("### 🔐 Secure Login")
    
    with st.form("login_form", clear_on_submit=False):
        login_id = st.text_input("Corporate ID", placeholder="e.g., devadm000001")
        password = st.text_input("Secure Password", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("ENTER WORKSPACE")
        
        if submitted:
            if login_id and password:
                success, message, user_data = login_user(login_id, password)
                if success and user_data:
                    for k, v in user_data.items():
                        st.session_state[k] = v
                    st.session_state["logged_in"] = True
                    st.session_state["login_toast"] = True
                    
                    if not user_data.get("password_changed"):
                        st.switch_page("pages/change_password.py")
                    elif user_data["role"] == "admin":
                        st.switch_page("pages/admin_dashboard.py")
                    else:
                        st.switch_page("pages/user_dashboard.py")
                else:
                    st.error(f"❌ {message}")
            else:
                st.warning("⚠️ Please provide all credentials.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Footer Help
with st.expander("❓ Need Help with Login ID?"):
    st.markdown("""
    Your Login ID is generated based on your Department and Role.
    - **Format**: `[Dept][Role][Number]` (e.g., `devadm000001`)
    - Contact HR if you haven't received your credentials.
    """)