# llama/llama_runner.py
import os
from llama_cpp import Llama
from llama.config import MODEL_PATH

_llm = None

def get_model(n_threads=6, n_ctx=2048):
    global _llm
    if _llm is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        _llm = Llama(model_path=MODEL_PATH, n_ctx=n_ctx, n_threads=n_threads, verbose=False)
    return _llm

def ask_go(prompt: str, max_tokens: int = 400) -> str:
    """
    Standard instruction wrapper for the local model.
    """
    model = get_model()
    instruction = f"### Instruction:\n{prompt.strip()}\n\n### Response:"
    out = model(instruction, max_tokens=max_tokens)
    return out["choices"][0]["text"].strip()
