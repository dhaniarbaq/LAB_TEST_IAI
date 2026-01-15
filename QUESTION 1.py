# -*- coding: utf-8 -*-
import numpy as np
import streamlit as st
import pandas as pd

# ---------------- Parameters ----------------
POP_SIZE = 300
GENE_LENGTH = 80
MAX_GEN = 50
PC = 0.9
PM = 0.01
ELITE = 2
TOUR_K = 3
SEED = 42

rng = np.random.default_rng(SEED)

# Fitness (OneMax)
def fitness(pop):
    return np.sum(pop, axis=1)

def init_population():
    return rng.integers(0, 2, size=(POP_SIZE, GENE_LENGTH))

def tournament_selection(pop, fit):
    candidates = rng.choice(len(pop), TOUR_K, replace=False)
    return pop[candidates[np.argmax(fit[candidates])]]

# Two-point crossover
def crossover(p1, p2):
    if rng.random() < PC:
        p1_idx, p2_idx = sorted(rng.integers(1, GENE_LENGTH, 2))
        c1 = np.concatenate([p1[:p1_idx], p2[p1_idx:p2_idx], p1[p2_idx:]])
        c2 = np.concatenate([p2[:p1_idx], p1[p1_idx:p2_idx], p2[p2_idx:]])
        return c1, c2
    return p1.copy(), p2.copy()

def mutation(child):
    flip = rng.random(GENE_LENGTH) < PM
    child[flip] ^= 1
    return child

def run_ga():
    population = init_population()
    history = []

    progress = st.progress(0)

    for gen in range(MAX_GEN):
        fit = fitness(population)

        history.append({
            "Generation": gen + 1,
            "Best Fitness": fit.max(),
            "Average Fitness": fit.mean()
        })

        # Elitism
        elite_idx = np.argsort(fit)[-ELITE:]
        elites = population[elite_idx]

        new_population = []

        while len(new_population) < POP_SIZE - ELITE:
            parent1 = tournament_selection(population, fit)
            parent2 = tournament_selection(population, fit)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutation(child1))
            if len(new_population) < POP_SIZE - ELITE:
                new_population.append(mutation(child2))

        population = np.vstack([new_population, elites])
        progress.progress((gen + 1) / MAX_GEN)

    final_fit = fitness(population)
    best_index = np.argmax(final_fit)

    return pd.DataFrame(history), population[best_index], final_fit[best_index]

# ---------------- Streamlit UI (Redesigned Layout) ----------------
st.set_page_config(page_title="Genetic Algorithm – OneMax", layout="wide")

# Header
st.markdown(
    "<h1 style='text-align: center;'>🧬 Genetic Algorithm Dashboard – OneMax Problem</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# Sidebar for configuration info (visual only, parameters unchanged)
with st.sidebar:
    st.header("⚙️ GA Configuration")
    st.write(f"Population Size: **{POP_SIZE}**")
    st.write(f"Gene Length: **{GENE_LENGTH}**")
    st.write(f"Max Generations: **{MAX_GEN}**")
    st.write(f"Crossover Rate (PC): **{PC}**")
    st.write(f"Mutation Rate (PM): **{PM}**")
    st.write(f"Elites: **{ELITE}**")
    st.write(f"Tournament Size: **{TOUR_K}**")
    st.write(f"Random Seed: **{SEED}**")
    st.markdown("---")
    st.info("This sidebar shows the fixed GA parameters.\nFunctionality remains unchanged.")

# Control Panel
st.subheader("🎮 Control Panel")
run = st.button("🚀 Run Genetic Algorithm")

if run:
    history, best_solution, best_fitness = run_ga()

    st.success("Genetic Algorithm execution completed!")

    # Layout in two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Fitness Convergence")
        st.line_chart(history.set_index("Generation"))

    with col2:
        st.subheader("🏆 Best Solution Found")
        st.metric(
            label="Best Fitness",
            value=f"{best_fitness}",
            delta=f"{best_fitness - history['Average Fitness'].iloc[0]:.2f}"
        )
        st.write(f"**Maximum Possible Fitness:** {GENE_LENGTH}")
        st.progress(best_fitness / GENE_LENGTH)

        st.markdown("**Best Chromosome (Binary Representation):**")
        st.code("".join(best_solution.astype(str)), language="text")

    # Optional expandable section
    with st.expander("📊 Show Fitness History Table"):
        st.dataframe(history, use_container_width=True)
