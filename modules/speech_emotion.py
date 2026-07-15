"""
Speech Emotion Recognition Module (Prototype)
================================================
Extracts MFCC features from an uploaded audio clip with librosa and
classifies emotion using a model trained on RAVDESS
(see notebooks/Speech_Training.ipynb).

TODO:
- Place your trained model at models/speech_model.pkl
- Confirm the exact MFCC feature extraction (n_mfcc, aggregation)
  matches what was used at training time
"""

import numpy as np
import streamlit as st
import librosa
import joblib

MODEL_PATH = "models/speech_model.pkl"
EMOTIONS = ["Neutral", "Calm", "Happy", "Sad", "Angry", "Fearful", "Disgust", "Surprised"]


@st.cache_resource
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        st.warning(f"Model not found at {MODEL_PATH}. Add your trained model to enable predictions. ({e})")
        return None


def extract_features(file_path: str, n_mfcc: int = 40) -> np.ndarray:
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return np.mean(mfcc.T, axis=0)


def render():
    st.title("Speech Emotion Recognition (Prototype)")

    uploaded_file = st.file_uploader("Upload an audio clip (WAV)", type=["wav"])

    if uploaded_file is not None:
        st.audio(uploaded_file)

        tmp_path = "temp_audio.wav"
        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        model = load_model()
        if model is None:
            st.info("Prediction unavailable — model file not present in this repo.")
            return

        features = extract_features(tmp_path).reshape(1, -1)
        pred = model.predict(features)[0]

        st.subheader("Result")
        st.write(f"**Detected emotion:** {pred}")
