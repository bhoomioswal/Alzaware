"""
MRI-Based Alzheimer Risk Prediction Module (Prototype)
========================================================
Loads a trained CNN model (e.g., trained in notebooks/MRI_Training.ipynb)
and produces a preliminary, non-clinical risk indicator from an uploaded
brain MRI slice.

TODO:
- Place your trained model at models/mri_model.keras
- Replace the placeholder preprocessing with the exact pipeline used
  during training (resize, normalization, channel handling)
- Replace CLASS_NAMES with your actual label set from training
"""

import numpy as np
import streamlit as st
from PIL import Image

MODEL_PATH = "models/mri_model.keras"
IMG_SIZE = (176, 176)  # match training input size
CLASS_NAMES = ["Non-Demented", "Very Mild Demented", "Mild Demented", "Moderate Demented"]


@st.cache_resource
def load_model():
    import tensorflow as tf

    try:
        return tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        st.warning(f"Model not found at {MODEL_PATH}. Add your trained model to enable predictions. ({e})")
        return None


def preprocess(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB").resize(IMG_SIZE)
    arr = np.array(image) / 255.0
    return np.expand_dims(arr, axis=0)


def render():
    st.title("MRI-Based Risk Prediction (Prototype)")
    st.caption("Non-clinical, illustrative only.")

    uploaded_file = st.file_uploader("Upload an MRI slice (JPG/PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded MRI", width=300)

        model = load_model()
        if model is None:
            st.info("Prediction unavailable — model file not present in this repo.")
            return

        x = preprocess(image)
        preds = model.predict(x)[0]
        top_idx = int(np.argmax(preds))

        st.subheader("Result")
        st.write(f"**Predicted category:** {CLASS_NAMES[top_idx]}")
        st.write(f"**Confidence:** {preds[top_idx] * 100:.2f}%")

        st.bar_chart({name: float(p) for name, p in zip(CLASS_NAMES, preds)})
