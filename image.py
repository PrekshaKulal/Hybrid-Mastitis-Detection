import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Mastitis Detection",
    layout="wide",
    page_icon="🐄"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
            
.stApp {
    background-image: url("https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
           



.title-text {
    text-align: center;
    font-size: 40px;
    font-weight: 700;
    color: #F2F3F6FF;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #F2F3F6FF1;
    margin-bottom: 30px;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    font-size: 18px;
    padding: 10px 25px;
    border-radius: 10px;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}

.info-box {
    background: #f1f5f9;
    color: #1f2937;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    font-size: 16px;
}
            /* Smooth transition for all buttons */
.stButton > button {
    transition: all 0.25s ease-in-out;
}

/* Hover effect */
.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);   /* slight lift */
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
    background-color: #1d4ed8;                 /* darker blue */
}

/* Download button specific styling */
button[kind="secondary"] {
    transition: all 0.25s ease-in-out;
}

button[kind="secondary"]:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
    background-color: #16a34a !important;      /* green hover */
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MAIN CARD ----------------
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

st.markdown('<div class="title-text">🖼 Image-Based Mastitis Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Detect mastitis from udder images using CNN model</div>', unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = tf.keras.models.load_model("final_cnn_model1.h5")

# ---------------- IMAGE PREPROCESS ----------------
def preprocess_image(img, model_input_shape):
    img = img.resize((model_input_shape[1], model_input_shape[2]))
    channels = model_input_shape[-1]

    if channels == 1:
        img = img.convert("L")
        arr = np.array(img) / 255.0
        arr = arr.reshape(1, model_input_shape[1], model_input_shape[2], 1)
    else:
        img = img.convert("RGB")
        arr = np.array(img) / 255.0
        arr = arr.reshape(1, model_input_shape[1], model_input_shape[2], 3)

    return arr

# ---------------- PDF REPORT ----------------
def generate_pdf_report(result, confidence):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<b>Mastitis Detection Report</b>", styles["Title"]))
    content.append(Spacer(1, 20))

    content.append(Paragraph("<b>Detection Type:</b> Image-Based Detection", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Prediction Result:</b> {result}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Confidence:</b> {confidence:.2f}%", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "<b>Recommendation:</b> Please consult a veterinary professional for confirmation and treatment.",
        styles["Normal"]
    ))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        f"<b>Date & Time:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
        styles["Normal"]
    ))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ---------------- IMAGE UPLOAD ----------------
uploaded = st.file_uploader(
    "📤 Upload Udder Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", use_column_width=True)

# ---------------- PREDICTION ----------------
if st.button("🔍 Predict"):
    if uploaded is None:
        st.warning("Please upload an image first.")
    else:
        with st.spinner("Analyzing image using CNN model..."):
            time.sleep(1.5)

            try:
                arr = preprocess_image(img, model.input_shape)
                pred = model.predict(arr)[0][0]

                mastitis_conf = pred * 100
                healthy_conf = (1 - pred) * 100

                st.markdown("### 🔎 Prediction Confidence")

                if pred > 0.5:
                    st.progress(int(mastitis_conf))
                    st.error(f"⚠ Mastitis Detected\n\nConfidence: {mastitis_conf:.2f}%")

                    st.markdown("""
                    <div class="info-box">
                    <b>Explanation:</b><br>
                    The model detected visual patterns associated with mastitis such as inflammation
                    and texture abnormalities in the udder region.
                    <br><br>
                    <b>Recommended Action:</b><br>
                    Immediate veterinary consultation is advised.
                    </div>
                    """, unsafe_allow_html=True)

                    pdf = generate_pdf_report("Mastitis Detected", mastitis_conf)

                else:
                    st.progress(int(healthy_conf))
                    st.success(f"✅ Healthy Udder\n\nConfidence: {healthy_conf:.2f}%")

                    st.markdown("""
                    <div class="info-box">
                    <b>Explanation:</b><br>
                    No visible symptoms of mastitis were detected in the uploaded image.
                    <br><br>
                    <b>Note:</b><br>
                    Regular monitoring is recommended.
                    </div>
                    """, unsafe_allow_html=True)

                    pdf = generate_pdf_report("Healthy Udder", healthy_conf)

                st.download_button(
                    label="📄 Download Report",
                    data=pdf,
                    file_name="mastitis_detection_report.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Prediction failed: {e}")


