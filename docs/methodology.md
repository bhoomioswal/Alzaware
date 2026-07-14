# Methodology

## 1. Overview

AlzAware is a prototype multimodal AI & ML framework designed to support early cognitive health assessment by integrating multiple sources of information rather than relying on a single indicator. The system combines MRI brain image analysis, facial emotion recognition, speech emotion recognition, memory assessment, and cognitive assessment to provide a comprehensive overview of the user's cognitive wellness.

Each modality is processed independently using a dedicated Machine Learning or Deep Learning model. The outputs of these modules are presented together through an interactive Streamlit dashboard. The current implementation demonstrates the integration of these modules as a proof-of-concept and is intended for educational and research purposes.

---

## 2. Data

### MRI Alzheimer's Prediction

**Dataset**

- Alzheimer's MRI Dataset

**Preprocessing**

- Resize images to 224 × 224 pixels
- Normalize pixel values to the range [0,1]
- Data augmentation:
  - Rotation
  - Horizontal Flip
  - Zoom
- Training / Testing split provided by the dataset

---

### Facial Emotion Recognition

**Dataset**

- FER-2013

**Preprocessing**

- Face detection using OpenCV Haar Cascade
- Grayscale conversion
- Resize to 48 × 48 pixels
- Pixel normalization

---

### Speech Emotion Recognition

**Dataset**

- RAVDESS

**Preprocessing**

- Noise reduction
- Audio normalization
- Feature extraction:
  - MFCC
  - Mel Spectrogram
  - Chroma Features

---

### Memory Assessment

No external dataset is used.

The module evaluates user performance through three interactive games:

- Word Recall
- Card Matching
- Object Recall

The following metrics are recorded:

- Recall accuracy
- Number of correct responses
- Completion time

---

### Cognitive Assessment

No external dataset is used.

The module measures cognitive performance using a Reaction Time Test.

Recorded metrics include:

- Reaction time
- Accuracy
- Response consistency

---

## 3. Models

| Module | Architecture | Input | Output |
|---------|-------------|-------|--------|
| MRI Prediction | CNN with Transfer Learning (EfficientNetB0  | MRI Brain Image | Dementia Category |
| Facial Emotion Recognition | CNN | Facial Image | Emotion Class |
| Speech Emotion Recognition | CNN / ANN using MFCC Features | Audio Recording | Emotion Class |
| Memory Assessment | Rule-based Scoring | User Responses | Memory Score (0–100) |
| Cognitive Assessment | Rule-based Scoring | Reaction Time | Cognitive Score (0–100) |

---

## 4. Workflow

The prototype follows the workflow below:

1. User Registration
2. MRI Image Upload
3. MRI Prediction
4. Facial Emotion Recognition
5. Speech Emotion Recognition
6. Memory Assessment
7. Cognitive Assessment
8. Display Results on Interactive Dashboard

Each module generates an independent output which is presented together to provide an overall view of the user's cognitive wellness.

---

## 5. Evaluation

The AI and ML models are evaluated individually using standard classification metrics.

Metrics include:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

Performance values will be updated after final model training and evaluation.

---

## 6. Current Prototype Status

The current version of AlzAware is a functional prototype that demonstrates:

- MRI-based Alzheimer's prediction
- Facial emotion recognition
- Speech emotion recognition
- Memory assessment
- Cognitive assessment
- Interactive Streamlit dashboard
- AI chatbot integration

The project focuses on demonstrating multimodal integration rather than providing a clinically validated diagnosis.

---

## 7. Limitations

- The framework is a prototype developed for research and educational purposes.
- MRI predictions depend on publicly available datasets.
- Memory and cognitive assessments are screening tools and are not standardized clinical tests.
- Facial and speech emotion recognition are used as supportive indicators rather than diagnostic measures.
- No clinically validated multimodal risk fusion model has been implemented.
- The system is not intended to replace professional medical diagnosis.

---

## 8. Future Work

Future improvements include:

- Training on larger and more diverse datasets.
- Improving MRI classification accuracy.
- Clinical validation with healthcare professionals.
- Secure cloud-based user data storage.
- Longitudinal cognitive health tracking.
- Mobile application deployment.
- Advanced multimodal feature fusion using transformer-based architectures.
