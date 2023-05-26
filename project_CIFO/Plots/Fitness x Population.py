from project_CIFO.charles.charles import Population, Individual
from project_CIFO.data.data import data_, nutrients
from project_CIFO.charles.selection import fps, tournament_sel, rank_selection
from project_CIFO.charles.mutation import swap_mutation, creep_mutation, uniform_mutation, random_resetting
from project_CIFO.charles.crossover import single_point_co, multi_point_co, uniform_co, pmx
from operator import attrgetter
import matplotlib.pyplot as plt
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


def plot_fitness(populations, best_fitness_values):
    population_nums = np.arange(len(best_fitness_values))
    fitness_values = np.array(best_fitness_values)

    # Reshape the fitness values to match the population_nums shape
    fitness_values = fitness_values.reshape(population_nums.shape)

    plt.plot(population_nums, fitness_values)
    plt.xlabel('Population')
    plt.ylabel('Fitness')
    plt.title('Fitness Variation')
    plt.show()


def evolution_process2(initial_population, num_populations):
    populations = []
    best_fitness_values = []

    current_population = initial_population
    for population in range(num_populations):
        current_population.evolve(gens=population, xo_prob=0.9, mut_prob=0.2, select=tournament_sel, mutate=swap_mutation, crossover=uniform_co, elitism=True)

        # Get the best individual in the current population
        best_individual = min(current_population, key=attrgetter("fitness"))
        best_fitness = best_individual.fitness

        # Store the current population and best fitness value
        populations.append(current_population)
        best_fitness_values.append(best_fitness)

        # Generate the next population
        current_population = Population(size=50, optim="min", sol_size=len(data_), valid_set=range(10), replacement=True)

    # Plot the fitness variation
    plot_fitness2(populations, best_fitness_values)


# Set up the initial population and other parameters
initial_population = Population(size=50, optim="min", sol_size=len(data_), valid_set=range(10), replacement=True)
num_populations = 100

evolution_process2(initial_population, num_populations)