from pressure_stats import PressureStats
from selection_diff_stats import SelectionDiffStats
from reproduction_stats import ReproductionStats
from noise_stats import NoiseStats
from run import Run
from population import Population
from functions import *
from constants import *


class EvoAlgorithm:
    def __init__(
        self,
        initial_population: Population,
        selection_function,
        fitness_function,
        optimal,
        p_m: float | None,
        p_c: float | None,
    ):
        self.population: Population = initial_population
        self.selection_function = selection_function
        self.iteration = 0
        self.pressure_stats = PressureStats()
        self.reproduction_stats = ReproductionStats()
        self.selection_diff_stats = SelectionDiffStats()
        self.best = self.population.get_best_genotype()
        self.optimal_chromosome = fitness_function.generate_optimal(len(initial_population.genotypes_list[0]))
        self.pressure_stats.num_of_best.append(
            self.population.genotypes_list.count(self.best)
        )
        self.pressure_stats.f_best.append(self.population.get_max_fitness())
        self.fitness_function = fitness_function
        self.optimal = optimal
        self.p_m = p_m
        self.p_c = p_c

    def run(self, run, folder_name):
        self.iteration = 0
        avg_fitness_list = [self.population.get_mean_fitness()]
        std_fitness_list = [self.population.get_fitness_std()]
        optimal_count = [self.population.get_chromosomes_copies_count(self.optimal_chromosome)]
        stop = G
        convergent = self.population.estimate_convergence(self.p_m)

        ff_name = repr(self.fitness_function)

        while not convergent and self.iteration < stop:
            if run < ITERATIONS_TO_REPORT and self.iteration < ITERATIONS_TO_REPORT:
                sf_name = repr(self.selection_function)
                self.population.print_ones_distribution(
                    folder_name,
                    sf_name,
                    run + 1,
                    self.iteration + 1,
                    self.fitness_function
                )
                if not ff_name.startswith("FConst"):
                    self.population.print_genotypes_distribution(
                        folder_name,
                        sf_name,
                        run + 1,
                        self.iteration + 1,
                        self.fitness_function,
                    )
                if not ff_name.startswith("FConst"):
                    self.population.print_phenotypes_distribution(
                        folder_name,
                        sf_name,
                        run + 1,
                        self.iteration + 1,
                        self.fitness_function,
                    )

            best_chromosomes = self.population.get_best_chromosomes()
            f = avg_fitness_list[self.iteration]
            self.population = self.selection_function.select(self.population)
            keys_after_selection = self.population.get_keys_list()
            selected_chromosome_keys = set(keys_after_selection)
            f_parents_pool = self.population.get_mean_fitness()
            self.population.crossover(self.fitness_function, self.p_c)
            self.population.mutate(self.fitness_function, self.p_m)
            f_std = self.population.get_fitness_std()
            std_fitness_list.append(f_std)
            fs = self.population.get_mean_fitness()
            avg_fitness_list.append(fs)
            optimal_count.append(self.population.get_chromosomes_copies_count(self.optimal_chromosome))
            self.selection_diff_stats.s_list.append(f_parents_pool - f)
            num_of_best = self.population.get_chromosomes_copies_count(best_chromosomes)
            self.reproduction_stats.rr_list.append(
                len(selected_chromosome_keys) / N
            )
            self.reproduction_stats.best_rr_list.append(
                num_of_best / len(self.population.chromosomes)
            )
            self.pressure_stats.intensities.append(
                PressureStats.calculate_intensity(
                    f_parents_pool, f, std_fitness_list[self.iteration]
                )
            )
            self.pressure_stats.f_best.append(self.population.get_max_fitness())
            self.pressure_stats.num_of_best.append(num_of_best)
            self.iteration += 1
            self.pressure_stats.grs.append(
                PressureStats.calculate_growth_rate(
                    self.pressure_stats.num_of_best[self.iteration],
                    self.pressure_stats.num_of_best[self.iteration - 1],
                    self.pressure_stats.f_best[self.iteration],
                    self.pressure_stats.f_best[self.iteration - 1],
                )
            )
            if num_of_best >= N / 2 and self.pressure_stats.grl is None:
                self.pressure_stats.grli = self.iteration
                self.pressure_stats.grl = self.pressure_stats.grs[-1]
            convergent = self.population.estimate_convergence(self.p_m)
            self.population.override_chromosome_keys()

        if convergent:
            self.pressure_stats.NI = self.iteration

        if run < ITERATIONS_TO_REPORT:
            sf_name = repr(self.selection_function)
            self.population.print_ones_distribution(
                folder_name,
                sf_name,
                run + 1,
                self.iteration + 1,
                self.fitness_function,
                is_last_iteration=True
            )
            if not ff_name.startswith("FConst"):
                self.population.print_genotypes_distribution(
                    folder_name,
                    sf_name,
                    run + 1,
                    self.iteration + 1,
                    self.fitness_function,
                    is_last_iteration=True
                )
            if not ff_name.startswith("FConst"):
                self.population.print_phenotypes_distribution(
                    folder_name,
                    sf_name,
                    run + 1,
                    self.iteration + 1,
                    self.fitness_function,
                    is_last_iteration=True
                )

        self.pressure_stats.takeover_time = self.iteration
        self.pressure_stats.f_found = self.population.get_max_fitness()
        self.pressure_stats.f_avg = self.population.get_mean_fitness()
        self.pressure_stats.calculate()
        self.reproduction_stats.calculate()
        self.selection_diff_stats.calculate()
        is_successful = self.check_success() if convergent else False

        ns = NoiseStats() if ff_name.startswith("FConst") else None
        if is_successful and ns:
            ns.NI = self.iteration
            ns.conv_to = self.population.chromosomes[0].code[0]

        return Run(
            avg_fitness_list,
            std_fitness_list,
            optimal_count,
            self.pressure_stats,
            self.reproduction_stats,
            self.selection_diff_stats,
            ns,
            is_successful,
        )

    def check_success(self):
        ff_name = repr(self.fitness_function)
        if ff_name.startswith("FHD"):
            optimal_chromosomes = self.population.get_chromosomes_copies_count(self.optimal_chromosome)
            if self.p_m:
                return optimal_chromosomes >= .9 * N
            else:
                return optimal_chromosomes == N
        elif ff_name.startswith("FConst"):
            return True
        else:
            success_chromosomes = [
                self.fitness_function.check_chromosome_success(p)
                for p in self.population.chromosomes
            ]
            return any(success_chromosomes)
