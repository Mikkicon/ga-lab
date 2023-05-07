import os

import matplotlib.pyplot as plt

from constants import N, ENCODING


def save_line_plot(fitness_func_name, selection_name, data, file_name, y_label, iteration):
    if fitness_func_name.startswith("FHD") or fitness_func_name.startswith("FConst"):
        dir_path = f"BinaryChain/{N}/{fitness_func_name}/{selection_name}/{str(iteration)}"
    else:
        dir_path = f"RealArgument-{ENCODING}/{N}/{fitness_func_name}/{selection_name}/{str(iteration)}"
    # dir_path = f"Function/{N}/{ENCODING}/{fitness_func_name}/{selection_name}/{str(iteration)}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    x = list(range(1, len(data) + 1))
    plt.xticks(x, rotation='vertical')
    plt.plot(x, data, label=selection_name)
    plt.ylabel(y_label)
    plt.xlabel("generation")
    plt.legend()
    plt.savefig(f"{dir_path}/{file_name}.png")
    plt.close()


def save_lines_plot(
    fitness_func_name, selection_name, data_arr, label_arr, file_name, y_label, iteration
):
    if fitness_func_name.startswith("FHD") or fitness_func_name.startswith("FConst"):
        dir_path = f"BinaryChain/{N}/{fitness_func_name}/{selection_name}/{str(iteration)}"
    else:
        dir_path = f"RealArgument-{ENCODING}/{N}/{fitness_func_name}/{selection_name}/{str(iteration)}"
    # dir_path = f"Function/{N}/{ENCODING}/{fitness_func_name}/{selection_name}/{str(iteration)}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for i in range(0, len(data_arr)):
        data = data_arr[i]
        label = label_arr[i]
        x = list(range(1, len(data) + 1))
        plt.xticks(x, rotation='vertical')
        plt.plot(x, data, label=label)

    plt.ylabel(y_label)
    plt.xlabel("generation")
    plt.legend()
    plt.savefig(f"{dir_path}/{file_name}.png")
    plt.close()


def save_run_plots(ff_name, sf_name, run, iteration):
    save_line_plot(
        ff_name,
        sf_name,
        run.avg_fitness_list,
        "f_avg" + str(iteration + 1),
        "f avg",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.pressure_stats.f_best,
        "f_best" + str(iteration + 1),
        "f best",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.std_fitness_list,
        "f_std" + str(iteration + 1),
        "f std",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.optimal_count,
        "optimal_count" + str(iteration + 1),
        "Optimal count",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.pressure_stats.intensities,
        "intensity" + str(iteration + 1),
        "Intensity",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.selection_diff_stats.s_list,
        "selection_diff" + str(iteration + 1),
        "Selection difference",
        iteration + 1,
    )
    save_lines_plot(
        ff_name,
        sf_name,
        [run.pressure_stats.intensities, run.selection_diff_stats.s_list],
        ["Intensity", "EvoAlgorithm diff"],
        "intensity_and_sel_diff" + str(iteration + 1),
        "Intensity + EvoAlgorithm diff",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.pressure_stats.grs,
        "gr" + str(iteration + 1),
        "Growth rate",
        iteration + 1,
    )
    save_lines_plot(
        ff_name,
        sf_name,
        [
            run.reproduction_stats.rr_list,
            [1 - rr for rr in run.reproduction_stats.rr_list],
        ],
        ["Reproduction rate", "Loss of diversity"],
        "repro_rate_and_loss_of_diversity" + str(iteration + 1),
        "Reproduction rate + Loss of diversity",
        iteration + 1,
    )
    save_line_plot(
        ff_name,
        sf_name,
        run.reproduction_stats.best_rr_list,
        "best_rr" + str(iteration + 1),
        "Best chromosome rate",
        iteration + 1,
    )
