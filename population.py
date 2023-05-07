import os

import random
import numpy as np
import matplotlib.pyplot as plt

from chromosome import Chromosome
from constants import N, ENCODING


class Population:
    def __init__(self, chromosomes: list[Chromosome]):
        self.chromosomes = chromosomes
        self.phenotypes_list = np.fromiter(
            map(lambda chromosome: chromosome.fitness, self.chromosomes),
            dtype=np.float64,
        )
        self.genotypes_list = list(
            map(lambda chromosome: list(chromosome.code), self.chromosomes)
        )

    def print_ones_distribution(
        self, ff_name, selection_name, run, iteration, fitness_function, is_last_iteration=False
    ):
        if ff_name.startswith("FHD") or ff_name.startswith("FConst"):
            dir_path = f"BinaryChain/{N}/{ff_name}/{selection_name}/{run}/ones"
        else:
            dir_path = f"RealArgument-{ENCODING}/{N}/{ff_name}/{selection_name}/{run}/ones"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        length = len(self.genotypes_list[0])
 
        values = [genotype_list.count(1) for genotype_list in self.genotypes_list]
        boxes = 10
        counts, bins = np.histogram(values, bins=boxes)

        ones_min, ones_max = (0, length)
        ones_step = (ones_max - ones_min) / boxes
        ones_left, ones_right = int(ones_min - ones_step), int(ones_max + ones_step)
        ticks = np.arange(ones_left, ones_right, 1 if length == 10 else 10)

        kwargs = {} if not is_last_iteration else { 'width': ones_step / 10 if length == 100 else ones_step / 5 }

        f = plt.figure()
        plt.xlim(ones_left, ones_right)
        plt.xticks(ticks, rotation='vertical')
        plt.hist(bins[:-1], len(bins), weights=counts, **kwargs)
        plt.xlabel("Ones in a genotype bin")
        plt.ylabel("Number of individuals")
        plt.title("Ones distribution")
        plt.savefig(f"{dir_path}/{iteration}.png")
        f.clear()
        plt.close(f)

    def print_phenotypes_distribution(
        self, ff_name, selection_name, run, iteration, fitness_function, is_last_iteration=False
    ):
        if ff_name.startswith("FConst"):
            return 
        elif ff_name.startswith("FHD"):
            dir_path = f"BinaryChain/{N}/{ff_name}/{selection_name}/{run}/phenotypes"
        else:
            dir_path = f"RealArgument-{ENCODING}/{N}/{ff_name}/{selection_name}/{run}/phenotypes"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        length = len(self.genotypes_list[0])

        values = self.phenotypes_list
        boxes = 20 if length == 10 else 10
        counts, bins = np.histogram(values, bins=boxes)

        y_min, y_max = fitness_function.y
        y_step = (y_max - y_min) / boxes
        y_left, y_right = (y_min - y_step), (y_max + y_step)
        ticks = np.arange(y_left, y_right, y_step)

        kwargs = {} if not is_last_iteration else { 'width': y_step / 10 }

        f = plt.figure()
        plt.xlim(y_left, y_right)
        plt.xticks(ticks, rotation='vertical')
        plt.hist(bins[:-1], len(bins), weights=counts, **kwargs)
        plt.xlabel("Health")
        plt.ylabel("Number of individuals")
        plt.title("Phenotypes (fitness) distribution")
        plt.savefig(f"{dir_path}/{iteration}.png")
        f.clear()
        plt.close(f)

    def print_genotypes_distribution(
        self, ff_name, selection_name, run, iteration, fitness_function, is_last_iteration=False
    ):
        if ff_name.startswith("FConst"):
            return 
        elif ff_name.startswith("FHD"):
            dir_path = f"BinaryChain/{N}/{ff_name}/{selection_name}/{run}/genotypes"
        else:
            dir_path = f"RealArgument-{ENCODING}/{N}/{ff_name}/{selection_name}/{run}/genotypes"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        length = len(self.genotypes_list[0])

        values = [fitness_function.get_genotype_value(code) for code in self.genotypes_list]
        boxes = 20 if length == 10 else 10
        counts, bins = np.histogram(values, bins=boxes)

        x_min, x_max = fitness_function.a, fitness_function.b
        x_step = (x_max - x_min) / boxes
        x_left, x_right = (x_min - x_step), (x_max + x_step)
        ticks = np.arange(x_left, x_right, x_step)

        kwargs = {} if not is_last_iteration else { 'width': x_step / 10 }

        f = plt.figure()
        plt.xlim(x_left, x_right)
        plt.xticks(ticks, rotation='vertical')
        plt.hist(bins[:-1], len(bins), weights=counts, **kwargs)
        plt.xlabel("x")
        plt.ylabel("Number of individuals")
        plt.title("Genotype (x) distribution")
        plt.savefig(f"{dir_path}/{iteration}.png")
        f.clear()
        plt.close(f)

    def estimate_convergence(self, p_m):
        if not p_m or p_m == 0:
            return self.is_identical
        else:
            return self.is_homogeneous(percentage=99)

    def is_homogeneous(self, percentage: int) -> bool:
        assert percentage < 100, (
            "According to formula: (unique / total) * 100 <= 100 - percentage, "
            "we can't have percentage >= 100!"
        )
        chromosomes = [self.bin2int(genotype) for genotype in self.genotypes_list]
        total = len(chromosomes)
        unique = len(set(chromosomes))
        return (unique / total) * 100 <= 100 - percentage

    @property
    def is_identical(self) -> bool:
        genotypes = {self.bin2int(genotype) for genotype in self.genotypes_list}
        return len(genotypes) == 1

    def crossover(self, fitness_function, p_c):
        if p_c == 0:
            return

        next_chromosomes = []

        chromosomes = self.chromosomes.copy()

        def pop_chromosome():
            index = random.randrange(0, len(chromosomes))
            return chromosomes.pop(index)

        next_key = 0

        while len(chromosomes) > 0:
            parent1 = pop_chromosome()
            parent2 = pop_chromosome()

            crossover_point = int(random.random() * len(parent1.code))

            child_code1 = [
                *parent1.code[:crossover_point],
                *parent2.code[crossover_point:],
            ]
            child_chromosome1 = Chromosome(
                child_code1, fitness_function.estimate(child_code1), next_key + 1
            )

            child_code2 = [
                *parent2.code[:crossover_point],
                *parent1.code[crossover_point:],
            ]
            child_chromosome2 = Chromosome(
                child_code2, fitness_function.estimate(child_code2), next_key + 2
            )

            next_chromosomes.append(child_chromosome1)
            next_chromosomes.append(child_chromosome2)

            next_key += 2

        self.update_chromosomes(next_chromosomes)

    def mutate(self, fitness_function, p_m):
        if p_m == 0:
            return
        for chromosome in self.chromosomes:
            for i in range(0, len(chromosome.code)):
                if random.random() < p_m:
                    chromosome.code[i] = int(not chromosome.code[i])
                    chromosome.fitness = fitness_function.estimate(chromosome.code)
        self.update()

    def get_mean_fitness(self):
        return self.phenotypes_list.mean()

    def get_max_fitness(self):
        return self.phenotypes_list.max()

    def get_fitness_std(self):
        return self.phenotypes_list.std()

    def get_best_genotype(self) -> list[int]:
        best_index = self.phenotypes_list.argmax()
        best_genotype = self.genotypes_list[best_index]
        return best_genotype

    def get_best_chromosomes(self) -> list[Chromosome]:
        max_fitness = self.get_max_fitness()
        best_phenotypes_indices = np.argwhere(self.phenotypes_list == max_fitness)[0].astype(np.int8)
        best_chromosomes_duplicated = [self.chromosomes[i] for i in best_phenotypes_indices]
        best_chromosomes_keys = set()
        best_chromosomes = [
            chromosome for chromosome in best_chromosomes_duplicated
            if chromosome.key not in best_chromosomes_keys
            and not best_chromosomes_keys.add(chromosome.key)
        ]
        return best_chromosomes

    def get_best_chromosome(self) -> Chromosome:
        best_index = self.phenotypes_list.argmax()
        best_chromosome = self.chromosomes[best_index]
        return best_chromosome

    def get_keys_list(self):
        return list(map(lambda chromosome: chromosome.key, self.chromosomes))

    def get_chromosomes_copies_count(self, chromosome_sample_or_list):
        if type(chromosome_sample_or_list) == list:
            chromosome_list = chromosome_sample_or_list
            return self.get_chromosomes_copy_count(chromosome_list)
        else:
            chromosome_sample = chromosome_sample_or_list
            return self.get_chromosomes_copy_count([chromosome_sample])

    def get_chromosomes_copy_count(self, chromosome_list: list[Chromosome]):
        copies_count = 0
        genotypes_available = [self.bin2int(genotype) for genotype in self.genotypes_list]
        genotype_copies = {self.bin2int(chromosome.code) for chromosome in chromosome_list}

        for genotype_available in genotypes_available:
            copies_count += 1 if genotype_available in genotype_copies else 0
        return copies_count

    def bin2int(self, bits):
        total = 0
        for shift, j in enumerate(bits[::-1]):
            if j:
                total += 1 << shift
        return total

    def get_chromosomes_copies_counts(self, genotypes: list[list[int]]) -> int:
        all_genotypes = [self.bin2int(genotype) for genotype in self.genotypes_list]
        unique_genotypes = {self.bin2int(genotype) for genotype in genotypes}

        copies_count = 0
        for genotype in unique_genotypes:
            copies_count += all_genotypes.count(genotype)
        return copies_count

    def update(self):
        self.phenotypes_list = np.fromiter(
            map(lambda chromosome: chromosome.fitness, self.chromosomes),
            dtype=np.float64,
        )
        self.genotypes_list = list(
            map(lambda chromosome: list(chromosome.code), self.chromosomes)
        )

    def update_rws(self, probabilities):
        self.chromosomes = np.random.choice(self.chromosomes, len(self.chromosomes), p=probabilities).tolist()
        self.update()

    def update_chromosomes(self, chromosomes):
        self.chromosomes = chromosomes
        self.update()

    def override_chromosome_keys(self):
        for index, chromosome in enumerate(self.chromosomes):
            self.chromosomes[index] = chromosome.clone(key=index)

    def __copy__(self):
        return Population(self.chromosomes.copy())
