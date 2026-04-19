import sys, os
import streamlit as st # type: ignore

# Path Resolution
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "backend")
if BACKEND not in sys.path: sys.path.insert(0, BACKEND)
if ROOT not in sys.path: sys.path.insert(0, ROOT)

try:
    from styles import SHARED_CSS # type: ignore
    from auth import change_password # type: ignore
except (ImportError, ModuleNotFoundError):
    try:
        from frontend.styles import SHARED_CSS # type: ignore
        from backend.auth import change_password # type: ignore
    except:
        pass

st.set_page_config(page_title="Security Center – CSM", page_icon="🔐", layout="centered", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

if not st.session_state.get("logged_in"): st.switch_page("pages/streamlit_login.py")

st.markdown("<div class='vfx-fade-in'><h1>🔐 Security Protocol</h1></div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='glass-card vfx-glow'>", unsafe_allow_html=True)
    st.markdown("### Update Credentials")
    
    with st.form("pwd_form"):
        curr = st.text_input("Current Global Password", type="password")
        new = st.text_input("New Secure Password", type="password")
        conf = st.text_input("Confirm New Password", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("LOCK IN NEW PASSWORD"):
            if curr and new == conf:
                res, msg = change_password(st.session_state.get("login_id"), curr, new, conf)
                if res:
                    st.success("✅ Protocol Updated!")
                    st.balloons()
                    st.session_state["password_changed"] = True
                    # Dash redirect
                    if st.session_state.get("role") == "admin": st.switch_page("pages/admin_dashboard.py")
                    else: st.switch_page("pages/user_dashboard.py")
                else: st.error(msg)
            else: st.warning("Ensure passwords match.")
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("⬅️ EXIT TO LOGIN"):
    st.session_state.clear()
    st.switch_page("pages/streamlit_login.py")
