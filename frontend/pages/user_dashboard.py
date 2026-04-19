import sys, os
import streamlit as st # type: ignore
import base64

# Robust IDE-Proof Path Injection
CWD = os.getcwd()
if CWD not in sys.path: sys.path.insert(0, CWD)
BACKEND_DIR = os.path.join(CWD, "backend")
if BACKEND_DIR not in sys.path: sys.path.insert(0, BACKEND_DIR)

try:
    from styles import SHARED_CSS # type: ignore
    from auth import change_password # type: ignore
    from rag_assistant import answer # type: ignore
except (ImportError, ModuleNotFoundError):
    try:
        from frontend.styles import SHARED_CSS # type: ignore
        from backend.auth import change_password # type: ignore
        from backend.rag_assistant import answer # type: ignore
    except:
        pass
except ImportError:
    # Manual fallback for IDE visibility
    sys.path.append(os.path.join(os.getcwd(), "backend"))
    sys.path.append(os.getcwd())
    from styles import SHARED_CSS
    from auth import change_password
    from rag_assistant import answer

# Helper for background
def get_base64_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="User Dashboard – CSM", page_icon="💬", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# BG VFX
bg_path = os.path.join(CWD, "frontend", "assets", "bg.png")
if os.path.exists(bg_path):
    bin_str = get_base64_bin_file(bg_path)
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(10, 14, 26, 0.85), rgba(10, 14, 26, 0.85)), 
                    url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# Auth guard
if not st.session_state.get("logged_in"):
    st.switch_page("pages/streamlit_login.py")

# Session state initialization
if "selected_feature" not in st.session_state: st.session_state["selected_feature"] = None
if "chatbot_messages" not in st.session_state: st.session_state["chatbot_messages"] = []

# Header UI
col_info, col_logout = st.columns([4, 1])
with col_info:
    st.markdown(f"<div class='vfx-fade-in'><h1>Welcome, {st.session_state.get('first_name', 'User')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>{st.session_state.get('department', 'General')}</strong> | {st.session_state.get('role', 'Member')}</p></div>", unsafe_allow_html=True)

with col_logout:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/streamlit_login.py")

st.divider()

# ICON-BASED TILE GRID (GLASSMORPHISM)
def feature_tile(label, icon, key):
    st.markdown(f"""
    <div class="glass-card vfx-fade-in" style="text-align: center; padding: 1.5rem; height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="color: var(--primary-gold); font-weight: 700; font-size: 1.2rem;">{label}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(f"OPEN {label}", key=key, use_container_width=True):
        return True
    return False

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    if feature_tile("MESSAGES", "💬", "btn_msg"): st.switch_page("pages/messages.py")
with row1_col2:
    if feature_tile("CALENDAR", "📅", "btn_cal"): st.switch_page("pages/calendar.py")
with row2_col1:
    if feature_tile("AI ASSISTANT", "🤖", "btn_ai"):
        st.session_state["selected_feature"] = "chatbot"
        st.rerun()
with row2_col2:
    if feature_tile("SETTINGS", "⚙️", "btn_set"):
        st.session_state["selected_feature"] = "settings"
        st.rerun()

# --- FEATURE DISPLAY ---
st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.get("selected_feature") == "chatbot":
    st.markdown("<div class='glass-card vfx-fade-in'>", unsafe_allow_html=True)
    st.markdown("### 🤖 CSM Intelligence")
    for m in st.session_state["chatbot_messages"]:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    prompt = st.chat_input("Ask about company processes or tasks...")
    if prompt:
        st.session_state["chatbot_messages"].append({"role": "user", "content": prompt})
        st.rerun()
    
    if st.session_state["chatbot_messages"] and st.session_state["chatbot_messages"][-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Analyzing Workspace..."):
                response = answer(st.session_state["chatbot_messages"][-1]["content"], st.session_state.get("user_id", ""))
                st.session_state["chatbot_messages"].append({"role": "assistant", "content": response})
                st.write(response)
                st.rerun()

    if st.button("❌ CLOSE ASSISTANT"):
        st.session_state["selected_feature"] = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.get("selected_feature") == "settings":
    st.markdown("<div class='glass-card vfx-fade-in'>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Account Preferences")
    
    with st.expander("🔑 Password Management"):
        with st.form("pwd_form"):
            curr = st.text_input("Current Password", type="password")
            new = st.text_input("New Password", type="password")
            conf = st.text_input("Confirm", type="password")
            if st.form_submit_button("UPDATE PASSWORD"):
                if curr and new == conf:
                    res, msg = change_password(st.session_state.get("login_id"), curr, new, conf)
                    if res: st.success(msg)
                    else: st.error(msg)
                else: st.warning("Check inputs")

    if st.button("❌ CLOSE SETTINGS"):
        st.session_state["selected_feature"] = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)