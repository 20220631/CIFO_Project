from random import uniform, choice, sample, choices, random
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.

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
        # Was here before: raise NotImplementedError
        # The new changes:

        # Find individual in the position of the spin
        for individual in population:
            # Reverse the selection process for minimization
            # Subtracting individual fitness from total fitness emphasizes smaller fitness values, reducing their contribution to the position.
            position += total_fitness - individual.fitness
            if position > spin:
                return individual

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
    for r in range(1, len(population)+1):
        selection_probs.append(r/total_rank)

    # Select the parents based on their selection probabilities
    parents = []
    for i in range(2): # so queremos 2 parents
        selected_index = choices(range(len(population)), weights=selection_probs)[0]
        parents.append(population[selected_index])

    return parents

def roulette_wheel_selection(population):
    total_fitness = sum(individual.fitness for individual in population)
    for _ in range(len(population)):
        r = random() * total_fitness
        cumulative_fitness = 0

        for individual in population:
            try:
                selected = individual
                cumulative_fitness += individual.fitness
                if cumulative_fitness >= r:
                    selected= individual
                    break
            except AttributeError:
                # Handle the AttributeError when fitness is not defined
                pass

    return selected
