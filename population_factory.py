from numpy import random
from chromosome import Chromosome
from population import Population


class PopulationFactory:
    def __init__(self, fitness_function):
        self.fitness_function = fitness_function

    def generate(self, n, l):
        ff_name = repr(self.fitness_function) 

        chromosomes = [] if ff_name.startswith("FConst") else [self.fitness_function.generate_optimal(l)]

        start = len(chromosomes)

        for key in range(start, n):
            code = random.binomial(n=1, p=0.5, size=l)
            fitness = self.fitness_function.estimate(code)
            chromosomes.append(Chromosome(code, fitness, key + 1))

        return Population(chromosomes)
