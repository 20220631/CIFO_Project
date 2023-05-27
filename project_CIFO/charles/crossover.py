from random import sample, randint


def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = randint(1, len(p1)-2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2


def multi_point_co(p1, p2, num_points=2):
    """Implementation of multi-point crossover.

    Args:
        p1 (list): First parent for crossover.
        p2 (list): Second parent for crossover.
        num_points (int, optional): Number of crossover points. Defaults to 2.

    Returns:
        tuple: Two offspring, resulting from the crossover.
    """
    # Make sure we have enough points to perform crossover
    assert num_points < len(
        p1), "Number of crossover points must be less than the length of the parent representations."

    # Generate crossover points
    co_points = sorted(sample(range(1, len(p1)), num_points))

    offspring1, offspring2 = [], []
    for i in range(num_points + 1):
        if i == 0:
            start, end = 0, co_points[0]
        elif i == num_points:
            start, end = co_points[i - 1], len(p1)
        else:
            start, end = co_points[i - 1], co_points[i]

        if i % 2 == 0:  # if even
            offspring1.extend(p1[start:end])
            offspring2.extend(p2[start:end])
        else:  # if odd
            offspring1.extend(p2[start:end])
            offspring2.extend(p1[start:end])

    return offspring1, offspring2


def uniform_co(p1, p2):
    """
    Implementation of uniform crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    offspring1 = []
    offspring2 = []

    for gene1, gene2 in zip(p1, p2):
        if randint(0, 1) == 0:
            offspring1.append(gene1)
            offspring2.append(gene2)
        else:
            offspring1.append(gene2)
            offspring2.append(gene1)

    return offspring1, offspring2


def pmx(parent1, parent2):
    # Create empty offspring
    offspring1 = [None] * len(parent1)
    offspring2 = [None] * len(parent2)

    # Select random crossover points
    point1 = randint(0, len(parent1) - 1)
    point2 = randint(0, len(parent1) - 1)

    # Ensure point2 is greater than point1
    if point2 < point1:
        point1, point2 = point2, point1

    # Copy the selected segment from parent1 to offspring
    offspring1[point1:point2+1] = parent1[point1:point2+1]
    offspring2[point1:point2+1] = parent2[point1:point2+1]

    # Map the values from parent2 to the corresponding positions in offspring
    for i in range(point1, point2+1):
        if parent2[i] not in offspring1:
            while offspring1[i] is None:
                index = parent2.index(parent1[i])
                if offspring1[index] is None:
                    offspring1[index] = parent2[i]
                else:
                    offspring1[i] = parent2[i]
        else:
            offspring1[i] = parent2[i]

    # Map the values from parent1 to the corresponding positions in offspring
    for i in range(point1, point2+1):
        if parent1[i] not in offspring2:
            while offspring2[i] is None:
                index = parent1.index(parent2[i])
                if offspring2[index] is None:
                    offspring2[index] = parent1[i]
                else:
                    offspring2[i] = parent1[i]
        else:
            offspring2[i] = parent1[i]

    # Fill the remaining positions in offspring with values from parent2
    for i in range(len(offspring1)):
        if offspring1[i] is None:
            offspring1[i] = parent2[i]
        if offspring2[i] is None:
            offspring2[i] = parent1[i]

    return offspring1, offspring2




if __name__ == '__main__':
    #p1, p2 = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10], [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
    p1, p2 = [0.1,0.15,0.3],[0.3,0.1,0.2]
    o1, o2 = pmx(p1, p2)
    print(o1, o2)