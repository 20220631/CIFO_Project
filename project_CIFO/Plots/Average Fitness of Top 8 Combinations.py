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

# List all the combinations of mutation, selection and crossover
mutation_methods = [swap_mutation, random_resetting]
selection_methods = [tournament_sel, rank_selection]
crossover_methods = [uniform_co, pmx]

# Record the results of each run in a list
results = []

# Run the genetic algorithm with each combination of mutation, selection, and crossover
for mutate in mutation_methods:
    for select in selection_methods:
        for crossover in crossover_methods:
            for _ in range(1):  # repeat the test N times
                # Initialize the population
                pop = Population(size=70, optim="min", sol_size=len(data_), valid_set=range(20), replacement=True)

                # Evolve the population
                pop.evolve(gens=70, xo_prob=0.9, mut_prob=0.2, select=select, mutate=mutate, crossover=crossover,
                           elitism=True)

                # Get the best individual
                if pop.optim == "max":
                    best_individual = max(pop.individuals, key=attrgetter("fitness"))
                elif pop.optim == "min":
                    best_individual = min(pop.individuals, key=attrgetter("fitness"))

                # Record the result of the run (assuming that the best fitness is what you want to record)
                results.append((mutate.__name__, select.__name__, crossover.__name__, best_individual.get_fitness()))

# At the end of this loop, `results` should be a list where each item is a tuple containing:
# (mutation method name, selection method name, crossover method name and the best fitness achieved)

# To compute the highest, lowest, and average fitness for each combination:
boxplot_results = {}

for result in results:
    combination = (result[0], result[1], result[2])  # mutation, selection, crossover
    fitness = result[3]

    if combination in boxplot_results:
        boxplot_results[combination].append(fitness)
    else:
        boxplot_results[combination] = [fitness]

# Order the combinations by average fitness
sorted_combinations = sorted(boxplot_results.items(), key=lambda x: np.mean(x[1]))

# Extract the ordered combination names and fitness values
ordered_names = ['\n'.join(map(str, combination)) for combination, _ in sorted_combinations]
ordered_data = [boxplot_results[combination] for combination, _ in sorted_combinations]

# Generate the box plot
fig, ax = plt.subplots(figsize=(10, 20))  # Increase figure size

# Plot the box plot with ordered data
ax.boxplot(ordered_data)

# Set x-axis tick labels
ax.set_xticklabels(ordered_names, fontsize='xx-small')

# Set y-axis label
ax.set_ylabel('Fitness')

# Set title
ax.set_title('Fitness Variation for top 8 combinations of mutation, selection, and crossover methods')

# Show the box plot
plt.show()
