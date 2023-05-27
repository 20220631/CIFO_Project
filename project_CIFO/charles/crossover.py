from random import sample, randint


def single_point_co(p1, p2):
    """
    Single-point crossover creates offspring by choosing a random crossover point in the parent chromosomes,
    then swapping all genes after that point between the two parents.
    This results in each offspring sharing some initial genes with one parent and the rest with the other parent.

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
    """
    Multipoint crossover creates offspring by choosing multiple random crossover points in the parent chromosomes,
    then swapping all genes between those points. The swapping occurs alternatively between the parents,
    resulting in a mix of genes from both parents.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.
        num_points (int, optional): Number of crossover points. Defaults to 2.

    Returns:
        Two offspring, resulting from the crossover.
    """
    # Make sure we have enough points to perform crossover
    assert num_points < len(p1), "Number of crossover points must be less than the length of the parent representations"

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
    Uniform crossover creates offspring by visiting each gene in the parent chromosomes and,
    with a 50% chance, swapping that gene between the two parents.
    In this way, each offspring is a mix of both parents' genes.

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


def pmx(p1, p2):
    """
    PMX (Partially Mapped Crossover) operates in the following way:
        1. Two crossover points are selected on parent chromosomes
        2. The segment between these points is directly copied from parents to offspring
        3. From the remaining chromosome, each value maps to the position of that value in the other parent.
        4. Complete the chromosome by preserving the position of each value in the selected segment from the parent.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Two offspring, resulting from the crossover. Each offspring is a permutation of the parent genes.
    """

    # Create empty offspring
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p2)

    # Select random crossover points
    point1 = randint(0, len(p1) - 1)
    point2 = randint(0, len(p1) - 1)

    # Ensure point2 is greater than point1
    if point2 < point1:
        point1, point2 = point2, point1

    # Copy the selected segment from parent1 to offspring
    offspring1[point1:point2+1] = p1[point1:point2+1]
    offspring2[point1:point2+1] = p2[point1:point2+1]

    # Map the values from parent2 to the corresponding positions in offspring
    for i in range(point1, point2+1):
        if p2[i] not in offspring1:
            while offspring1[i] is None:
                index = p2.index(p1[i])
                if offspring1[index] is None:
                    offspring1[index] = p2[i]
                else:
                    offspring1[i] = p2[i]
        else:
            offspring1[i] = p2[i]

    # Map the values from parent1 to the corresponding positions in offspring
    for i in range(point1, point2+1):
        if p1[i] not in offspring2:
            while offspring2[i] is None:
                index = p1.index(p2[i])
                if offspring2[index] is None:
                    offspring2[index] = p1[i]
                else:
                    offspring2[i] = p1[i]
        else:
            offspring2[i] = p1[i]

    # Fill the remaining positions in offspring with values from parent2
    for i in range(len(offspring1)):
        if offspring1[i] is None:
            offspring1[i] = p2[i]
        if offspring2[i] is None:
            offspring2[i] = p1[i]

    return offspring1, offspring2
