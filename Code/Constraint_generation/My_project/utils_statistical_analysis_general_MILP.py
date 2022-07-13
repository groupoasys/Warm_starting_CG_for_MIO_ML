import matplotlib.pyplot as plt
import os
import pandas as pd
from matplotlib.patches import Patch


def get_statistical_analysis_general_MILP(csv_files,
                                          data_folder,
                                          folder_particular_dataset,
                                          grid_neighbours,
                                          comparative_table_constraints_csv_name,
                                          comparative_table_iterations_csv_name,
                                          threshold_equality,
                                          total_number_of_constraints,
                                          comparative_table_online_time_csv_name):
    os.chdir(data_folder)
    os.chdir(folder_particular_dataset)
    CG_file = csv_files['CG']
    benchmark_file = csv_files['benchmark']
    benchmark_results = pd.read_csv(benchmark_file, sep=';', index_col=0)
    user_time_MILP_BN = benchmark_results['user time (s)']
    objective_values_benchmark = benchmark_results['obj. value']

    CG_results = pd.read_csv(CG_file, sep=';', index_col=0)
    columns_comparison_table = CG_results.index
    comparative_table_constraints = pd.DataFrame(columns=columns_comparison_table)
    comparative_table_iterations = pd.DataFrame(columns=columns_comparison_table)
    comparative_table_online_time = pd.DataFrame(columns=columns_comparison_table)

    (comparative_table_constraints,
     comparative_table_iterations,
     comparative_table_online_time) = update_CG_results(CG_results=CG_results,
                                                        comparative_table_constraints=comparative_table_constraints,
                                                        comparative_table_iterations=comparative_table_iterations,
                                                        comparative_table_online_time=comparative_table_online_time,
                                                        user_time_MILP_BN=user_time_MILP_BN)

    for number_of_neighbors in grid_neighbours:
        DD_file = csv_files['DD'] + str(number_of_neighbors) + '.csv'
        knn_file = csv_files['knn_DD'] + str(number_of_neighbors) + '.csv'
        DD_results = pd.read_csv(DD_file, sep=';', index_col=0)
        knn_DD_results = pd.read_csv(knn_file, sep=';', index_col=0)

        (comparative_table_constraints,
         comparative_table_iterations,
         comparative_table_online_time) = update_DD_results(DD_results=DD_results,
                                                            comparative_table_constraints=comparative_table_constraints,
                                                            DD_method_string='DD',
                                                            number_of_neighbors=number_of_neighbors,
                                                            comparative_table_iterations=comparative_table_iterations,
                                                            comparative_table_online_time=comparative_table_online_time,
                                                            knn_DD_results=knn_DD_results,
                                                            objective_values_benchmark=objective_values_benchmark,
                                                            threshold_equality=threshold_equality,
                                                            total_number_of_constraints=total_number_of_constraints,
                                                            user_time_MILP_BN=user_time_MILP_BN)
        aa = 0
        (comparative_table_constraints,
         comparative_table_iterations,
         comparative_table_online_time) = update_DD_CG_results(DD_results=DD_results,
                                                               comparative_table_constraints=comparative_table_constraints,
                                                               number_of_neighbors=number_of_neighbors,
                                                               DD_method_string='DD',
                                                               comparative_table_iterations=comparative_table_iterations,
                                                               comparative_table_online_time=comparative_table_online_time,
                                                               knn_DD_results=knn_DD_results,
                                                               total_number_of_constraints=total_number_of_constraints,
                                                               user_time_MILP_BN=user_time_MILP_BN)

        aa = 0
        DD_file = csv_files['DD*'] + str(number_of_neighbors) + '.csv'
        knn_file = csv_files['knn_DD*'] + str(number_of_neighbors) + '.csv'
        DD_results = pd.read_csv(DD_file, sep=';', index_col=0)

        (comparative_table_constraints,
         comparative_table_iterations,
         comparative_table_online_time) = update_DD_results(DD_results=DD_results,
                                                            comparative_table_constraints=comparative_table_constraints,
                                                            DD_method_string='DD*',
                                                            number_of_neighbors=number_of_neighbors,
                                                            comparative_table_iterations=comparative_table_iterations,
                                                            comparative_table_online_time=comparative_table_online_time,
                                                            knn_DD_results=knn_DD_results,
                                                            objective_values_benchmark=objective_values_benchmark,
                                                            threshold_equality=threshold_equality,
                                                            total_number_of_constraints=total_number_of_constraints,
                                                            user_time_MILP_BN=user_time_MILP_BN)
        (comparative_table_constraints,
         comparative_table_iterations,
         comparative_table_online_time) = update_DD_CG_results(DD_results=DD_results,
                                                               comparative_table_constraints=comparative_table_constraints,
                                                               number_of_neighbors=number_of_neighbors,
                                                               DD_method_string='DD*',
                                                               comparative_table_iterations=comparative_table_iterations,
                                                               comparative_table_online_time=comparative_table_online_time,
                                                               knn_DD_results=knn_DD_results,
                                                               total_number_of_constraints=total_number_of_constraints,
                                                               user_time_MILP_BN=user_time_MILP_BN)
        aa = 0
    comparative_table_constraints.to_csv(comparative_table_constraints_csv_name, sep=';')
    comparative_table_iterations.to_csv(comparative_table_iterations_csv_name, sep=';')
    comparative_table_online_time.to_csv(comparative_table_online_time_csv_name, sep=';')

    plot_boxplots_number_of_constraints(comparative_table_constraints=comparative_table_constraints,
                                        grid_neighbours=grid_neighbours)
    plot_boxplots_number_of_iterations(comparative_table_iterations=comparative_table_iterations,
                                       grid_neighbours=[5, 50, 100, 999],
                                       original_grid_of_neighbours=grid_neighbours,
                                       name_figure='MILP_boxplot_number_of_iterations_1',
                                       y_limits={'axis_1': [119, 135],
                                                 'axis_2': [0, 10]})
    plot_boxplots_number_of_iterations(comparative_table_iterations=comparative_table_iterations,
                                       grid_neighbours=grid_neighbours,
                                       original_grid_of_neighbours=grid_neighbours)

    plot_boxplots_online_time(comparative_table_online_time=comparative_table_online_time,
                              grid_neighbours=grid_neighbours)

    return 0


