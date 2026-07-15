# Models

Trained model weights are **not** tracked in this repository (see `.gitignore`) because they are large binary files unsuited to standard git.

Expected files at runtime:

| File | Produced by | Used by |
|---|---|---|
| `mri_model.pkl` | `notebooks/MRI_Training.ipynb` | `modules/mri_prediction.py` |
| `fer_model.pkl` | `notebooks/FER_Training.ipynb` | `modules/facial_emotion.py` |
| `ravdess_model.pkl` | `notebooks/RAVDESS_Training.ipynb` | `modules/speech_emotion.py` |

