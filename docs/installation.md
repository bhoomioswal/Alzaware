# Installation Guide

## Prerequisites

- Python 3.10+
- pip
- (Optional) a virtual environment tool such as `venv` or `conda`

## Steps

```bash
git clone https://github.com/<your-username>/AlzAware.git
cd AlzAware

python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Add Model Files

This repo does not include trained model weights. Add them locally at:
models/mri_model.keras
models/fer_model.keras
models/speech_model.pkl

See `models/README.md` for options on sharing large model files.

## Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` by default.