def plot_boxplots_number_of_constraints(comparative_table_constraints,
                                        grid_neighbours):
    widths = 200
    bb = 500
    markersize_outliers = 3
    boxplot = plt.boxplot(comparative_table_constraints.iloc[[0], :].transpose(), positions=[0], widths=widths,
                          medianprops={"linewidth": 1.5, "solid_capstyle": "butt"},
                          flierprops={'marker': 'D', 'markersize': markersize_outliers})
    for median in boxplot['medians']:
        median.set_color('black')
    # plt.xticks(ticks=[1], labels=['CG'])
    ticks = [0]
    ticks_labels = ['CG']
    for index in range(1, (len(grid_neighbours) + 1)):
        boxplot = plt.boxplot(comparative_table_constraints.iloc[[4 * index - 2, 4 * index], :].transpose(),
                              positions=[(bb * index) - (0.5 * widths), (bb * index) + (0.5 * widths)],
                              patch_artist=True,
                              widths=widths,
                              medianprops={"linewidth": 1.5},
                              flierprops={'marker': 'D', 'markersize': markersize_outliers})
        hatches = ['OO', '..']
        colors = ['tab:blue', 'tab:red']
        for i in range(len(boxplot['boxes'])):
            boxplot['boxes'][i].set(hatch=hatches[i])
            boxplot['boxes'][i].set(facecolor=colors[i])
        for median in boxplot['medians']:
            median.set_color('black')
        ticks.append(bb * index)
        ticks_labels.append('$k = ' + str(grid_neighbours[index - 1]) + '$')
        plt.axvline(x=(bb * index) - 0.5 * bb, linestyle=':', linewidth=0.5, color='gray')
    plt.xticks(ticks=ticks, labels=ticks_labels, fontsize=8)
    legend_elements = [Patch(facecolor='white', edgecolor='black',
                             label='CG'),
                       Patch(facecolor='tab:blue', edgecolor='black', hatch=hatches[0],
                             label='$\mathcal{B}$-learner + CG'),
                       Patch(facecolor='tab:red', edgecolor='black', hatch=hatches[1],
                             label='$\mathcal{S}$-learner + CG')
                       ]
    plt.legend(handles=legend_elements, loc='lower right', handleheight=2)
    plt.ylabel('Number of constraints')
    plt.xlabel('Method')
    plt.savefig('MILP_boxplot_number_of_constraints.pdf')
    plt.savefig('MILP_boxplot_number_of_constraints.jpeg', dpi=300)
    plt.close()
    return 0


