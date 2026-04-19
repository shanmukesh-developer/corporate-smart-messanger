import sys, os # type: ignore
import streamlit as st # type: ignore

# Root Protection
ROOT = os.getcwd()
if ROOT not in sys.path: sys.path.insert(0, ROOT)

try:
    from styles import SHARED_CSS # type: ignore
    from auth import change_password # type: ignore
except:
    pass

st.set_page_config(page_title="Security – CSM", page_icon="🛡️", layout="centered", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Auth guard
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.title("🛡️ Security Protocol")
st.divider()

with st.container(border=True):
    st.subheader("🔐 Credential Override")
    with st.form("security_form"):
        curr = st.text_input("Active Key", type="password")
        new = st.text_input("New Node Key", type="password")
        confirm = st.text_input("Confirm New Key", type="password")
        if st.form_submit_button("VALIDATE & COMMIT"):
            if new == confirm:
                success, message = change_password(st.session_state.get("login_id"), curr, new, confirm)
                if success:
                    st.success("Protocol Updated.")
                    if st.session_state.get("role_code") == "adm": st.switch_page("pages/admin_dashboard.py")
                    else: st.switch_page("pages/user_dashboard.py")
                else: st.error(message)
            else: st.error("Keys do not match.")

if st.button("⬅️ DISCONNECT"):
    st.session_state.clear()
    st.switch_page("app.py")
