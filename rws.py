import random

from population import Population


class RankExponentialRWS:
    def __init__(self, c: float):
        self.c = c

    def exponential_rws(self, population: Population):
        N = len(population.chromosomes)

        ranks = list(map(lambda index: N - index, range(0, N)))
        probabilities = list(map(lambda rank: self.scale(N, rank), ranks))

        if sum(probabilities) == 0:
            return population

        population.update_rws(probabilities)

        return population

    def select(self, population: Population):
        chromosomes = population.chromosomes.copy()
        random.shuffle(chromosomes)
        chromosomes = self.sort(chromosomes)
        population.update_chromosomes(chromosomes)
        return self.exponential_rws(population)

    def scale(self, size: int, rank: int) -> float:
        return ((self.c - 1) / (pow(self.c, size) - 1)) * pow(self.c, size - rank)

    def sort(self, chromosomes):
        return sorted(
            chromosomes.copy(), key=lambda chromosome: chromosome.fitness, reverse=True
        )

    def __repr__(self):
        return f"RankExponentialRWS[c={self.c}]"
