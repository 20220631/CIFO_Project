from random import uniform, choice, sample
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":

        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        raise NotImplementedError

    else:
        raise Exception("No optimization specified (min or max).")


def tournament_sel(population, size=4):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: The best individual in the tournament.
    """

    # Select individuals based on tournament size
    # with choice, there is a possibility of repetition in the choices,
    # so every individual has a chance of getting selected
    tournament = [choice(population.individuals) for _ in range(size)]

    # with sample, there is no repetition of choices
    # tournament = sample(population.individuals, size)
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    if population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))


def rank_selection(population):
    # Ranked-Based Selection
    # Rank the individuals based on their fitness values (i.e., cost)
    ranked_indiv = sorted(population, key=lambda x: x.fitness_value)

    # Assign a selection probability to each individual based on its rank
    total_rank = sum(range(1, len(population)+1))
    selection_probs = []
    for i in range(1, len(population)+1):
        selection_probs.append(r/total_rank)

    # Select the parents based on their selection probabilities
    parents = []
    for i in range(2): # so queremos 2 parents
        selected_index = random.choices(range(len(population)), weights=selection_probs)[0]
        parents.append(population[selected_index])

    return parents

import random
def roulette_wheel_selection(population, costs):
    total_cost = sum(costs)
    cumulative_probabilities = [sum(costs[:i + 1]) / total_cost for i in range(len(costs))]
    roulette_value = random.random()
    selected_index = 0
    for i in range(len(cumulative_probabilities)):
        if roulette_value <= cumulative_probabilities[i]:
            selected_index = i
            break
    return population[selected_index]
