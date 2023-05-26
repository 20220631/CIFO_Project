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

def plot_fitness(generations, best_fitness_values):
    plt.plot(generations, best_fitness_values)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Average Fitness Variation')
    plt.show()


def evolution_process(num_runs=5):
    average_fitness_values = []

    for _ in range(num_runs):
        best_fitness_values = []

        for generation in range(20, 100):
            pop = Population(size=50, optim="min", sol_size=len(data_), valid_set=range(20), replacement=True)
            pop.evolve(gens=generation, xo_prob=0.9, mut_prob=0.2, select=tournament_sel,
                       mutate=swap_mutation, crossover=uniform_co, elitism=True)  # Evolve the population for 1 generation

            # Get the best individual in the current generation
            best_individual = min(pop, key=attrgetter("fitness"))
            best_fitness = best_individual.fitness

            # Store the best fitness value
            best_fitness_values.append(best_fitness)

        average_fitness_values.append(best_fitness_values)

    # Calculate the average fitness values
    average_fitness_values = np.mean(average_fitness_values, axis=0)

    # Plot the fitness variation
    generations = np.arange(20, 100)
    plot_fitness(generations, average_fitness_values)


# Set up the population and other parameters
evolution_process(num_runs=5)
