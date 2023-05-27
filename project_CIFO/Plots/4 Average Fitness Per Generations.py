from project_CIFO.charles.charles import Population, Individual
from project_CIFO.data.data import data_, nutrients
from project_CIFO.charles.selection import tournament_sel
from project_CIFO.charles.mutation import swap_mutation
from project_CIFO.charles.crossover import uniform_co
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


def plot_fitness(generations, avg_fitness_values, min_fitness_values, max_fitness_values):
    # Plot average fitness values
    plt.plot(generations, avg_fitness_values, label='Average', color='green')
    # Plot max fitness values
    plt.plot(generations, max_fitness_values, label='Max', color='grey')
    # Plot min fitness values
    plt.plot(generations, min_fitness_values, label='Min', color='grey')

    # Fill the area between max and min with grey color
    plt.fill_between(generations, min_fitness_values, max_fitness_values, color='grey', alpha=0.5)

    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Average Fitness Variation')
    plt.legend()
    plt.show()


def evolution_process(num_runs=5):
    avg_fitness_values = []
    min_fitness_values = []
    max_fitness_values = []

    for generation in range(40, 121):
        best_fitness_values = []
        print(f"generation:{generation}")
        for _ in range(num_runs):  # repeat each generation value 5 times
            pop = Population(size=91, optim="min", sol_size=len(data_), valid_set=np.arange(0, 1.01, 0.01), replacement=True)

            # Evolve population for each different value of generation
            pop.evolve(gens=generation, xo_prob=0.9, mut_prob=0.2, select=tournament_sel,
                       mutate=swap_mutation, crossover=uniform_co, elitism=True)

            # Get the best individual in the current generation
            best_individual = min(pop, key=attrgetter("fitness"))
            best_fitness = best_individual.fitness

            # Store the best fitness value
            best_fitness_values.append(best_fitness)

        # Calculate average, min and max fitness values
        avg_fitness_values.append(np.mean(best_fitness_values))
        min_fitness_values.append(np.min(best_fitness_values))
        max_fitness_values.append(np.max(best_fitness_values))

    # Plot the fitness variation
    generations = range(40, 121)
    plot_fitness(generations, avg_fitness_values, min_fitness_values, max_fitness_values)


# Run evolution_process function to extract results
evolution_process(num_runs=5)

