from langchain_community.llms import LlamaCpp

def load_llm():
    return LlamaCpp(
        model_path="models/Phi-3-mini-4k-instruct-Q4_K_M.gguf",
        n_ctx=4096,
        n_threads=8,
        n_gpu_layers=-1,
        temperature=0.6,
        top_p=0.9,
        max_tokens=512,
        stop=["<|user|>", "<|assistant|>"], # Chặn sớm cho nó đỡ lan man
        verbose=False # turn off llama_perf_context_print
    )