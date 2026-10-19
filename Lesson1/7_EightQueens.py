import random

import numpy as np


def init_population(population_size=8, queen_size=8):
    """Initialize population with random individuals"""
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, 7) for _ in range(queen_size)]
        population.append(individual)
    return population


def fitness(individual):
    """Calculate the fitness of an individual.
    The fitness is defined as the number of non-conflicting
    pairs of queens. The maximum fitness for 8 queens is 28,
    which occurs when no queens threaten each other."""

    non_conflicts = 0
    for i in range(len(individual)):
        for j in range(i + 1, len(individual)):
            if individual[i] != individual[j] and abs(i - j) != abs(
                individual[i] - individual[j]
            ):
                non_conflicts += 1
    return non_conflicts


def fitness_all(population):
    """Calculate the fitness for all individuals in
    the population and append it to each individual."""

    for i in range(len(population)):
        population[i].append(fitness(population[i]))


def fitness_probability(population):
    """Calculate the selection probability for
    each individual in the population."""

    total = sum([x[-1] for x in population])
    for i in range(len(population)):
        population[i].append(population[i][-1] / total)


def select_next_generation(population, population_size):
    """Select the next generation of individuals based on
    their selection probability."""

    select_prob = [x[-1] for x in population]
    selected_index = np.random.choice(
        range(len(population)), population_size, replace=False, p=select_prob
    )
    next_generation = [population[i][:-2] for i in selected_index]
    return next_generation


def crossover(individual1, individual2):
    """Perform crossover between two individuals."""

    crossover_point = random.randint(1, len(individual1) - 1)
    return (
        individual1[:crossover_point] + individual2[crossover_point:],
        individual2[:crossover_point] + individual1[crossover_point:],
    )


def crossover_all(population):
    """Perform crossover on all individuals in the population."""

    crossovered_population = []
    for i in range(0, len(population), 2):
        corssed1, crossed2 = crossover(population[i], population[i + 1])
        crossovered_population.extend([corssed1, crossed2])
    return crossovered_population


def mutation(individual, mutation_rate=0.1):
    """Perform mutation on an individual."""

    if random.random() < mutation_rate:
        mutate_point = random.randint(0, len(individual) - 1)
        individual[mutate_point] = random.randint(0, len(individual) - 1)
    return individual


def mutation_all(population, mutation_rate=0.1):
    """Perform mutation on all individuals in the population."""

    mutated_population = [mutation(x, mutation_rate) for x in population]
    return mutated_population


def output_board(individual):
    """Output the board representation of an individual."""

    for i in range(len(individual)):
        print(
            " ".join(
                ["Q" if x == individual[i] else "*" for x in range(len(individual))]
            )
        )


if __name__ == "__main__":
    population_size = 10
    queen_size = 8
    population = init_population(population_size, queen_size)

    num_generations = 1
    target = 28
    target_lists = []
    while True:
        # calculate fitness
        fitness_all(population)
        target_lists = [x for x in population if x[-1] == target]
        if len(target_lists) > 0:
            break
        # calculate probability
        fitness_probability(population)
        # select next generation
        pop_size = population_size // 2 if population_size // 2 % 2 == 0 else (population_size // 2) + 1 
        next_generation = select_next_generation(population, pop_size)
        # crossover
        crossovered_population = crossover_all(next_generation)
        random.shuffle(next_generation)
        crossovered_population.extend(crossover_all(next_generation))
        # mutation
        population = mutation_all(crossovered_population)
        num_generations += 1

    for target in target_lists:
        # print(target)
        output_board(target[:-1])
        print("\n\n")
