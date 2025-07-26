# RCC Cognitive Rupture Simulator

**Author:** Pulikanti Sashi Bharadwaj  
**Project:** Epacog Cognitive Systems  
**Grade:** Apple-Grade Cognitive Tooling  
**License:** MIT

---

## 🧠 What is This?

This simulator brings the theory of **Recursion Control Calculus (RCC)** into an operational framework. It simulates how cognition—human or artificial—undergoes drift, rupture, and recursive mutation.

Rather than correcting hallucinations, this system simulates what happens *after* rupture: **how perception mutates**.

---

## 🔧 Features

- ✅ Epistemic state simulation: V(t), R(t), ∆(t), E(t), Θ(t), S̄(t)
- ✅ RCC logic: Axioms 1–6 and non-associative continuity monad
- ✅ Projected divergence for rupture forecasting
- ✅ Mutated reception simulation (post-rupture perception distortion)
- ✅ GPT4All / OpenAI / synthetic R(t) modes
- ✅ Graphs + full savepoint timelines
- ✅ Streamlit interface for public or local deployment

---

## 🚀 How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

### Optional: For GPT4All

```bash
pip install gpt4all
# First run will download the model
```

---

## 🔐 API Keys (Optional)

If using OpenAI mode, create a `.streamlit/secrets.toml` file:

```toml
OPENAI_API_KEY = "sk-..."
```

---

## 🧬 Architecture

```
rcc_simulator/
├── app.py
├── rcc_core.py
├── reception_mutation.py
├── save_manager.py
├── llm_handler.py
├── viz.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml (optional)
```

---

## 🌐 Credits

This tool is powered by **Epacog** — a deployment layer for recursive cognitive systems based on RCC and Continuity Theory. Built by **Pulikanti Sashi Bharadwaj**, 2025.

