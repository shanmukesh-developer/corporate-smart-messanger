import sys, os # type: ignore
import streamlit as st # type: ignore

# Root Protection
ROOT = os.getcwd()
if ROOT not in sys.path: sys.path.insert(0, ROOT)
BACKEND = os.path.join(ROOT, "backend")
if BACKEND not in sys.path: sys.path.insert(0, BACKEND)

try:
    from styles import SHARED_CSS # type: ignore
    from database import get_user_conversations, get_messages, send_message # type: ignore
    from streamlit_autorefresh import st_autorefresh # type: ignore
except:
    st.error("System Core Link Failure")
    st.stop()

st.set_page_config(page_title="Messages – CSM", page_icon="💬", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Auth guard
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

current_user_id = st.session_state.get("login_id")
st_autorefresh(interval=15000, key="chat_refresh")

# Header
col_back, col_title = st.columns([1, 5])
with col_back:
    if st.button("⬅️ BACK", use_container_width=True):
        if st.session_state.get("role_code") == "adm": st.switch_page("pages/admin_dashboard.py")
        else: st.switch_page("pages/user_dashboard.py")

st.title("⚡ Secure Global Communications")
st.divider()

# Structure
conversations = get_user_conversations(current_user_id)
c_list, c_win = st.columns([1, 2.5])

with c_list:
    st.write("### 👥 Active Channels")
    for conv in conversations:
        name = conv.get("name", "Direct Message")
        if st.button(f"👤 {name}", key=f"btn_{conv['_id']}", use_container_width=True):
            st.session_state["active_conv"] = str(conv["_id"])
            st.rerun()

with c_win:
    active_id = st.session_state.get("active_conv")
    if active_id:
        st.write("### 💬 Workspace Channel")
        msg_list = get_messages(active_id)
        with st.container(border=True):
            for m in msg_list:
                role = "user" if m["sender_id"] == current_user_id else "assistant"
                with st.chat_message(role):
                    st.write(f"**{m.get('sender_name', m['sender_id'])}**")
                    st.markdown(m['content'])
        
        with st.form("msg_send", clear_on_submit=True):
            txt = st.text_input("Enter secure encryption...", placeholder="Data signal input...")
            if st.form_submit_button("VALIDATE & TRANSMIT"):
                if txt:
                    send_message(active_id, current_user_id, txt) # type: ignore
                    st.rerun()
    else:
        st.info("Select a secure channel to begin transmission.")
