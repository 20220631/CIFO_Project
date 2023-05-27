from random import uniform, choice, choices
from operator import attrgetter


def fps(population):
    """
    Fitness Proportionate Selection (FPS), also known as "roulette wheel selection",
    for a genetic algorithm.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: Selected individual.
    """

    total_fitness = sum([i.fitness for i in population])

    # Randomly select a spin value between 0 and total_fitness
    spin = uniform(0, total_fitness)
    position = 0

    if population.optim == "max":
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":

        # Find individual in the position of the spin
        for individual in population:

            # Reverse the selection process for minimization
            # Subtracting individual fitness from total fitness emphasizes smaller fitness values,
            # reducing their contribution to the position.
            position += total_fitness - individual.fitness
            if position > spin:
                return individual

    else:
        raise Exception("No optimization specified (min or max).")


def tournament_sel(population, size=10):
    """
    Tournament selection for a genetic algorithm.
    It selects a number (size parameter) of Individuals from the population and picks the best among them.

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
    """
    Rank selection for a genetic algorithm.

    This function performs a rank selection: it ranks the individuals by fitness, then
    selects individuals according to their rank.

    Args:
        population (Population): The population from which to select individuals.

    Returns:
        Individual: The selected individual.


    """

    # Rank-Based Selection
    # Select parents based on their ranks in the population
    num_parents= 1
    sorted_population = sorted(population, key=attrgetter("fitness"))
    total_rank = sum(range(1, len(population) + 1))
    selection_probs = [rank / total_rank for rank in range(1, len(population) + 1)]

    parents = choices(sorted_population, weights=selection_probs, k=1)

    return parents[0]
