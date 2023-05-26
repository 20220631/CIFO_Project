from random import random, randint, sample, choice, uniform



def swap_mutation(individual):
    """Swap mutation for a GA individual. Swaps the bits.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    individual[mut_indexes[0]], individual[mut_indexes[1]] = individual[mut_indexes[1]], individual[mut_indexes[0]]
    return individual

def creep_mutation(individual):
    """
    Creep mutation for a GA individual. Slightly alters the quantity of a selected food item.

    Args:
        individual (Individual): A GA individual. In this case, each gene represents a quantity of a particular food item.

    Returns:
        Individual: The mutated individual. The mutation is performed in-place.
    """
    index = randint(0, len(individual) - 1)  # select a random index
    individual[index] += uniform(-1,1)  # slightly alter its value
    individual[index] = min(max(0, individual[index]), 1)  # ensure the quantity stays within bounds
    return individual


def uniform_mutation(individual, mutation_rate=0.5, min_value=0, max_value=30):
    """Perform uniform mutation on the individual.

    Args:
        individual (list): The individual to mutate.
        mutation_rate (float): The probability of each gene being mutated.
        min_value (int): The minimum possible value for a gene.
        max_value (int): The maximum possible value for a gene.

    Returns:
        list: The mutated individual.
    """
    mutated_solution = individual[:]  # Create a copy of the original solution

    for i in range(len(mutated_solution)):
        if random() < mutation_rate:
            mutated_solution[i] = uniform(0,1)

    return mutated_solution



def random_resetting(individual):
    """
    Random resetting mutation for a GA individual. Randomly resets the quantity of a selected food item.

    Args:
        individual (Individual): A GA individual. In this case, each gene represents a quantity of a particular food item.

    Returns:
        Individual: The mutated individual. The mutation is performed in-place.
    """
    index = randint(0, len(individual) - 1)  # select a random index
    individual[index] = uniform(0,1)  # reset its value to a random quantity
    return individual

if __name__ == '__main__':
    test = [1, 2, 3, 4, 5, 6]
    test = swap_mutation(test)
    print(test)













