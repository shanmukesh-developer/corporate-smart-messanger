import sys, os # type: ignore
import streamlit as st # type: ignore

# Root Protection
ROOT = os.getcwd()
if ROOT not in sys.path: sys.path.insert(0, ROOT)
BACKEND = os.path.join(ROOT, "backend")
if BACKEND not in sys.path: sys.path.insert(0, BACKEND)

try:
    from styles import SHARED_CSS # type: ignore
    from auth import change_password # type: ignore
    from rag_assistant import answer # type: ignore
except:
    st.error("System Core Link Failure")
    st.stop()

st.set_page_config(page_title="Personal Portal – CSM", page_icon="👤", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Auth guard
if not st.session_state.get("logged_in"):
    st.error("⛔ Unauthorized Node")
    if st.button("Disconnect"): st.switch_page("app.py")
    st.stop()

# State
if "selected_feature" not in st.session_state: st.session_state["selected_feature"] = None
if "chatbot_messages" not in st.session_state: st.session_state["chatbot_messages"] = []

# Header
c1, c2, c3 = st.columns([1, 4, 1.2])
with c2:
    st.title("👤 Executive Personnel Portal")
    st.write(f"Identity: **{st.session_state.get('first_name', '')} {st.session_state.get('last_name', '')}** | Node: {st.session_state.get('login_id', 'Unknown')}")

with c3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()

# Navigation Grid
def feature_card(label, icon, key, desc):
    with st.container(border=True):
        st.markdown(f"### {icon} {label}")
        st.write(f"*{desc}*")
        if st.button(f"ENTER {label}", key=key, use_container_width=True):
            return True
    return False

n1, n2, n3 = st.columns(3)
with n1:
    if feature_card("MESSAGES", "⚡", "u_msg", "Secure Chat Protocol"): st.switch_page("pages/messages.py")
with n2:
    if feature_card("SMART SCHEDULE", "🌌", "u_cal", "Neural Workspace Calendar"): st.switch_page("pages/calendar.py")
with n3:
    if feature_card("NEURAL ASSISTANT", "🧠", "u_ai", "Advanced AI Support"):
        st.session_state["selected_feature"] = "chatbot"; st.rerun()

# Feature Display
if st.session_state.get("selected_feature"):
    st.divider()
    feat = st.session_state["selected_feature"]
    
    if feat == "chatbot":
        st.subheader("🧠 Neural Support Interface")
        for m in st.session_state["chatbot_messages"]:
            with st.chat_message(m["role"]): st.write(m["content"])
        p = st.chat_input("Query workspace intelligence...")
        if p:
            st.session_state["chatbot_messages"].append({"role":"user","content":p})
            st.rerun()
        if st.session_state["chatbot_messages"] and st.session_state["chatbot_messages"][-1]["role"] == "user":
            with st.chat_message("assistant"):
                with st.spinner("Decoding nodes..."):
                    resp = answer(st.session_state["chatbot_messages"][-1]["content"], st.session_state.get("login_id", ""))
                    st.session_state["chatbot_messages"].append({"role":"assistant","content":resp})
                    st.write(resp); st.rerun()

    if st.button("❌ TERMINATE LAYER", use_container_width=True):
        st.session_state["selected_feature"] = None
        st.rerun()