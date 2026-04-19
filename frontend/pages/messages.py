import sys, os
import streamlit as st # type: ignore
import base64 # type: ignore
from datetime import timezone, datetime

# Robust IDE-Proof Path Injection
CWD = os.getcwd()
if CWD not in sys.path: sys.path.insert(0, CWD)
BACKEND_DIR = os.path.join(CWD, "backend")
if BACKEND_DIR not in sys.path: sys.path.insert(0, BACKEND_DIR)

try:
    from styles import SHARED_CSS
    from database import (
        get_user_conversations, get_messages, send_message, 
        get_all_users_for_chat, get_or_create_direct_conversation, 
        create_group_conversation, get_registered_users
    )
    from streamlit_autorefresh import st_autorefresh # type: ignore
except (ImportError, ModuleNotFoundError):
    try:
        from frontend.styles import SHARED_CSS
        from backend.database import (
            get_user_conversations, get_messages, send_message, 
            get_all_users_for_chat, get_or_create_direct_conversation, 
            create_group_conversation, get_registered_users
        )
        from streamlit_autorefresh import st_autorefresh # type: ignore
    except:
        pass

# Helper for background
def get_base64_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="Messages - CSM", page_icon="💬", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# LOAD BACKGROUND# BG VFX
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
    /* MASTERPIECE CHAT UI */
    .whatsapp-container {{ 
        display: flex; height: 80vh; 
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px; 
        overflow: hidden; 
    }}
    .chat-list {{ 
        width: 350px; border-right: 1px solid rgba(255, 255, 255, 0.1); 
        background: rgba(0, 0, 0, 0.2); 
        overflow-y: auto; 
    }}
    .chat-window {{ flex-grow: 1; background: transparent; display: flex; flex-direction: column; }}
    .chat-header {{ 
        padding: 1.2rem; background: rgba(212, 175, 55, 0.1); 
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        color: var(--primary-gold); font-weight: 700;
    }}
    .chat-messages {{ 
        flex-grow: 1; padding: 1.5rem; overflow-y: auto; 
        background: rgba(10, 14, 26, 0.4); 
    }}
    .chat-item {{ 
        padding: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); 
        cursor: pointer; transition: all 0.3s;
    }}
    .chat-item:hover {{ background: rgba(212, 175, 55, 0.05); transform: translateX(5px); }}
    .chat-item.active {{ background: rgba(212, 175, 55, 0.15); border-left: 4px solid var(--primary-gold); }}
    
    .msg-user {{ 
        background: linear-gradient(135deg, var(--primary-gold), var(--dark-gold)) !important; 
        color: white !important; border-radius: 15px 15px 0 15px !important;
        margin-left: auto; max-width: 70%; padding: 0.8rem; margin-bottom: 1rem;
    }}
    .msg-other {{ 
        background: rgba(255,255,255,0.1) !important; 
        color: white !important; border-radius: 15px 15px 15px 0 !important;
        margin-right: auto; max-width: 70%; padding: 0.8rem; margin-bottom: 1rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# Auth guard
if not st.session_state.get("logged_in"): st.switch_page("pages/streamlit_login.py")

# Autorefresh (Masterpiece mode: silent and efficient)
st_autorefresh(interval=10000, key="chat_refresh")

current_user_id = st.session_state.get("login_id")

col_back, col_title = st.columns([1, 5])
with col_back:
    if st.button("⬅️ BACK"):
        if st.session_state.get("role") == "admin": st.switch_page("pages/admin_dashboard.py")
        else: st.switch_page("pages/user_dashboard.py")

st.markdown("<div class='vfx-fade-in'><h1>💬 Secure Messaging</h1></div>", unsafe_allow_html=True)

# Main App Logic
conversations = get_user_conversations(current_user_id)

with st.container():
    c_list, c_win = st.columns([1, 2])
    
    with c_list:
        st.markdown("<div class='chat-list'>", unsafe_allow_html=True)
        st.write("### Conversations")
        selected_conv = None
        for conv in conversations:
            name = conv.get("name", "Individual Chat")
            is_active = st.session_state.get("active_conv") == str(conv["_id"])
            active_cls = "active" if is_active else ""
            if st.button(f"👤 {name}", key=f"btn_{conv['_id']}", use_container_width=True):
                st.session_state["active_conv"] = str(conv["_id"])
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c_win:
        active_id = st.session_state.get("active_conv")
        if active_id:
            msg_list = get_messages(active_id)
            st.markdown(f"<div class='chat-header'>Workspace Channel</div>", unsafe_allow_html=True)
            
            chat_area = st.container()
            with chat_area:
                for m in msg_list:
                    role = "user" if m["sender_id"] == current_user_id else "assistant"
                    with st.chat_message(role):
                        st.markdown(f"**{m['sender_name']}**: {m['content']}")
            
            with st.form("msg_send", clear_on_submit=True):
                txt = st.text_input("Type a message...", key="msg_input")
                if st.form_submit_button("SEND"):
                    if txt:
                        send_message(active_id, current_user_id, txt) # type: ignore
                        st.rerun()
        else:
            st.info("Select a conversation to start messaging.")
