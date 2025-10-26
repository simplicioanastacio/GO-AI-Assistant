from llama_cpp import Llama

# Load the model from your path
llm = Llama(
    model_path="E:\\PROJECTS\\models\\mistral-7b-instruct-v0.1.Q6_K.gguf",
    n_ctx=4096,
    n_threads=6,   # adjust based on your CPU
    n_batch=512,
    use_mlock=True  # optional: helps performance on some systems
)

# Run a test prompt
response = llm(
    "### Instruction:\nWhat's the capital of Guinea-Bissau?\n\n### Response:",
    max_tokens=128,
    temperature=0.7,
    top_p=0.9,
    stop=["###"]
)

print(response["choices"][0]["text"].strip())
