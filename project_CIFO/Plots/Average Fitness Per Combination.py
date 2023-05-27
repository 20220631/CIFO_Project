from project_CIFO.charles.charles import Population, Individual
from project_CIFO.data.data import data_, nutrients
from project_CIFO.charles.selection import fps, tournament_sel, rank_selection
from project_CIFO.charles.mutation import swap_mutation, creep_mutation, uniform_mutation, random_resetting
from project_CIFO.charles.crossover import single_point_co, multi_point_co, uniform_co, pmx
from operator import attrgetter
import matplotlib.pyplot as plt


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
mutation_methods = [swap_mutation, creep_mutation, uniform_mutation, random_resetting]
selection_methods = [fps, tournament_sel, rank_selection]
crossover_methods = [single_point_co, multi_point_co, uniform_co, pmx]

# Record the results of each run in a list
results = []

# Run the genetic algorithm with each combination of mutation, selection, and crossover
for mutate in mutation_methods:
    for select in selection_methods:
        for crossover in crossover_methods:
            for _ in range(5):  # repeat the test N times
                # Initialize the population
                pop = Population(size=50, optim="min", sol_size=len(data_), valid_set=range(30), replacement=True)

                # Evolve the population
                pop.evolve(gens=40, xo_prob=0.9, mut_prob=0.2, select=select, mutate=mutate, crossover=crossover,
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

# To compute the average fitness for each combination:
average_results = {}
for result in results:
    combination = (result[0], result[1], result[2])  # mutation, selection, crossover
    if combination in average_results:
        average_results[combination].append(result[3])  # append the fitness
    else:
        average_results[combination] = [result[3]]  # initialize the list with the fitness

# Compute the averages
for combination in average_results:
    average_results[combination] = sum(average_results[combination]) / len(average_results[combination])

# To plot the results:
plt.figure(figsize=(10, 20))  # Increase figure size and invert axes

# Sort combinations by average fitness
sorted_combinations = sorted(average_results.items(), key=lambda x: x[1])

# Display combination names in a readable way
names_values = [(str(combination), average_fitness) for combination, average_fitness in sorted_combinations]

names = [name for name, _ in names_values]
values = [value for _, value in names_values]

plt.barh(names, values)  # Use barh for horizontal bars
plt.yticks(rotation=0, fontsize='xx-small')  # Make the y-axis text size smaller
plt.xlabel('Average Fitness')  # Invert x and y axes labels
plt.ylabel('Combination of Mutations')
plt.title('Average Fitness for each combination of mutation, selection and crossover methods')
plt.show()





