import numpy as np

from chromosome import Chromosome
from constants import DELTA, SIGMA
from population_factory import PopulationFactory
from coding import *


class FHD:
    def __init__(self, delta: float = 100.0):
        self.delta = delta
        self.a = 0
        self.b = 100
        self.x = (self.a, self.b)
        self.y = (self.estimate([0]*100), self.estimate([1]*100))
        self.factory = PopulationFactory(self)

    def get_genotype_value(self, chromosome_code):
        k = np.count_nonzero(chromosome_code)
        return k

    def estimate(self, chromosome_code):
        l = len(chromosome_code)
        k = l - np.count_nonzero(chromosome_code)
        return (l - k) + k * self.delta

    def generate_optimal(self, length):
        coding = np.zeros((length, ), dtype=int)
        return Chromosome(coding, self.estimate(coding))

    def get_optimal(self, n, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l):
        return self.factory.generate(n, l)

    def __repr__(self):
        return "FHD"


class FConst:
    def __init__(self):
        self.a = 0
        self.b = 100
        self.x = (self.a, self.b)
        self.y = (self.score(self.a), self.score(self.b))
        self.factory = PopulationFactory(self)

    def get_genotype_value(self, chromosome_code):
        k = np.count_nonzero(chromosome_code)
        return k

    def score(self, x: float):
        return 100

    def estimate(self, chromosome_code):
        return len(chromosome_code)

    def generate_optimal(self, length: int):
        return Chromosome(np.zeros((length,), dtype=int), length)

    def generate_population(self, n, l):
        return self.factory.generate(n, l)

    def get_optimal(self, n, l):
        return self.generate_optimal(l)

    def __repr__(self):
        return "FConst"


class Fx2:
    def __init__(self):
        self.a = 0
        self.b = 10.23
        self.x = (self.a, self.b)
        self.y = (self.score(self.a), self.score(self.b))
        self.factory = PopulationFactory(self)

    def score(self, x: float):
        return math.pow(x, 2)

    def estimate(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        y = self.score(x)
        return y

    def get_genotype_value(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        return x

    def get_optimal(self, n, l):
        return self.generate_optimal(l)

    def generate_optimal(self, length):
        x_max = self.x[1]
        coding = encode(x_max, self.a, self.b, length)
        return Chromosome(coding, self.estimate(coding))

    def generate_population(self, n, l):
        return self.factory.generate(n, l)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = decode(chromosome.code, self.a, self.b, len(chromosome.code))
        x_max = self.x[1]
        y = self.score(x)
        y_max = self.y[1]
        return abs(y_max - y) <= DELTA and abs(x_max - x) <= SIGMA

    def __repr__(self):
        return "Fx2"


class F5122subx2:
    def __init__(self):
        self.a = -5.12
        self.b = 5.11
        self.x = (self.a, 0)
        self.y = (self.score(self.a), self.score(0))
        self.factory = PopulationFactory(self)

    def score(self, x: float):
        return math.pow(5.12, 2) - math.pow(x, 2)

    def estimate(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        y = self.score(x)
        return y

    def get_genotype_value(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        return x

    def get_optimal(self, n, l):
        return self.generate_optimal(l)

    def generate_optimal(self, length):
        x_max = 0
        coding = encode(x_max, self.a, self.b, length)
        return Chromosome(coding, self.estimate(coding))

    def generate_population(self, n, l):
        return self.factory.generate(n, l)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = decode(chromosome.code, self.a, self.b, len(chromosome.code))
        x_max = self.x[1]
        y = self.score(x)
        y_max = self.y[1]
        return abs(y_max - y) <= DELTA and abs(x_max - x) <= SIGMA
    
    def __repr__(self):
        return "F5122subx2"


class Fecx:
    def __init__(self, c: float):
        self.a = 0
        self.b = 10.23
        self.x = (self.a, self.b)
        self.y = (self.score(self.a), self.score(self.b))
        self.c = c
        self.factory = PopulationFactory(self)

    def score(self, x: float):
        return math.exp(self.c * x)

    def estimate(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        return self.score(x)

    def get_genotype_value(self, chromosome_code):
        x = decode(chromosome_code, self.a, self.b, len(chromosome_code))
        return x

    def generate_optimal(self, length):
        x_max = self.x[1]
        coding = encode(x_max, self.a, self.b, length)
        return Chromosome(coding, self.estimate(coding))

    def get_optimal(self, n, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l):
        return self.factory.generate(n, l)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = decode(chromosome.code, self.a, self.b, len(chromosome.code))
        x_max = self.x[1]
        y = self.score(x)
        y_max = self.y[1]
        return abs(y_max - y) <= DELTA and abs(x_max - x) <= SIGMA

    def __repr__(self):
        return "Fecx"
