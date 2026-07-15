"""
Facial Emotion Recognition Module (Prototype)
================================================
Uses a CNN trained on FER-2013 (see notebooks/FER_Training.ipynb) plus
OpenCV's Haar cascade for face detection to classify emotion from an
uploaded photo.

TODO:
- Place your trained model at models/fer_model.keras
- Consider swapping the Haar cascade for a more robust face detector
  (e.g., MTCNN, MediaPipe) for better accuracy
"""

import cv2
import numpy as np
import streamlit as st
from PIL import Image

MODEL_PATH = "models/fer_model.keras"
EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
FACE_CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


@st.cache_resource
def load_model():
    import tensorflow as tf

    try:
        return tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        st.warning(f"Model not found at {MODEL_PATH}. Add your trained model to enable predictions. ({e})")
        return None


def render():
    st.title("Facial Emotion Recognition (Prototype)")

    uploaded_file = st.file_uploader("Upload a face photo (JPG/PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded photo", width=300)

        img_arr = np.array(image)
        gray = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
        detector = cv2.CascadeClassifier(FACE_CASCADE)
        faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            st.error("No face detected. Try a clearer, front-facing photo.")
            return

        model = load_model()
        if model is None:
            st.info("Prediction unavailable — model file not present in this repo.")
            return

        x, y, w, h = faces[0]
        face = cv2.resize(gray[y : y + h, x : x + w], (48, 48)) / 255.0
        face = face.reshape(1, 48, 48, 1)

        preds = model.predict(face)[0]
        top_idx = int(np.argmax(preds))

        st.subheader("Result")
        st.write(f"**Detected emotion:** {EMOTIONS[top_idx]}")
        st.write(f"**Confidence:** {preds[top_idx] * 100:.2f}%")
