# llama/config.py
import os

MODEL_PATH = r"E:\PROJECTS\models\mistral-7b-instruct-v0.1.Q6_K.gguf"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
