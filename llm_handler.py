import numpy as np
import openai
import requests
import streamlit as st

# Supported modes: 'synthetic', 'openai', 'huggingface'
MODE = 'huggingface'

# HuggingFace model and token
HF_MODEL = "tiiuae/falcon-rw-1b"
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

def get_reception_huggingface(prompt, model=HF_MODEL, hf_token=HF_TOKEN):
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            text = data[0]["generated_text"]
        elif isinstance(data, dict) and "generated_text" in data:
            text = data["generated_text"]
        else:
            text = str(data)
        R_t = min(1.0, len(text.strip()) / 1000)
        return float(R_t), text
    except Exception as e:
        return 0.5, f"[HF API error] {str(e)}"

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
        return 0.5, f"[OpenAI error] {str(e)}"

def get_reception(V_t, noise_scale=0.05):
    return np.random.normal(loc=V_t, scale=noise_scale)

def query_R_t(V_t=None, user_prompt=None, noise_scale=0.05):
    if MODE == 'synthetic':
        R_t = get_reception(V_t, noise_scale)
        return R_t, f"[Synthetic R(t): {round(R_t, 3)}]"
    elif MODE == 'openai' and user_prompt:
        return get_reception_openai(user_prompt)
    elif MODE == 'huggingface' and user_prompt:
        return get_reception_huggingface(user_prompt)
    else:
        return 0.5, "[Invalid MODE or Missing Prompt]"

