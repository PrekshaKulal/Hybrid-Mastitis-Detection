import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Hybrid Mastitis Detection",
    layout="wide",
    page_icon="🔀"
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

st.markdown('<div class="title-text">🔀 Hybrid Mastitis Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Detect mastitis using both image and symptom inputs</div>', unsafe_allow_html=True)

# ---------------- LOAD MODELS ----------------
cnn_model = tf.keras.models.load_model("final_cnn_model1.h5")
symptom_model = tf.keras.models.load_model("symptom1_model.h5")

# ---------------- IMAGE UPLOAD ----------------
uploaded = st.file_uploader("📤 Upload Udder Image", type=["jpg", "jpeg", "png"])
if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", use_column_width=True)

# ---------------- SYMPTOMS CHECKBOXES ----------------
st.subheader("✔ Select Observed Symptoms")
symptoms_labels = ["Redness in Udder","Swelling","Hardness","Fever","Low Milk Yield","Clots in Milk"]
cols = st.columns(3)
symptoms = []
for i, label in enumerate(symptoms_labels):
    with cols[i % 3]:
        symptoms.append(st.checkbox(label, key=f"s{i}"))

# ---------------- IMAGE PREPROCESS ----------------
def preprocess_image(img, model_input_shape):
    img = img.resize((model_input_shape[1], model_input_shape[2]))
    channels = model_input_shape[-1]
    if channels == 1:
        img = img.convert("L")
        arr = np.array(img)/255.0
        arr = arr.reshape(1, model_input_shape[1], model_input_shape[2], 1)
    elif channels == 3:
        img = img.convert("RGB")
        arr = np.array(img)/255.0
        arr = arr.reshape(1, model_input_shape[1], model_input_shape[2], 3)
    else:
        raise ValueError(f"Unsupported channels: {channels}")
    return arr

# ---------------- PDF REPORT ----------------
def generate_pdf_report(final_result, img_pred, sym_pred, final_pred, selected_symptoms):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []
    
    content.append(Paragraph("<b>Hybrid Mastitis Detection Report</b>", styles["Title"]))
    content.append(Spacer(1,20))
    content.append(Paragraph(f"<b>Image-Based Prediction:</b> {img_pred*100:.2f}%", styles["Normal"]))
    content.append(Paragraph(f"<b>Symptoms-Based Prediction:</b> {sym_pred*100:.2f}%", styles["Normal"]))
    content.append(Paragraph(f"<b>Hybrid Prediction:</b> {final_pred*100:.2f}%", styles["Normal"]))
    content.append(Spacer(1,10))
    content.append(Paragraph(f"<b>Final Result:</b> {final_result}", styles["Normal"]))
    content.append(Spacer(1,10))
    
    if selected_symptoms:
        content.append(Paragraph("<b>Observed Symptoms:</b>", styles["Normal"]))
        for sym in selected_symptoms:
            content.append(Paragraph(f"- {sym}", styles["Normal"]))
    else:
        content.append(Paragraph("<b>Observed Symptoms:</b> None", styles["Normal"]))
    
    content.append(Spacer(1,10))
    content.append(Paragraph(f"<b>Date & Time:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles["Normal"]))
    doc.build(content)
    buffer.seek(0)
    return buffer
# ---------------- PREDICTION ----------------
if st.button("🔍 Predict"):
    if uploaded is None or not any(symptoms):
        st.warning("⚠ Hybrid prediction requires BOTH an uploaded image and at least one selected symptom.")
    else:
        with st.spinner("Analyzing inputs..."):
            time.sleep(1.5)
            try:
                # Image prediction
                img_arr = preprocess_image(img, cnn_model.input_shape)
                img_pred = cnn_model.predict(img_arr)[0][0]
                
                # Symptom prediction
                sym_arr = np.array(symptoms, dtype=int).reshape(1,6)
                sym_pred = symptom_model.predict(sym_arr)[0][0]

                # Hybrid prediction
                final_pred = (img_pred + sym_pred)/2
                final_result = "⚠ Mastitis Detected" if final_pred>0.5 else "✅ Healthy Cow"

                # Display predictions
                st.markdown("### 🔎 Prediction Probabilities")
                st.write(f"Image-based: {img_pred*100:.2f}%")
                st.write(f"Symptoms-based: {sym_pred*100:.2f}%")
                st.write(f"Hybrid: {final_pred*100:.2f}%")
                
                # Info box
                if final_pred>0.5:
                    st.error(f"{final_result} (Hybrid Result)")
                    info_text = "Immediate veterinary consultation is advised."
                else:
                    st.success(f"{final_result} (Hybrid Result)")
                    info_text = "Continue regular monitoring of the cow’s health."

                st.markdown(f"""
                <div class="info-box">
                <b>Explanation:</b><br>{info_text}
                </div>
                """, unsafe_allow_html=True)

                # PDF download
                selected_symptoms = [symptoms_labels[i] for i,val in enumerate(symptoms) if val]
                pdf = generate_pdf_report(final_result, img_pred, sym_pred, final_pred, selected_symptoms)
                st.download_button(
                    label="📄 Download Report",
                    data=pdf,
                    file_name="hybrid_mastitis_report.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Prediction failed: {e}")


              