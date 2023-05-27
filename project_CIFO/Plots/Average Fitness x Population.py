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


def plot_fitness(population_nums, avg_fitness_values, min_fitness_values, max_fitness_values):
    # Plot average fitness values
    plt.plot(population_nums, avg_fitness_values, label='Average', color='green')
    # Plot max fitness values
    plt.plot(population_nums, max_fitness_values, label='Max', color='grey')
    # Plot min fitness values
    plt.plot(population_nums, min_fitness_values, label='Min', color='grey')

    # Fill the area between max and min with grey color
    plt.fill_between(population_nums, min_fitness_values, max_fitness_values, color='grey', alpha=0.5)

    plt.xlabel('Population Size')
    plt.ylabel('Fitness')
    plt.title('Fitness Variation')
    plt.legend()
    plt.show()


def evolution_process(num_populations, num_runs):
    avg_fitness_values = []
    min_fitness_values = []
    max_fitness_values = []

    for size in range(30,num_populations+1):
        fitness_values = []

        for _ in range(num_runs):
            # Generate the next population
            current_population = Population(size=size, optim="min", sol_size=len(data_), valid_set=np.arange(0,1.1,0.01),
                                            replacement=True)

            current_population.evolve(gens=120, xo_prob=0.9, mut_prob=0.2, select=tournament_sel, mutate=swap_mutation, crossover=uniform_co, elitism=True)

            # Get the best individual in the current population
            best_individual = min(current_population, key=attrgetter("fitness"))
            best_fitness = best_individual.fitness

            fitness_values.append(best_fitness)

        # Calculate average, min and max fitness values
        avg_fitness_values.append(np.mean(fitness_values))
        min_fitness_values.append(np.min(fitness_values))
        max_fitness_values.append(np.max(fitness_values))

    population_nums = np.arange(30, num_populations + 1)

    # Plot the fitness variation
    plot_fitness(population_nums, avg_fitness_values, min_fitness_values, max_fitness_values)

# Set up the initial population and other parameters
num_populations = 100
num_runs = 5

evolution_process(num_populations, num_runs)

