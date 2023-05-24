from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from copy import deepcopy
from data.data import data_, nutrients
from charles.selection import fps, tournament_sel, roulette_wheel_selection
from charles.mutation import swap_mutation, creep_mutation, uniform_mutation
from charles.crossover import single_point_co, multi_point_co, uniform_co, pmx
from random import random, choice
from operator import attrgetter


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


def get_neighbours(self):
    """A neighbourhood function for the Stigler Diet Problem, for each neighbour, randomly adds or subtracts a bit
    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation))]

    for index, neighbour in enumerate(n):
        neighbour[index] += choice([-1, 1])

        neighbour[index] = max(0, neighbour[index])  # Lower bound
        neighbour[index] = min(29, neighbour[index])  # Upper bound

    n = [Individual(i) for i in n]
    return n




# Monkey Patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours

#pop = Population(size=100, optim="min", sol_size=len(data_), valid_set=range(20), replacement=True)
#pop.evolve(gens=200, xo_prob=0.9, mut_prob=0.2, select=tournament_sel, mutate=creep_mutation, crossover=uniform_co, elitism=True)

# List all the combinations of mutation, selection and crossover
mutation_methods = [swap_mutation, creep_mutation, uniform_mutation]
selection_methods = [tournament_sel, fps]
crossover_methods = [single_point_co, uniform_co, multi_point_co, pmx]

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
                pop.evolve(gens=20, xo_prob=0.9, mut_prob=0.2, select=select, mutate=mutate, crossover=crossover,
                           elitism=True)

                # Get the best individual
                if pop.optim == "max":
                    best_individual = max(pop.individuals, key=attrgetter("fitness"))
                elif pop.optim == "min":
                    best_individual = min(pop.individuals, key=attrgetter("fitness"))

                # Record the result of the run (assuming that the best fitness is what you want to record)
                results.append((mutate.__name__, select.__name__, crossover.__name__, best_individual.get_fitness()))

# At the end of this loop, `results` should be a list where each item is a tuple containing:
# (mutation method name, selection method name, crossover method name, best fitness achieved)


import matplotlib.pyplot as plt

# Assuming the results are as above, with each item being a tuple of:
# (mutation method name, selection method name, crossover method name, best fitness achieved)

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
plt.figure(figsize=(20,10)) # Increase figure size

# sort combinations by average fitness
sorted_combinations = sorted(average_results.items(), key=lambda x: x[1])

names = ['\n'.join(combination) for combination, _ in sorted_combinations]
values = [average_fitness for _, average_fitness in sorted_combinations]

plt.bar(names, values)
plt.xticks(rotation=0,fontsize='xx-small') # Make the text size smaller
plt.xlabel('Average Fitness')
plt.ylabel('Fitness')
plt.title('Average Fitness for each combination of mutation, selection, crossover methods')
plt.show()


