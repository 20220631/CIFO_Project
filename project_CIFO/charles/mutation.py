from random import randint, sample
import  random


def binary_mutation(individual):
    """Binary mutation for a GA individual. Flips the bits.

    Args:
        individual (Individual): A GA individual from charles.py

    Raises:
        Exception: When individual is not binary encoded.py

    Returns:
        Individual: Mutated Individual
    """
    mut_index = randint(0, len(individual) - 1)

    if individual[mut_index] == 0:
        individual[mut_index] = 1
    elif individual[mut_index] == 1:
        individual[mut_index] = 0
    else:
        raise Exception(
            f"Trying to do binary mutation on {individual}. But it's not binary.")
    return individual


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
    """Nuno
    Creep mutation for a GA individual. Slightly alters the quantity of a selected food item.

    Args:
        individual (Individual): A GA individual. In this case, each gene represents a quantity of a particular food item.

    Returns:
        Individual: The mutated individual. The mutation is performed in-place.
    """
    index = randint(0, len(individual) - 1)  # select a random index
    individual[index] += randint(-1, 1)  # slightly alter its value
    individual[index] = min(max(0, individual[index]), 7)  # ensure the quantity stays within bounds
    return individual

def inversion_mutation(individual):
    """Inversion mutation for a GA individual. Reverts a portion of the representation.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    # mut_indexes = [0,3]
    mut_indexes.sort()
    individual[mut_indexes[0]:mut_indexes[1]] = individual[mut_indexes[0]:mut_indexes[1]][::-1]
    return individual


def uniform_mutation(individual, mutation_rate, min_value, max_value, nutrient_data):
    # nutrient_data argument is a list of lists containing the calorie and nutrient values for each food item
    mutated_individual = individual.copy()

    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            mutated_individual[i] += random.uniform(min_value, max_value)

            # Ensure that the mutated value is within the allowed range
            mutated_individual[i] = max(mutated_individual[i], min_value)
            mutated_individual[i] = min(mutated_individual[i], max_value)

            # Adjust the mutated individual to satisfy nutrient constraints
            total_calories = sum([mutated_individual[i] * nutrient_data[i][0] for i in range(len(mutated_individual))])
            total_nutrients = [sum([mutated_individual[i] * nutrient_data[i][j] for i in range(len(mutated_individual))]) for j in range(1, len(nutrient_data[0]))]

            while total_calories > 3000:
                # Reduce the quantity of high-calorie foods to balance the total calories
                high_calorie_indices = [i for i in range(len(mutated_individual)) if nutrient_data[i][0] >= 150]
                if not high_calorie_indices:
                    break
                index = random.choice(high_calorie_indices)
                reduction = min(mutated_individual[index], 1)
                mutated_individual[index] -= reduction
                total_calories -= nutrient_data[index][0] * reduction

            while any([nutrient < 0 for nutrient in total_nutrients]):
                # Increase the quantity of low-nutrient foods to balance the nutrients
                low_nutrient_indices = [i for i in range(len(mutated_individual)) if nutrient_data[i][1:] == [0, 0, 0, 0, 0]]
                if not low_nutrient_indices:
                    break
                index = random.choice(low_nutrient_indices)
                increase = min(max_value - mutated_individual[index], 1)
                mutated_individual[index] += increase
                total_nutrients = [sum([mutated_individual[i] * nutrient_data[i][j] for i in range(len(mutated_individual))]) for j in range(1, len(nutrient_data[0]))]

    return mutated_individual


if __name__ == '__main__':
    test = [1, 2, 3, 4, 5, 6]
    test = inversion_mutation(test)
    print(test)
















