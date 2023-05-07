from typing import List
from constants import G
from population import Population
from numpy import random
from statistics import mean
from chromosome import Chromosome


def get_candidate_indexes(population:Population, t):
    indexes = random.choice(len(population.chromosomes), size=t, replace=False)
    return indexes


class Selection:
    def select(self, population_with_health):
        raise NotImplementedError


class TournamentReturn(Selection):
    def __init__(self, t):
        self.t = t

    def select(self, population: Population):
        """
        population [(candidate, health_fun(candidate))]
        t (number of candidates) == self.t
        """
        n = len(population.chromosomes)
        mating_pool: List[Population] = []
        while len(mating_pool) != n:
            indexes = get_candidate_indexes(population, self.t)
            candidates = [population.chromosomes[i] for i in indexes]
            random.shuffle(candidates)
            best = sorted(candidates, key=lambda chrom: chrom.fitness, reverse=True)[0]
            mating_pool.append(best)
        population.update_chromosomes(mating_pool)
        return population

    def __repr__(self):
        return f"TournamentReturn[t={self.t}]"


class TournamentNoReturn(Selection):
    def __init__(self, t):
        self.t = t

    def select(self, population: Population):
        """
        population [(candidate, health_fun(candidate))]
        t (number of candidates) == self.t
        """
        # make t copies of population
        population_copies = [Population(population.chromosomes.copy()) for x in range(self.t)]
        current_population = Population(population.chromosomes.copy())
        n = len(population.chromosomes)
        mating_pool = []
        i = 0
        while len(mating_pool) != n:
            # todo fix for odd number
            if len(current_population.chromosomes) < self.t:
                # if there are less than t inds left in pop. - we can't make tournament
                # and need to replace population with a new one
                current_population = population_copies[i]
                i+=1
            indexes = get_candidate_indexes(current_population, self.t)
            candidates = [current_population.chromosomes[i] for i in indexes]
            for c in candidates:
                current_population.chromosomes.remove(c)
            random.shuffle(candidates)
            best = sorted(candidates, key=lambda chrom: chrom.fitness, reverse=True)[0]
            mating_pool.append(best)
        population.update_chromosomes(mating_pool)
        return population

    def __repr__(self):
        return f"TournamentNoReturn[t={self.t}]"

#%%
