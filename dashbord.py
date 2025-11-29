import time
import streamlit as st
import google.generativeai as genai


# Setup API and model
MY_API_KEY = " API_ key "
genai.configure(api_key=MY_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")


# Sidebar area with controls and info
with st.sidebar:
    st.title("Settings Panel")

    dark_mode_enabled = st.checkbox("Use Dark Theme", value=False, help="Toggle between dark and light modes")

    st.button("Profile")
    reload_pressed = st.button("Clear Chat")
    history_pressed = st.button("Session History")
    st.button("Settings")
    help_pressed = st.button("Help Center")

    st.write("Created by Priyansh Kharol - Dashboard v1.0")

    # Clear chat data on reload
    if reload_pressed:
        if "chat_log" in st.session_state:
            st.session_state.chat_log.clear()
        if "resp_times" in st.session_state:
            st.session_state.resp_times.clear()
        st.experimental_rerun()

    # Show chat history when requested
    if history_pressed:
        st.markdown("## Chat History")
        logs = st.session_state.get("chat_log", [])
        if logs:
            for speaker, txt in logs:
                label = "User" if speaker == "User" else "Bot"
                st.write(f"**{label}:** {txt}")
        else:
            st.info("No chat history found.")

    # Show help info 
    if help_pressed:
        st.markdown("## Contact Information")
        st.markdown("Email: [priyanshkharol2396@gmail.com](Mail to:priyanshkharol2396@gmail.com)  ")
        st.markdown("Mobile: +910000000000")


# Define CSS for dark and light theme with smaller differences
DARK_STYLE = """
<style>
body, .css-18e3th9 {
    background-color: #1a1a1a;
    color: #ccc;
}
.reportview-container .sidebar-content {
    background-color: #121212;
    color: #eee;
    font-weight: 600;
}
.chatbox {
    background-color: #333333;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 12px;
    color: #ddd;
    max-width: 75%;
}
.bot-message {
    color: #99bbff;
    font-weight: 600;
    margin-left: auto;
}
.user-message {
    color: #99cc99;
    font-weight: 600;
}
button[kind="primary"]:hover {
    background-color: #5577ee !important;
}
</style>
"""

LIGHT_STYLE = """
<style>
body, .css-18e3th9 {
    background-color: #fafafa;
    color: #222222;
}
.reportview-container .sidebar-content {
    background-color: #003366;
    color: white;
    font-weight: 600;
}
.chatbox {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 12px;
    color: #222;
    max-width: 75%;
}
.bot-message {
    color: #004099;
    font-weight: 600;
    margin-left: auto;
}
.user-message {
    color: #008800;
    font-weight: 600;
}
button[kind="primary"]:hover {
    background-color: #0066cc !important;
}
</style>
"""

st.markdown(DARK_STYLE if dark_mode_enabled else LIGHT_STYLE, unsafe_allow_html=True)


# Main Title 
st.title("Chatbot Application")
st.info("Type your question below and hit send.......")


#  chat log and response times
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "resp_times" not in st.session_state:
    st.session_state.resp_times = []


#  user input
with st.form("chat_input", clear_on_submit=True):
    user_text = st.text_input("Ask me anything.....")
    submit_clicked = st.form_submit_button("Send")


# When send pressed, get response and record timings
if submit_clicked:
    if not user_text.strip():
        st.warning("Input cannot be empty. Please type a message.")
    else:
        start = time.time()
        answer = gemini_model.generate_content(user_text)
        end = time.time()
        duration = end - start
        st.session_state.resp_times.append(duration)

        st.session_state.chat_log.append(("User", user_text))
        st.session_state.chat_log.append(("Bot", answer.text))


# Display chat log with style
for role, content in st.session_state.chat_log:
    css_cls = "bot-message" if role == "Bot" else "user-message"
    st.markdown(f'<div class="chatbox {css_cls}">{content}</div>', unsafe_allow_html=True)


# Display average response time to user
if st.session_state.resp_times:
    avg = sum(st.session_state.resp_times) / len(st.session_state.resp_times)
    st.markdown(f"Average reply time: {avg:.2f} seconds")
