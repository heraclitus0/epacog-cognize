import numpy as np
import openai

# GPT4All support
from gpt4all import GPT4All

# Supported modes: 'synthetic', 'openai', 'gpt4all'
MODE = 'gpt4all'

# Local GPT4All model path or name (auto-download)
GPT4ALL_MODEL_NAME = "orca-mini-3b-gguf2-q4_0.gguf"
GPT4ALL_MODEL = None


def init_gpt4all(model_path=GPT4ALL_MODEL_NAME):
    global GPT4ALL_MODEL
    if GPT4ALL_MODEL is None:
        GPT4ALL_MODEL = GPT4All(model_path)


def get_reception_gpt4all(prompt):
    """
    Get R(t) using GPT4All local model
    """
    with GPT4ALL_MODEL.chat_session():
        response = GPT4ALL_MODEL.generate(prompt, max_tokens=150)
    R_t = min(1.0, len(response.strip()) / 1000)  # crude projection
    return R_t, response


def get_reception_openai(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        answer = response['choices'][0]['message']['content']
        R_t = min(1.0, len(answer.strip()) / 1000)
        return R_t, answer
    except Exception as e:
        print("OpenAI API Error:", e)
        return 0.5, "[Error generating response]"


def get_reception(V_t, noise_scale=0.05):
    """
    Simulated R(t) around V(t)
    """
    return np.random.normal(loc=V_t, scale=noise_scale)


def query_R_t(V_t=None, user_prompt=None, noise_scale=0.05):
    """
    Unified interface for R(t)
    """
    if MODE == 'synthetic':
        R_t = get_reception(V_t, noise_scale)
        return R_t, f"[Synthetic R(t): {round(R_t, 3)}]"

    elif MODE == 'openai' and user_prompt:
        return get_reception_openai(user_prompt)

    elif MODE == 'gpt4all' and user_prompt:
        return get_reception_gpt4all(user_prompt)

    else:
        return 0.5, "[Invalid MODE or Missing Prompt]"
