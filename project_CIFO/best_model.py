from charles.charles import Population, Individual
from data.data import data_, nutrients
from charles.selection import tournament_sel
from charles.mutation import swap_mutation
from charles.crossover import uniform_co
from operator import attrgetter
import numpy as np


def get_fitness(self):
    """A function to calculate the total cost of the diet, penalizing it if the nutrient minimums are not met.
    Returns:
        float: Total cost of the diet
    """
    fitness = 0
    nutrient_totals = [0] * len(nutrients)

    for bit in range(len(self.representation)):
        if self.representation[bit] != 0:
            fitness += self.representation[bit]*data_[bit][2]  # cost of the selected item
            for nutrient_index in range(len(nutrients)):
                nutrient_totals[nutrient_index] += self.representation[bit]*data_[bit][3 + nutrient_index]

    # Apply a penalty if nutrient minimums are not met
    penalty = 0
    for nutrient_index in range(len(nutrients)):
        if nutrient_totals[nutrient_index] < nutrients[nutrient_index][1]:
            penalty += 1000000

    return fitness + penalty


# Monkey Patching
Individual.get_fitness = get_fitness


def get_best_individual(pop):
    return min(pop, key=attrgetter("fitness"))


def evolution_process(num_runs=500):
    best_individual = None
    best_fitness = float('inf')

    for _ in range(num_runs):

        pop = Population(size=91, optim="min", sol_size=len(data_), valid_set=np.arange(0, 1.01, 0.01), replacement=True)
        pop.evolve(gens=113, xo_prob=0.9, mut_prob=0.2, select=tournament_sel,
                   mutate=swap_mutation, crossover=uniform_co, elitism=True)

        # Get the best individual in the current generation
        current_best_individual = get_best_individual(pop)

        if current_best_individual.fitness < best_fitness:
            best_individual = current_best_individual
            best_fitness = current_best_individual.fitness

    return best_individual, best_fitness


# Set up the population and other parameters
best_individual, best_fitness = evolution_process()

print(f"Best fitness across all runs: {best_fitness}")

# Count the number of products used in the best individual
num_products_used = sum(1 for bit in best_individual.representation if bit != 0)
print(f"Number of products used in the best fitness: {num_products_used}")


for i, quantity in enumerate(best_individual.representation):
    print(f"Product: {data_[i][0]}, Unit: {data_[i][1]}, 1939 price (cents): {data_[i][2]}, Quantity: {quantity}")


