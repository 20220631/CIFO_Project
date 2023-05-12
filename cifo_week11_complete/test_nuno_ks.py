from charles.charles import Population, Individual
#from charles.search import hill_climb, sim_annealing
from copy import deepcopy
from data.data import data, nutrients
from charles.selection import fps, tournament_sel
from charles.mutation import binary_mutation
from charles.crossover import single_point_co
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
        if self.representation[bit] == 1:
            fitness += data[bit][2]  # cost of the selected item
            for nutrient_index in range(len(nutrients)):
                nutrient_totals[nutrient_index] += data[bit][3 + nutrient_index]

    # Apply a penalty if nutrient minimums are not met
    penalty = 0
    for nutrient_index in range(len(nutrients)):
        if nutrient_totals[nutrient_index] < nutrients[nutrient_index][1]:
            penalty += (nutrients[nutrient_index][1] - nutrient_totals[nutrient_index]) * 1000

    return fitness + penalty


def get_neighbours(self):
    """A neighbourhood function for the Stigler Diet Problem, for each neighbour, flips the bits
    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation))]

    for index, neighbour in enumerate(n):
        if neighbour[index] == 1:
            neighbour[index] = 0
        elif neighbour[index] == 0:
            neighbour[index] = 1

    n = [Individual(i) for i in n]
    return n




# Monkey Patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours

pop = Population(size=30, optim="min", sol_size=len(data), valid_set=[0, 1], replacement=True)

pop.evolve(gens=100, xo_prob=0.9, mut_prob=0.2, select=tournament_sel, mutate=binary_mutation, crossover=single_point_co, elitism=True)