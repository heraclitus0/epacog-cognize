import streamlit as st
from rcc_core import RCC
from reception_mutation import mutate_reception
from save_manager import SaveManager
from llm_handler import query_R_t, MODE, init_gpt4all
from viz import plot_rcc_trace

# Init model if needed
if MODE == "gpt4all":
    with st.spinner("Loading GPT4All model..."):
        init_gpt4all()

rcc = RCC()
memory = SaveManager()

st.title("🧠 RCC Cognitive Rupture Simulator")
st.markdown("Simulate how cognition mutates under recursive drift, rupture, and projection divergence.")
st.caption(f"🔌 Current Mode: `{MODE}`")

n_cycles = st.slider("Number of cycles", 5, 100, 25)
mutate_on_rupture = st.checkbox("Enable mutated reception post-rupture", value=True)
prompt = st.text_input("Prompt (used in LLM modes)", value="Explain recursion control calculus")

if st.button("🚀 Run Simulation"):
    rcc.__init__()
    memory.reset()
    
    for t in range(n_cycles):
        V_t = rcc.V
        R_t, raw = query_R_t(V_t=V_t, user_prompt=prompt)
        V_new, E, delta, theta, S_bar, rupture = rcc.update(R_t)

        if rupture and mutate_on_rupture:
            R_t = mutate_reception(R_t, S_bar, E)
            # Skip extra update — let next cycle take mutated R_t

        memory.add_point(V_new, R_t, delta, theta, E, S_bar, rupture)

        if st.session_state.get("show_raw", False):
            st.text(f"[{t}] {raw}")

    st.success("✅ Simulation complete.")

    st.subheader("📊 RCC Trace")
    plot_rcc_trace(memory.all_points())

    with st.expander("📋 Detailed Table"):
        st.dataframe(memory.all_points())

    st.subheader("🧠 Final State")
    last = memory.get_point(len(memory.timeline) - 1)
    st.json(last.as_dict() if last else {})
