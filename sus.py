import random

from numpy import random

from population import Population


def basic_sus(population: Population, probabilities: float, probability_scale: list):
    mating_pool = []
    number_of_parents = len(population.chromosomes)
    fitness_step = probabilities / number_of_parents
    random_offset = random.uniform(0, fitness_step)
    current_fitness_pointer = random_offset
    last_fitness_scale_position = 0

    for _ in range(len(population.chromosomes)):
        for fitness_scale_position in range(
            last_fitness_scale_position, len(probability_scale)
        ):
            if probability_scale[fitness_scale_position] >= current_fitness_pointer:
                mating_pool.append(population.chromosomes[fitness_scale_position])
                last_fitness_scale_position = fitness_scale_position
                break
        current_fitness_pointer += fitness_step

    return mating_pool


class RankExponentialSUS:
    def __init__(self, c: float):
        self.c = c

    def exponential_sus(self, population: Population):
        probabilities_total = 0
        probability_scale = []

        N = len(population.chromosomes)

        ranks = list(map(lambda index: N - index, range(0, N)))
        probabilities = list(map(lambda rank: self.scale(N, rank), ranks))

        for index, probability in enumerate(probabilities):
            probabilities_total += probability
            if index == 0:
                probability_scale.append(probability)
            else:
                probability_scale.append(probability + probability_scale[index - 1])

        mating_pool = basic_sus(population, probabilities_total, probability_scale)
        population.update_chromosomes(mating_pool)

        return population

    def select(self, population: Population):
        chromosomes = population.chromosomes.copy()
        random.shuffle(chromosomes)
        chromosomes = self.sort(chromosomes)
        population.update_chromosomes(chromosomes)
        return self.exponential_sus(population)

    def scale(self, size: int, rank: int) -> float:
        return ((self.c - 1) / (pow(self.c, size) - 1)) * pow(self.c, size - rank)

    def sort(self, chromosomes):
        return sorted(
            chromosomes.copy(), key=lambda chromosome: chromosome.fitness, reverse=True
        )

    def __repr__(self):
        return f"RankExponentialSUS[c={self.c}]"
