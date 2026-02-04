from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st
import tensorflow as tf
import numpy as np
import time
from datetime import datetime
import io

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Symptoms Based Detection",
    page_icon="🐄",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=1074&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* FULL WIDTH CHECKBOX */
div[data-testid="stCheckbox"] {
    width: 100%;
}

div[data-testid="stCheckbox"] input {
    display: none !important;
}

div[data-testid="stCheckbox"] svg {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

div[data-testid="stCheckbox"] label {
    width: 100%;
    cursor: pointer;
}

div[data-testid="stCheckbox"] label > div {
    width: 100%;
    background: #e0f2f1;
    padding: 18px 22px;
    border-radius: 16px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 16px;
    font-size: 17px;
    font-weight: 500;
    color: #0f172a;
    transition: all 0.25s ease;
    border: 2px solid transparent;
}

div[data-testid="stCheckbox"] label > div:hover {
    background: #ccfbf1;
}

div[data-testid="stCheckbox"] label > div::before {
    content: none !important;
}

div[data-testid="stCheckbox"] input:checked + div {
    background: #22c55e;
    color: #ffffff;
    border-color: #16a34a;
}

/* BUTTON STYLING */
.stButton > button {
    background-color: #2563eb;
    color: white;
    font-size: 18px;
    padding: 10px 25px;
    border-radius: 10px;
    transition: all 0.25s ease-in-out;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);   /* slight lift */
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
    background-color: #1d4ed8;                 /* darker blue */
}

/* DOWNLOAD BUTTON SPECIFIC */
button[kind="secondary"] {
    transition: all 0.25s ease-in-out;
}

button[kind="secondary"]:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
    background-color: #16a34a !important;      /* green hover */
    color: white !important;
}

.title-text {
    text-align: center;
    font-size: 40px;
    font-weight: 700;
    color: white;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #e5e7eb;
    margin-bottom: 30px;
}

.info-box {
    background: #f1f5f9;
    color: #1f2937;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
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
st.markdown('<div class="title-text">📋 Symptoms-Based Mastitis Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Detect mastitis based on observed clinical symptoms</div>', unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = tf.keras.models.load_model("symptom1_model.h5")

# ---------------- SYMPTOMS CHECKBOXES ----------------
st.subheader("✔ Select Observed Symptoms")

symptoms_labels = [
    "Redness in Udder",
    "Swelling",
    "Hardness",
    "Fever",
    "Low Milk Yield",
    "Clots in Milk"
]

cols = st.columns(3)
symptoms = []

for i, label in enumerate(symptoms_labels):
    with cols[i % 3]:
        symptoms.append(st.checkbox(label, key=f"s{i}"))

# ---------------- PREDICTION AND PDF ----------------
if st.button("🔍 Predict"):
    if any(symptoms):  # <-- Check if at least one symptom is selected
        with st.spinner("Analyzing symptoms..."):
            time.sleep(1.2)
            data = np.array(symptoms, dtype=int).reshape(1, 6)
            pred = model.predict(data)[0][0]

            date_time = datetime.now().strftime("%d-%m-%Y %H:%M")

            if pred > 0.5:
                result = "Mastitis Detected"
                message = "Immediate veterinary consultation is advised."
                st.error("⚠ Mastitis Detected")
            else:
                result = "Healthy Cow"
                message = "Continue regular monitoring of the cow’s health."
                st.success("✅ Healthy Cow")

            # ---------------- DISPLAY EXPLANATION ----------------
            st.markdown(f"""
            <div class="info-box">
            <b>Explanation:</b><br>{message}
            </div>
            """, unsafe_allow_html=True)

            # ---------------- CREATE PDF ----------------
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            c.setFont("Helvetica-Bold", 22)
            c.drawCentredString(A4[0]/2, 800, "Mastitis Detection Report")
            c.setFont("Helvetica", 14)
            c.drawString(50, 760, f"Date & Time: {date_time}")
            c.drawString(50, 740, f"Result: {result}")
            c.drawString(50, 720, f"Message: {message}")

            observed = [symptoms_labels[i] for i, val in enumerate(symptoms) if val]
            if observed:
                c.drawString(50, 700, "Symptoms Observed:")
                y = 680
                for sym in observed:
                    c.drawString(70, y, f"- {sym}")
                    y -= 20
            else:
                c.drawString(50, 700, "Symptoms Observed: None")

            c.showPage()
            c.save()
            buffer.seek(0)

            # ---------------- DOWNLOAD BUTTON ----------------
            st.download_button(
                label="📄 Download Report",
                data=buffer,
                file_name="mastitis_detection_report.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("⚠ Please select at least one symptom to check for Mastitis.")

