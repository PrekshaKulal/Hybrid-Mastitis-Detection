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
st.set_page_config(page_title="Contact Us", page_icon="📞", layout="centered")

st.title("Contact Us")

st.write("""
Get in touch with us through the following details:
""")

# Your Contact Information
st.markdown("""
**Company Name:** My Demo App  
**Address:** 123, Demo Street, City, Country  
**Email:** contact@demoapp.com  
**Phone:** +91 12345 67890  
**Website:** [www.demoapp.com](https://www.demoapp.com)
""")

# Optional: Social Media Links
st.markdown("""
**Follow us on:**  
[Twitter](https://twitter.com/) | [LinkedIn](https://linkedin.com/) | [Facebook](https://facebook.com/)
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