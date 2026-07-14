# Models

Trained model weights are **not** tracked in this repository (see `.gitignore`) because they are large binary files unsuited to standard git.

Expected files at runtime:

| File | Produced by | Used by |
|---|---|---|
| `mri_model.keras` | `notebooks/MRI_Training.ipynb` | `modules/mri_prediction.py` |
| `fer_model.keras` | `notebooks/FER_Training.ipynb` | `modules/facial_emotion.py` |
| `speech_model.pkl` | `notebooks/Speech_Training.ipynb` | `modules/speech_emotion.py` |

