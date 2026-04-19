import sys, os # type: ignore
import streamlit as st # type: ignore
import base64 # type: ignore

# Robust IDE-Proof Path Injection
CWD = os.getcwd()
if CWD not in sys.path: sys.path.insert(0, CWD)
BACKEND_DIR = os.path.join(CWD, "backend")
if BACKEND_DIR not in sys.path: sys.path.insert(0, BACKEND_DIR)

try:
    from styles import SHARED_CSS # type: ignore
    from database import get_users_collection, get_registered_users # type: ignore
    from auth import register_user, change_password, DEPARTMENTS, ROLES # type: ignore
    from rag_assistant import answer # type: ignore
except (ImportError, ModuleNotFoundError):
    # Fallback for localized Pylance resolution
    try:
        from frontend.styles import SHARED_CSS # type: ignore
        from backend.database import get_users_collection, get_registered_users # type: ignore
        from backend.auth import register_user, change_password, DEPARTMENTS, ROLES # type: ignore
        from backend.rag_assistant import answer # type: ignore
    except:
        pass # Streamlit handles this at runtime
except ImportError:
    # Fallback to local paths if IDE is struggling
    sys.path.append(os.path.join(os.getcwd(), "backend"))
    sys.path.append(os.getcwd())
    from styles import SHARED_CSS # type: ignore
    from database import get_users_collection, get_registered_users # type: ignore
    from auth import register_user, change_password, DEPARTMENTS, ROLES # type: ignore
    from rag_assistant import answer # type: ignore

# Helper for background
def get_base64_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="Admin Dashboard – CSM", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# LOAD BACKGROUND
bg_path = os.path.join(CWD, "frontend", "assets", "bg.png")
if os.path.exists(bg_path):
    bin_str = get_base64_bin_file(bg_path)
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(10, 14, 26, 0.9), rgba(10, 14, 26, 0.9)), 
                    url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# Auth guard – admins only
if not st.session_state.get("logged_in") or st.session_state.get("role") != "admin":
    st.error("⛔ Unauthorized Access")
    if st.button("Back to Login"): st.switch_page("pages/streamlit_login.py")
    st.stop()

# Initialize session state
if "selected_feature" not in st.session_state: st.session_state["selected_feature"] = None
if "chatbot_messages" not in st.session_state: st.session_state["chatbot_messages"] = []

# Header UI
col_info, col_logout = st.columns([4, 1])
with col_info:
    st.markdown(f"<div class='vfx-fade-in'><h1>🛡️ Master Command Center</h1>", unsafe_allow_html=True)
    st.markdown(f"<p>Admin: <strong>{st.session_state.get('first_name', '')} {st.session_state.get('last_name', '')}</strong> | Secure Workspace</p></div>", unsafe_allow_html=True)

with col_logout:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 SIGN OUT", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/streamlit_login.py")

st.divider()

# ICON-BASED TILE GRID (GLASSMORPHISM)
def admin_tile(label, icon, key, desc):
    st.markdown(f"""
    <div class="glass-card vfx-fade-in" style="text-align: center; padding: 1rem; min-height: 180px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="color: var(--primary-gold); font-weight: 700;">{label}</div>
        <div style="color: var(--text-dim); font-size: 0.8rem;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(f"LAUNCH {label}", key=key, use_container_width=True):
        return True
    return False

r1c1, r1c2, r1c3 = st.columns(3)
r2c1, r2c2, r2c3 = st.columns(3)

with r1c1:
    if admin_tile("MESSAGES", "💬", "adm_msg", "Team Comms"): st.switch_page("pages/messages.py")
with r1c2:
    if admin_tile("CALENDAR", "📅", "adm_cal", "Schedule"): st.switch_page("pages/calendar.py")
with r1c3:
    if admin_tile("AI ANALYST", "🤖", "adm_ai", "Deep Insights"):
        st.session_state["selected_feature"] = "chatbot"; st.rerun()

with r2c1:
    if admin_tile("ADD USER", "👥", "adm_reg", "Onboarding"):
        st.session_state["selected_feature"] = "register"; st.rerun()
with r2c2:
    if admin_tile("TEAM DIRECTORY", "📋", "adm_view", "User Management"):
        st.session_state["selected_feature"] = "view"; st.rerun()
with r2c3:
    if admin_tile("SYSTEM SETTINGS", "⚙️", "adm_set", "Preferences"):
        st.session_state["selected_feature"] = "settings"; st.rerun()

# --- FEATURE DISPLAY ---
st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.get("selected_feature"):
    st.markdown("<div class='glass-card vfx-fade-in vfx-glow'>", unsafe_allow_html=True)
    
    # 🤖 CHATBOT
    if st.session_state["selected_feature"] == "chatbot":
        st.markdown("### 🤖 Admin Intelligence")
        for m in st.session_state["chatbot_messages"]:
            with st.chat_message(m["role"]): st.write(m["content"])
        p = st.chat_input("Query the system...")
        if p:
            st.session_state["chatbot_messages"].append({"role":"user","content":p})
            st.rerun()
        if st.session_state["chatbot_messages"] and st.session_state["chatbot_messages"][-1]["role"] == "user":
            with st.chat_message("assistant"):
                with st.spinner("Processing..."):
                    resp = answer(st.session_state["chatbot_messages"][-1]["content"], st.session_state.get("user_id", ""))
                    st.session_state["chatbot_messages"].append({"role":"assistant","content":resp})
                    st.write(resp); st.rerun()

    # 👥 REGISTER
    elif st.session_state["selected_feature"] == "register":
        st.markdown("### 👥 Employee Registration")
        with st.form("reg_form"):
            c1, c2 = st.columns(2)
            fn = c1.text_input("First Name")
            ln = c1.text_input("Last Name")
            dept = c2.selectbox("Department", options=list(DEPARTMENTS.keys()), format_func=lambda x: DEPARTMENTS[x])
            role = c2.selectbox("Role", options=[r for r in ROLES.keys() if r != "adm"], format_func=lambda x: ROLES[x])
            if st.form_submit_button("CREATE ACCOUNT"):
                if fn and ln:
                    s, m, l_id, pwd = register_user(fn, ln, dept, role)
                    if s: st.success(f"✅ Created: {l_id} (Temp Password: {pwd})")
                    else: st.error(m)
                else: st.warning("Fill all fields")

    # 📋 DIRECTORY
    elif st.session_state["selected_feature"] == "view":
        st.markdown("### 📋 Organizational Directory")
        users = get_registered_users(st.session_state.get("department_code"))
        if users:
            st.table([{"Name": f"{u['first_name']} {u['last_name']}", "ID": u['login_id'], "Role": u.get('role', 'N/A')} for u in users])
        else: st.info("No matching employees.")

    # ⚙️ SETTINGS
    elif st.session_state["selected_feature"] == "settings":
        st.markdown("### ⚙️ Admin Configuration")
        with st.expander("🔐 Security"):
            with st.form("pwd_form"):
                curr = st.text_input("Current", type="password")
                new = st.text_input("New", type="password")
                if st.form_submit_button("CHANGE PWD"):
                    r, msg = change_password(st.session_state.get("login_id"), curr, new, new)
                    if r: st.success(msg)
                    else: st.error(msg)

    if st.button("❌ CLOSE COMPONENT"):
        st.session_state["selected_feature"] = None
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
