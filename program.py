import time

from copy import copy

from evoalgorithm import EvoAlgorithm

def main(
    run: int,
    fitness_function,
    initial_population,
    selection_method,
    file_name,
    *args,
):
    ff_name = repr(fitness_function)
    sf_name = repr(selection_method)
    print(f"{file_name} for {sf_name} per {run} run: starting...")
    p_start = time.time()
    p = copy(initial_population)
    optimal = fitness_function.get_optimal(*args)
    folder_name = file_name if file_name is not None else ff_name
    current_run = EvoAlgorithm(p, selection_method, fitness_function, optimal, *args).run(
        run, folder_name
    )

    # if run < ITERATIONS_TO_REPORT:
    #     print(f"{file_name}, {run} run: saving plots...")
    #     save_run_plots(folder_name, sf_name, current_run, run)

    # if run < ITERATIONS_TO_REPORT:
    #     print(f"{file_name}, {run} run: saving reports...")
    #     run_stats = RunsStats() 
    #     run_stats.runs.append(current_run)
    #     run_stats.calculate()
    #     save_to_excel(run_stats, sf_name, file_name, run + 1, selection_method.t)

    p_end = time.time()
    print(f"{file_name} for {sf_name} per {run} run: finished in {str(p_end - p_start)} seconds...")
    return current_run
