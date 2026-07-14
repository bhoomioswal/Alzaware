# AlzAware: A Multimodal Human-Centered AI & ML Framework for Early Alzheimer Risk Prediction and Emotional Monitoring
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)



This project is a research prototype developed during the IEEE EMBS Student Internship Program. It demonstrates the integration of multiple AI and ML modules for preliminary cognitive health assessment.

> It is intended for **educational and research purposes only** and is **not** a clinically validated diagnostic system.

## Problem Statement

Early detection of Alzheimer's risk indicators typically relies on a single 
diagnostic modality (e.g., MRI alone), which can miss complementary behavioral 
and emotional signals. AlzAware explores whether combining MRI analysis with 
facial/speech emotion patterns and simple memory/cognitive exercises can 
surface a more holistic, early, non-clinical picture — as a research question, 
not a replacement for medical diagnosis.



## Introduction

Alzheimer's disease is often diagnosed only after significant cognitive decline has already occurred, largely because early detection today relies on a single diagnostic lens — most commonly MRI-based structural analysis — evaluated in isolation. AlzAware is a research prototype that explores a different approach: combining multiple, complementary signals into one unified framework to build a more holistic, early-stage, non-clinical picture of cognitive health.

The application integrates five core modules into a single Streamlit-based interface. MRI scans are analyzed using a convolutional neural network to produce a preliminary risk category. Facial and speech emotion recognition models assess emotional expression patterns from photos and audio clips, which can offer supplementary behavioral context. Interactive memory and cognitive assessment exercises add a simple, engagement-based measure alongside the AI-driven modules. All results are brought together in a unified dashboard, giving a session-level summary rather than a single, opaque score.

AlzAware was developed as part of the IEEE EMBS Student Internship Program, with an accompanying IEEE conference paper detailing the methodology and evaluation of each component. It is important to note that this is a prototype and proof-of-concept — the modules have been developed and tested independently, but the framework has not been clinically validated and is not intended for medical diagnosis. Its purpose is to demonstrate how multimodal AI/ML techniques could be combined for future, clinically-supervised research in this space.
## Features

- ✅ Prototype MRI-based Alzheimer's risk indicator
- ✅ Prototype facial emotion recognition
- ✅ Prototype speech emotion recognition
- ✅ Interactive memory assessment games
- ✅ Cognitive assessment module
- ✅ Unified interactive dashboard
- ✅ AI chatbot integration

## What This Project Is NOT

- ❌ A deployed clinical system
- ❌ A diagnostic tool
- ❌ Hospital-ready software
- ❌ A production application

This is a **proof-of-concept (POC)** built for academic and research purposes.

## Workflow

```
User Registration
       ↓
MRI Upload
       ↓
Facial & Speech Emotion Recognition
       ↓
Memory Assessment
       ↓
Cognitive Assessment
       ↓
Risk Analysis
       ↓
Dashboard
```
## Architecture

<img width="2720" height="2480" alt="AlzAware_system_architecture" src="https://github.com/user-attachments/assets/ef0e2590-1b26-4b72-a9c8-ef2639a35eb5" />



## Tech Stack

- Python
- TensorFlow / Keras
- OpenCV
- Scikit-learn
- Streamlit
- NumPy / Pandas
- Librosa (speech features)

## Datasets
- Alzeihmer's MRI Dataset
- FER-2013
- RAVDESS

## Repository Structure

```
AlzAware/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── assets/
│   ├── architecture.png
│   ├── workflow.png
│   └── screenshots/
│
├── models/
├── datasets/
│   └── dataset_links.md
│
├── modules/
│   ├── registration.py
│   ├── mri_prediction.py
│   ├── facial_emotion.py
│   ├── speech_emotion.py
│   ├── memory_assessment.py
│   ├── cognitive_assessment.py
│   ├── chatbot.py
│   └── dashboard.py
│
├── notebooks/
│   ├── MRI_Training.ipynb
│   ├── FER_Training.ipynb
│   └── Speech_Training.ipynb
│
├── reports/
│
└── docs/
    ├── methodology.md
    ├── installation.md
    └── future_scope.md
```
## Installation

```bash
git clone https://github.com/<your-username>/AlzAware.git
cd AlzAware
pip install -r requirements.txt
streamlit run alzaware.py
```

## Results

Individual AI/ML modules were developed and tested independently, then integrated into a unified prototype demonstrating multimodal cognitive health assessment. Add your model metrics (accuracy, precision, recall, F1, confusion matrices) here once finalized.

## Future Scope

- Improve MRI prediction accuracy using larger, more diverse datasets
- Deploy the application on a secure cloud platform
- Integrate longitudinal patient monitoring
- Develop a companion mobile application
- Validate the framework against clinical datasets
- Conduct usability testing with healthcare professionals

## Authors

- Bhoomi — Modern College of Engineering, Pune
- Co-authors: Utkarsha Raje, Anand Parekh
- Mentor: Kush Patel (IEEE EMBS Student Internship Program)

## Disclaimer

This repository contains a prototype developed for academic and research purposes. It is **not** intended for clinical diagnosis or medical decision-making.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
