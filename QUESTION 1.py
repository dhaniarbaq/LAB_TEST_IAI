import streamlit as st
import random
import numpy as np

POP_SIZE = 300
CHROM_LENGTH = 80
GENERATIONS = 50
TARGET_ONES = 40

def fitness(chrom):
    return abs(TARGET_ONES - sum(chrom))

def create_population():
    return [[random.randint(0,1) for _ in range(CHROM_LENGTH)] for _ in range(POP_SIZE)]

def crossover(p1, p2):
    point = random.randint(1, CHROM_LENGTH-1)
    return p1[:point] + p2[point:]

def mutate(chrom):
    idx = random.randint(0, CHROM_LENGTH-1)
    chrom[idx] = 1 - chrom[idx]
    return chrom

st.title("Genetic Algorithm Bit Pattern Generator")

population = create_population()

for gen in range(GENERATIONS):
    population = sorted(population, key=fitness)
    new_pop = population[:10]  # elitism
    while len(new_pop) < POP_SIZE:
        p1, p2 = random.sample(population[:100], 2)
        child = crossover(p1, p2)
        if random.random() < 0.1:
            child = mutate(child)
        new_pop.append(child)
    population = new_pop

best = population[0]
st.write("Best chromosome:", best)
st.write("Number of ones:", sum(best))