def plot_boxplots_number_of_iterations(comparative_table_iterations,
                                       grid_neighbours,
                                       original_grid_of_neighbours,
                                       name_figure='MILP_boxplot_number_of_iterations',
                                       y_limits={'axis_1': [119, 135],
                                                 'axis_2': [0, 27]}):
    widths = 200
    bb = 500
    markersize_outliers = 3

    f, (ax, ax2) = plt.subplots(2, 1, sharex=True)
    ax.set_ylim(y_limits['axis_1'][0], y_limits['axis_1'][1])
    ax2.set_ylim(y_limits['axis_2'][0], y_limits['axis_2'][1])
    ax.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax.xaxis.tick_top()
    ax.tick_params(labeltop=False,
                   top=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    boxplot = ax.boxplot(comparative_table_iterations.iloc[[0], :].transpose(),
                         positions=[0], widths=widths,
                         medianprops={"linewidth": 1.5, "solid_capstyle": "butt"},
                         flierprops={'marker': 'D', 'markersize': markersize_outliers})
    for median in boxplot['medians']:
        median.set_color('black')
    hatches = ['OO', '..']
    legend_elements = [Patch(facecolor='white', edgecolor='black',
                             label='CG'),
                       Patch(facecolor='tab:blue', edgecolor='black', hatch=hatches[0],
                             label='$\mathcal{B}$-learner + CG'),
                       Patch(facecolor='tab:red', edgecolor='black', hatch=hatches[1],
                             label='$\mathcal{S}$-learner + CG')]
    ax.legend(handles=legend_elements, loc='upper right', handleheight=2)

    ticks = [0]
    ticks_labels = ['CG']
    for index in range(1, (len(original_grid_of_neighbours) + 1)):
        aa = 0
        if original_grid_of_neighbours[index - 1] in grid_neighbours:
            boxplot = ax2.boxplot(comparative_table_iterations.iloc[[4 * index - 2, 4 * index], :].transpose(),
                                  positions=[(bb * index) - (0.5 * widths), (bb * index) + (0.5 * widths)],
                                  patch_artist=True,
                                  widths=widths,
                                  medianprops={"linewidth": 1.5},
                                  flierprops={'marker': 'D', 'markersize': markersize_outliers})
            colors = ['tab:blue', 'tab:red']
            for i in range(len(boxplot['boxes'])):
                boxplot['boxes'][i].set(hatch=hatches[i])
                boxplot['boxes'][i].set(facecolor=colors[i])
            for median in boxplot['medians']:
                median.set_color('black')
            ticks.append(bb * index)
            ticks_labels.append('$k = ' + str(original_grid_of_neighbours[index - 1]) + '$')
            plt.axvline(x=(bb * index) - 0.5 * bb, linestyle=':', linewidth=0.5, color='gray')
            ax.axvline(x=(bb * index) - 0.5 * bb, linestyle=':', linewidth=0.5, color='gray')

    plt.xticks(ticks=ticks, labels=ticks_labels, fontsize=8)

    plt.ylabel('Number of CG iterations')
    ax2.yaxis.set_label_coords(-0.1, 1)
    plt.xlabel('Method')

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
    ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

    plt.savefig(name_figure + '.pdf')
    plt.savefig(name_figure + '.jpeg', dpi=300)
    plt.close()
    return 0


def plot_boxplots_online_time(comparative_table_online_time,
                              grid_neighbours):
    widths = 200
    bb = 500
    markersize_outliers = 3
    boxplot = plt.boxplot(comparative_table_online_time.iloc[[0], :].transpose(), positions=[0], widths=widths,
                          medianprops={"linewidth": 1.5, "solid_capstyle": "butt"},
                          flierprops={'marker': 'D', 'markersize': markersize_outliers})
    for median in boxplot['medians']:
        median.set_color('black')
    # plt.xticks(ticks=[1], labels=['CG'])
    ticks = [0]
    ticks_labels = ['CG']
    for index in range(1, (len(grid_neighbours) + 1)):
        boxplot = plt.boxplot(comparative_table_online_time.iloc[[4 * index - 2, 4 * index], :].transpose(),
                              positions=[(bb * index) - (0.5 * widths), (bb * index) + (0.5 * widths)],
                              patch_artist=True,
                              widths=widths,
                              medianprops={"linewidth": 1.5},
                              flierprops={'marker': 'D', 'markersize': markersize_outliers})
        hatches = ['OO', '..']
        colors = ['tab:blue', 'tab:red']
        for i in range(len(boxplot['boxes'])):
            boxplot['boxes'][i].set(hatch=hatches[i])
            boxplot['boxes'][i].set(facecolor=colors[i])
        for median in boxplot['medians']:
            median.set_color('black')
        ticks.append(bb * index)
        ticks_labels.append('$k = ' + str(grid_neighbours[index - 1]) + '$')
        plt.axvline(x=(bb * index) - 0.5 * bb, linestyle=':', linewidth=0.5, color='gray')
    plt.xticks(ticks=ticks, labels=ticks_labels, fontsize=8)
    legend_elements = [Patch(facecolor='white', edgecolor='black',
                             label='CG'),
                       Patch(facecolor='tab:blue', edgecolor='black', hatch=hatches[0],
                             label='$\mathcal{B}$-learner + CG'),
                       Patch(facecolor='tab:red', edgecolor='black', hatch=hatches[1],
                             label='$\mathcal{S}$-learner + CG')
                       ]
    plt.legend(handles=legend_elements, loc='upper right', handleheight=2)
    plt.ylabel('$\delta_t\,(\%)$')
    plt.xlabel('Method')
    plt.savefig('MILP_boxplot_online_time.pdf')
    plt.savefig('MILP_boxplot_online_time.jpeg', dpi=300)
    plt.close()
    return 0


def plot_boxplots_online_time_2(comparative_table_online_time,
                                grid_neighbours,
                                original_grid_of_neighbours,
                                name_figure='boxplot_online_time',
                                y_limits={'axis_1': [500, 5000],
                                          'axis_2': [0, 2000]}):
    widths = 200
    bb = 500
    markersize_outliers = 3

    f, (ax, ax2) = plt.subplots(2, 1, sharex=True)
    ax.set_ylim(y_limits['axis_1'][0], y_limits['axis_1'][1])
    ax2.set_ylim(y_limits['axis_2'][0], y_limits['axis_2'][1])
    ax.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax.xaxis.tick_top()
    ax.tick_params(labeltop=False,
                   top=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    boxplot = ax.boxplot(comparative_table_online_time.iloc[[0], :].transpose(),
                         positions=[0], widths=widths,
                         medianprops={"linewidth": 1.5, "solid_capstyle": "butt"},
                         flierprops={'marker': 'D', 'markersize': markersize_outliers})
    for median in boxplot['medians']:
        median.set_color('black')
    hatches = ['OO', '..']
    legend_elements = [Patch(facecolor='white', edgecolor='black',
                             label='CG'),
                       Patch(facecolor='tab:blue', edgecolor='black', hatch=hatches[0],
                             label='$\mathcal{B}$-learner + CG'),
                       Patch(facecolor='tab:red', edgecolor='black', hatch=hatches[1],
                             label='$\mathcal{S}$-learner + CG')]
    ax.legend(handles=legend_elements, loc='upper right', handleheight=2)

    ticks = [0]
    ticks_labels = ['CG']
    for index in range(1, (len(original_grid_of_neighbours) + 1)):
        aa = 0
        if original_grid_of_neighbours[index - 1] in grid_neighbours:
            boxplot = ax2.boxplot(comparative_table_online_time.iloc[[4 * index - 2, 4 * index], :].transpose(),
                                  positions=[(bb * index) - (0.5 * widths), (bb * index) + (0.5 * widths)],
                                  patch_artist=True,
                                  widths=widths,
                                  medianprops={"linewidth": 1.5},
                                  flierprops={'marker': 'D', 'markersize': markersize_outliers})
            colors = ['tab:blue', 'tab:red']
            for i in range(len(boxplot['boxes'])):
                boxplot['boxes'][i].set(hatch=hatches[i])
                boxplot['boxes'][i].set(facecolor=colors[i])
            for median in boxplot['medians']:
                median.set_color('black')
            ticks.append(bb * index)
            ticks_labels.append('$k = ' + str(original_grid_of_neighbours[index - 1]) + '$')
            plt.axvline(x=(bb * index) - 0.5 * bb, linestyle=':', linewidth=0.5, color='gray')
            ax.axvline(x=(bb * index) - 0.5 * bb, linestyle=':', linewidth=0.5, color='gray')

    plt.xticks(ticks=ticks, labels=ticks_labels, fontsize=8)

    plt.ylabel('Number of CG iterations')
    ax2.yaxis.set_label_coords(-0.1, 1)
    plt.xlabel('Method')

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
    ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

    plt.savefig(name_figure + '.pdf')
    plt.savefig(name_figure + '.jpeg', dpi=300)
    plt.close()
    return 0


def update_DD_CG_results(DD_results,
                         comparative_table_constraints,
                         number_of_neighbors,
                         DD_method_string,
                         comparative_table_iterations,
                         comparative_table_online_time,
                         knn_DD_results,
                         total_number_of_constraints,
                         user_time_MILP_BN):
    number_of_constraints_DD = DD_results['# constraints last MILP']
    counter_DD = DD_results['CG counter'] + 1
    knn_total_time = knn_DD_results['total knn time']
    CG_time_solve_model = DD_results['CG time solve model']
    user_time_MILP_DD = DD_results['user time last MILP']

    proportion_time_online = 100 * ((
                                            knn_total_time / total_number_of_constraints) + CG_time_solve_model + user_time_MILP_DD) / user_time_MILP_BN

    comparative_table_constraints.loc[DD_method_string + str(number_of_neighbors) + '+CG', :] = number_of_constraints_DD
    comparative_table_iterations.loc[DD_method_string + str(number_of_neighbors) + '+CG', :] = counter_DD
    comparative_table_online_time.loc[DD_method_string + str(number_of_neighbors) + '+CG', :] = proportion_time_online

    return (comparative_table_constraints,
            comparative_table_iterations,
            comparative_table_online_time)


def update_DD_results(DD_results,
                      comparative_table_constraints,
                      DD_method_string,
                      number_of_neighbors,
                      comparative_table_iterations,
                      comparative_table_online_time,
                      knn_DD_results,
                      objective_values_benchmark,
                      threshold_equality,
                      total_number_of_constraints,
                      user_time_MILP_BN):
    number_of_constraints_DD = DD_results['# constraints last MILP']
    counter_DD = DD_results['CG counter'] + 1
    knn_total_time = knn_DD_results['total knn time']
    objective_values_DD = DD_results['obj value last MILP']
    feasible_instances_DD = counter_DD[counter_DD - 1 == 0].index
    user_time_MILP_DD = DD_results['user time last MILP']

    abs_differences_objective_values_DD_vs_BN = abs(objective_values_benchmark - objective_values_DD)
    relative_differences_objective_values_DD_vs_BN = abs_differences_objective_values_DD_vs_BN / objective_values_benchmark
    relative_differences_feasible_instances = relative_differences_objective_values_DD_vs_BN.loc[feasible_instances_DD]
    optimal_instances_DD = relative_differences_feasible_instances.loc[
        relative_differences_feasible_instances <= threshold_equality].index
    proportion_time_online = 100 * (
            (knn_total_time[optimal_instances_DD] / total_number_of_constraints) + user_time_MILP_DD[
        optimal_instances_DD]) / user_time_MILP_BN[optimal_instances_DD]

    comparative_table_constraints.loc[DD_method_string + str(number_of_neighbors), :] = number_of_constraints_DD
    comparative_table_iterations.loc[DD_method_string + str(number_of_neighbors), :] = counter_DD
    comparative_table_online_time.loc[
        DD_method_string + str(number_of_neighbors), optimal_instances_DD] = proportion_time_online

    return (comparative_table_constraints,
            comparative_table_iterations,
            comparative_table_online_time)


def update_CG_results(CG_results,
                      comparative_table_constraints,
                      comparative_table_iterations,
                      comparative_table_online_time,
                      user_time_MILP_BN):
    number_of_constraints_CG = CG_results['# constraints last MILP']
    CG_iterations = CG_results['CG counter'] + 1  # The first iteration should also be taken into account
    CG_time_solve_model = CG_results['CG time solve model']
    proportion_time_online = 100 * CG_time_solve_model / user_time_MILP_BN

    comparative_table_constraints.loc['CG', :] = number_of_constraints_CG.transpose()
    comparative_table_iterations.loc['CG', :] = CG_iterations.transpose()
    comparative_table_online_time.loc['CG', :] = proportion_time_online.transpose()
    aa = 0
    return (comparative_table_constraints,
            comparative_table_iterations,
            comparative_table_online_time)
