import tiktoken


def get_tokens_text(text: str, model_name: str = "gpt2") -> int:
    encoding = tiktoken.get_encoding(model_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens
