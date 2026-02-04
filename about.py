import streamlit as st
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=1074&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Demo App", page_icon="📄", layout="centered")

st.title("Welcome to My App")

# Main page button
if st.button("About"):
    st.session_state.show_about = True

# Show content based on button click
if 'show_about' in st.session_state and st.session_state.show_about:
    st.subheader("About This App")
    st.write("""
    This is a demo Streamlit application.
    
    - It shows how to navigate content using buttons.
    - You can display text, images, or even other pages.
    - Built using Streamlit!
    """)
st.markdown("""
<div style="text-align: left; margin-bottom: 20px;">
    <a href="../app" style="
        background-color: #2563eb;
        color: white;
        padding: 8px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.25s ease-in-out;
    "
    onmouseover="this.style.backgroundColor='#1d4ed8'"
    onmouseout="this.style.backgroundColor='#2563eb'">
        ⬅ Home
    </a>
</div>
""", unsafe_allow_html=True)