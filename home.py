import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CATTLE DISEASE DETECTION SYSTEM",
    page_icon="🐄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    
    /* Apply font to entire app */
    .stApp {
        font-family: 'Roboto', sans-serif;
        background-image: url("https://images.unsplash.com/photo-1498191923457-88552caeccb3?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF;
    }

    /* Navbar */
    .navbar a {
        color: white;
        text-decoration: none;
        margin-left: 2rem;
        font-size: 16px;
    }
    .navbar a:hover {
        text-decoration: underline;
    }

    /* Remove Streamlit's default top padding */
.css-18e3th9 {   /* Main app container */
    padding-top: 0rem;
}

.css-1d391kg {   /* Page content spacing (varies by Streamlit version) */
    padding-top: 0rem;
}

    /* Header */
.header {
    text-align: center;
    margin-top: 0px;  /* Reduced from 100px to 40px */
    color: white;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.7);
}
.header h1 {
    font-size: 50px;
}
.header p {
    font-size: 20px;
}


    /* Cards/buttons */
div.stButton > button {
    background: rgba(255,255,255,0.6);  /* Slightly opaque */
    color: #000000;                      /* Dark text for contrast */
    border-radius: 20px;
    padding: 2rem;                       /* Reduced padding */
    width: 100%;
    height: 200px;                       /* Reduced height */
    border: none;
    box-shadow: 0 6px 15px rgba(0,0,0,0.3);
    transition: 0.3s;
    text-align: center;
    font-family: 'Roboto', sans-serif;
}

div.stButton > button p {
    font-size: 20px;                     /* Reduced font size */
    font-weight: bold;
    line-height: 1.3;
}

/* Hover effect in light green */
div.stButton > button:hover {
    background: rgba(144, 238, 144, 0.8);  /* Light green */
    color: #000000;                        /* Dark text on hover */
    transform: translateY(-5px);           /* Slightly smaller lift on hover */
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}


    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- NAVBAR ----------------
st.markdown("""
<div style="display: flex; justify-content: flex-end; gap: 20px; margin-bottom: 30px;">
    <a href="app" style="text-decoration: none; color: #000000; font-weight: 500;">Home</a>
    <a href="about" style="text-decoration: none; color: #000000; font-weight: 500;">About</a>
    <a href="contact" style="text-decoration: none; color: #000000; font-weight: 500;">Contact</a>
</div>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown(
    """
    <div class="header">
        <h1>CATTLE DISEASE DETECTION SYSTEM</h1>
        <p>Detect diseases in cattle using images, symptoms, or a hybrid approach.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# ---------------- CARDS (CORRECT NAVIGATION) ----------------
st.markdown(
    """
    <div style="margin-top: 10px;">  <!-- Adjust this value to move cards down -->
        <div style="display: flex; gap: 20px;">
            <div style="flex: 1;"></div>
            <div style="flex: 1;"></div>
            <div style="flex: 1;"></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<br><br><br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🖼️ Image Detection\n\nUpload images of cattle to detect diseases"):
        st.switch_page("pages/image.py")

with col2:
    if st.button("🩺 Symptoms Detection\n\nEnter observed symptoms to predict disease"):
        st.switch_page("pages/symptoms.py")

with col3:
    if st.button("🔀 Hybrid Detection\n\nUpload Image and Enter the symptoms"):
        st.switch_page("pages/hybrid.py")
