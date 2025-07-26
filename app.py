import streamlit as st
from rcc_core import RCC
from reception_mutation import mutate_reception
from save_manager import SaveManager
from llm_handler import query_R_t, MODE
from viz import plot_rcc_trace

# Initialize core
rcc = RCC()
memory = SaveManager()

# UI Header
st.title("🧠 Cognize")
st.caption("Epacog’s Recursive Cognition Simulator")
st.markdown("Simulating epistemic drift, rupture, and reception mutation under RCC control.")
st.code(f"MODE: {MODE.upper()}", language="yaml")

# Controls
n_cycles = st.slider("Cycles", 5, 100, 25, help="Number of recursive cognitive iterations.")
mutate_on_rupture = st.checkbox("Enable reception mutation after rupture", value=True)
prompt = st.text_input("Prompt", value="Explain recursion control calculus")

# Run Loop
if st.button("🚀 Run Cognition"):
    rcc.__init__()
    memory.reset()

    for t in range(n_cycles):
        V_t = rcc.V
        R_t, raw = query_R_t(V_t=V_t, user_prompt=prompt)
        V_new, E, delta, theta, S_bar, rupture = rcc.update(R_t)

        if rupture and mutate_on_rupture:
            R_t = mutate_reception(R_t, S_bar, E)

        memory.add_point(V_new, R_t, delta, theta, E, S_bar, rupture)

    st.success("✅ Cognition complete.")

    # Outputs
    st.subheader("📊 RCC Drift Trace")
    plot_rcc_trace(memory.all_points())

    with st.expander("🧾 Internal State Log"):
        st.dataframe(memory.all_points())

    st.subheader("🔍 Final State Snapshot")
    last = memory.get_point(len(memory.timeline) - 1)
    st.json(last.as_dict() if last else {})

