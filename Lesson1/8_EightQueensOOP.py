import random

import numpy as np


class EightQueens:
    def __init__(self, population_size=1000, queen_size=8):
        self.population_size = population_size
        self.queen_size = queen_size
        self.target = 28  # Maximum fitness for 8 queens
        self.target_lists = []
        self.population = []

    def __init_population(self):
        """Initialize population with random individuals"""

        for _ in range(self.population_size):
            individual = [random.randint(0, 7) for _ in range(self.queen_size)]
            self.population.append(individual)

    def __fitness(self, individual):
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

    def __fitness_all(self):
        """Calculate the fitness for all individuals in
        the population and append it to each individual."""

        for i in range(len(self.population)):
            self.population[i].append(self.__fitness(self.population[i]))

    def __fitness_probability(self):
        """Calculate the selection probability for
        each individual in the population."""

        total = sum([x[-1] for x in self.population])
        for i in range(len(self.population)):
            self.population[i].append(self.population[i][-1] / total)

    def __select_next_generation(self):
        """Select the next generation of individuals based on
        their selection probability."""

        select_prob = [x[-1] for x in self.population]
        selected_index = np.random.choice(
            range(len(self.population)),
            self.population_size,
            replace=False,
            p=select_prob,
        )
        next_generation = [self.population[i][:-2] for i in selected_index]
        return next_generation

    def __crossover(self, individual1, individual2):
        """Perform crossover between two individuals."""
        crossover_point = random.randint(1, self.queen_size - 1)
        child1 = individual1[:crossover_point] + individual2[crossover_point:]
        child2 = individual2[:crossover_point] + individual1[crossover_point:]
        return child1, child2

    def __crossover_all(self):
        """Perform crossover for the entire population."""
        next_generation = []
        for i in range(0, self.population_size, 2):
            child1, child2 = self.__crossover(
                self.population[i], self.population[i + 1]
            )
            next_generation.append(child1)
            next_generation.append(child2)
        return next_generation

    def __mutate(self, individual, mutation_rate=0.1):
        """Mutate an individual with a given mutation rate."""
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual[i] = random.randint(0, 7)
        return individual

    def __mutate_all(self, mutation_rate=0.1):
        """Mutate all individuals in the population."""
        for i in range(len(self.population)):
            self.population[i] = self.__mutate(self.population[i], mutation_rate)

    def output_board(self, individual):
        """Output the chessboard representation of an individual."""
        board = [["." for _ in range(8)] for _ in range(8)]
        for row, col in enumerate(individual):
            board[row][col] = "Q"
        for row in board:
            print(" ".join(row))
        print("\n")

    def run(self, mutation_rate=0.1):
        """Run the genetic algorithm for a given number of generations."""
        self.__init_population()
        while True:
            self.__fitness_all()
            self.__fitness_probability()
            self.population = self.__select_next_generation()
            self.population = self.__crossover_all()
            self.__mutate_all(mutation_rate)

            # Check if a solution is found
            for individual in self.population:
                if self.__fitness(individual) == self.target:
                    print(f"Solution found: {individual}")
                    self.output_board(individual)
                    return


if __name__ == "__main__":
    eight_queens = EightQueens(population_size=1000, queen_size=8)
    eight_queens.run(mutation_rate=0.1)
