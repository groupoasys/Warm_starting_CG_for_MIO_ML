import os
import pandas as pd


def get_comparative_results_UC(csv_files,
                               data_folder,
                               folder_particular_dataset,
                               grid_neighbours,
                               threshold_equality,
                               total_number_of_constraints,
                               comparative_table_csv_name='UC_comparative_results.csv'):
    os.chdir(data_folder)
    os.chdir(folder_particular_dataset)
    benchmark_file = csv_files['benchmark']
    CG_file = csv_files['CG']
    benchmark_results = pd.read_csv(benchmark_file, sep=';', index_col=0)
    CG_results = pd.read_csv(CG_file, sep=';', index_col=0)
    total_number_of_instances = benchmark_results.shape[0]
    columns_comparative_table = ['# inf', '% inf', '# opt', '% opt', '# constraints', 'min const', 'max const',
                                 'CG counter', 'min CG counter', 'max CG counter', '% CG iter = 0', 'time method',
                                 'time method solve time', 'time UC', '% prop. time orig. UC', '% prop. online time UC']
    comparative_table = pd.DataFrame(columns=columns_comparative_table)
    objective_values_benchmark = benchmark_results['obj. value']
    user_time_MILP_BN = benchmark_results['user time (s)']
    comparative_table = update_CG_results_UC(CG_results=CG_results,
                                             comparative_table=comparative_table,
                                             objective_values_benchmark=objective_values_benchmark,
                                             threshold_equality=threshold_equality,
                                             total_number_of_instances=total_number_of_instances,
                                             user_time_MILP_BN=user_time_MILP_BN)
    for number_of_neighbors in grid_neighbours:
        DD_file = csv_files['DD'] + str(number_of_neighbors) + '.csv'
        knn_file = csv_files['knn_DD'] + str(number_of_neighbors) + '.csv'
        DD_results = pd.read_csv(DD_file, sep=';', index_col=0)
        knn_DD_results = pd.read_csv(knn_file, sep=';', index_col=0)

        comparative_table = update_DD_results_UC(DD_results=DD_results,
                                                 knn_DD_results=knn_DD_results,
                                                 comparative_table=comparative_table,
                                                 objective_values_benchmark=objective_values_benchmark,
                                                 threshold_equality=threshold_equality,
                                                 total_number_of_instances=total_number_of_instances,
                                                 user_time_MILP_BN=user_time_MILP_BN,
                                                 DD_method_string='DD',
                                                 number_of_neighbors=number_of_neighbors,
                                                 total_number_of_constraints=total_number_of_constraints)
        aa = 0
        comparative_table = update_DD_CG_results_UC(DD_results=DD_results,
                                                    comparative_table=comparative_table,
                                                    knn_DD_results=knn_DD_results,
                                                    number_of_neighbors=number_of_neighbors,
                                                    objective_values_benchmark=objective_values_benchmark,
                                                    threshold_equality=threshold_equality,
                                                    total_number_of_constraints=total_number_of_constraints,
                                                    total_number_of_instances=total_number_of_instances,
                                                    user_time_MILP_BN=user_time_MILP_BN,
                                                    DD_method_string='DD')

        aa = 0
        DD_file = csv_files['DD*'] + str(number_of_neighbors) + '.csv'
        knn_file = csv_files['knn_DD*'] + str(number_of_neighbors) + '.csv'
        DD_results = pd.read_csv(DD_file, sep=';', index_col=0)
        knn_DD_results = pd.read_csv(knn_file, sep=';', index_col=0)

        comparative_table = update_DD_results_UC(DD_results=DD_results,
                                                 knn_DD_results=knn_DD_results,
                                                 comparative_table=comparative_table,
                                                 objective_values_benchmark=objective_values_benchmark,
                                                 threshold_equality=threshold_equality,
                                                 total_number_of_instances=total_number_of_instances,
                                                 user_time_MILP_BN=user_time_MILP_BN,
                                                 DD_method_string='DD*',
                                                 number_of_neighbors=number_of_neighbors,
                                                 total_number_of_constraints=total_number_of_constraints)
        comparative_table = update_DD_CG_results_UC(DD_results=DD_results,
                                                    comparative_table=comparative_table,
                                                    knn_DD_results=knn_DD_results,
                                                    number_of_neighbors=number_of_neighbors,
                                                    objective_values_benchmark=objective_values_benchmark,
                                                    threshold_equality=threshold_equality,
                                                    total_number_of_constraints=total_number_of_constraints,
                                                    total_number_of_instances=total_number_of_instances,
                                                    user_time_MILP_BN=user_time_MILP_BN,
                                                    DD_method_string='DD*')
        aa = 0
    comparative_table.to_csv(comparative_table_csv_name, sep=';')
    return 0


def update_DD_CG_results_UC(DD_results,
                            comparative_table,
                            knn_DD_results,
                            number_of_neighbors,
                            objective_values_benchmark,
                            threshold_equality,
                            total_number_of_constraints,
                            total_number_of_instances,
                            user_time_MILP_BN,
                            DD_method_string):
    aa = 0
    objective_values_DD = DD_results['obj value last UC']
    number_of_constraints_DD = DD_results['# constraints last UC']
    user_time_MILP_DD = DD_results['user time last UC']
    knn_total_time = knn_DD_results['total knn time']
    CG_time = DD_results['CG time']
    CG_time_solve_model = DD_results['CG time solve model']
    CG_counter = DD_results['CG counter']

    abs_differences_objective_values_DD_vs_BN = abs(objective_values_benchmark - objective_values_DD)
    relative_differences_objective_values_DD_vs_BN = abs_differences_objective_values_DD_vs_BN / objective_values_benchmark
    optimal_instances_DD = relative_differences_objective_values_DD_vs_BN.loc[
        relative_differences_objective_values_DD_vs_BN <= threshold_equality].index
    # optimal_instances_DD = abs_differences_objective_values_DD_vs_BN.loc[
    #     abs_differences_objective_values_DD_vs_BN <= threshold_equality].index
    number_of_optimal_instances_DD = len(optimal_instances_DD)
    percentage_optimal_instances_DD = 100 * (number_of_optimal_instances_DD / total_number_of_instances)
    number_of_infeasible_instances_DD = total_number_of_instances - number_of_optimal_instances_DD
    percentage_infeasible_instances_DD = 100 * (number_of_infeasible_instances_DD / total_number_of_instances)
    average_number_of_constraints = number_of_constraints_DD.mean()
    minimum_number_of_constraints = number_of_constraints_DD.min()
    maximum_number_of_constraints = number_of_constraints_DD.max()
    time_method_DD = (CG_time + (knn_total_time / total_number_of_constraints)).mean()
    time_method_solve_time_DD = (CG_time_solve_model + (knn_total_time / total_number_of_constraints)).mean()
    average_user_time_MILP_DD = user_time_MILP_DD[optimal_instances_DD].mean()
    average_proportion_user_time_MILP_DD_vs_BN = 100 * (user_time_MILP_DD / user_time_MILP_BN)[
        optimal_instances_DD].mean()
    proportion_time_online = 100 * ((
                                            knn_total_time / total_number_of_constraints) + CG_time_solve_model + user_time_MILP_DD).sum() / user_time_MILP_BN.sum()
    average_CG_counter = CG_counter[optimal_instances_DD].mean()
    min_CG_counter = CG_counter[optimal_instances_DD].min()
    max_CG_counter = CG_counter[optimal_instances_DD].max()
    instances_zero_CG_iterations = CG_counter[CG_counter == 0]
    percentage_instances_zero_CG_iterations = 100 * (len(instances_zero_CG_iterations) / len(CG_counter))

    comparison_DD = [number_of_infeasible_instances_DD, percentage_infeasible_instances_DD,
                     number_of_optimal_instances_DD, percentage_optimal_instances_DD, average_number_of_constraints,
                     minimum_number_of_constraints, maximum_number_of_constraints, average_CG_counter, min_CG_counter,
                     max_CG_counter, percentage_instances_zero_CG_iterations, time_method_DD, time_method_solve_time_DD,
                     average_user_time_MILP_DD, average_proportion_user_time_MILP_DD_vs_BN, proportion_time_online]
    comparative_table.loc[DD_method_string + str(number_of_neighbors) + '+CG', :] = comparison_DD
    return comparative_table


def update_DD_results_UC(DD_results,
                         knn_DD_results,
                         comparative_table,
                         objective_values_benchmark,
                         threshold_equality,
                         total_number_of_instances,
                         user_time_MILP_BN,
                         DD_method_string,
                         number_of_neighbors,
                         total_number_of_constraints):
    objective_values_DD = DD_results['obj value last UC']
    counter_DD = DD_results['CG counter']
    number_of_constraints_DD = DD_results['# constraints last UC']
    user_time_MILP_DD = DD_results['user time last UC']
    knn_total_time = knn_DD_results['total knn time']

    infeasible_instances_DD = counter_DD[counter_DD != 0].index
    feasible_instances_DD = counter_DD[counter_DD == 0].index
    number_of_infeasible_instances_DD = len(infeasible_instances_DD)
    percentage_infeasible_instances_DD = 100 * (number_of_infeasible_instances_DD / total_number_of_instances)
    abs_differences_objective_values_DD_vs_BN = abs(objective_values_benchmark - objective_values_DD)
    relative_differences_objective_values_DD_vs_BN = abs_differences_objective_values_DD_vs_BN / objective_values_benchmark
    abs_differences_feasible_instances = abs_differences_objective_values_DD_vs_BN.loc[feasible_instances_DD]
    relative_differences_feasible_instances = relative_differences_objective_values_DD_vs_BN.loc[feasible_instances_DD]
    # optimal_instances_DD = abs_differences_feasible_instances.loc[
    #     abs_differences_feasible_instances <= threshold_equality].index
    optimal_instances_DD = relative_differences_feasible_instances.loc[
        relative_differences_feasible_instances <= threshold_equality].index
    number_of_optimal_instances_DD = len(optimal_instances_DD)
    percentage_optimal_instances_DD = 100 * (number_of_optimal_instances_DD / total_number_of_instances)
    average_number_of_constraints = number_of_constraints_DD[optimal_instances_DD].mean()
    minimum_number_of_constraints = number_of_constraints_DD[optimal_instances_DD].min()
    maximum_number_of_constraints = number_of_constraints_DD[optimal_instances_DD].max()
    time_method_DD = None
    time_method_solve_time_DD = knn_total_time[optimal_instances_DD].mean() / total_number_of_constraints
    average_user_time_MILP_DD = user_time_MILP_DD[optimal_instances_DD].mean()
    average_proportion_user_time_MILP_DD_vs_BN = 100 * (user_time_MILP_DD / user_time_MILP_BN)[
        optimal_instances_DD].mean()
    proportion_time_online = 100 * (
            (knn_total_time[optimal_instances_DD] / total_number_of_constraints) + user_time_MILP_DD[
        optimal_instances_DD]).sum() / user_time_MILP_BN[optimal_instances_DD].sum()
    average_CG_counter = counter_DD[optimal_instances_DD].mean()
    min_CG_counter = counter_DD[optimal_instances_DD].min()
    max_CG_counter = counter_DD[optimal_instances_DD].max()
    instances_zero_CG_iterations = counter_DD[optimal_instances_DD][counter_DD[optimal_instances_DD] == 0]
    percentage_instances_zero_CG_iterations = 100 * (len(instances_zero_CG_iterations) / len(counter_DD))

    comparison_DD = [number_of_infeasible_instances_DD, percentage_infeasible_instances_DD,
                     number_of_optimal_instances_DD, percentage_optimal_instances_DD, average_number_of_constraints,
                     minimum_number_of_constraints, maximum_number_of_constraints, average_CG_counter, min_CG_counter,
                     max_CG_counter, percentage_instances_zero_CG_iterations, time_method_DD, time_method_solve_time_DD,
                     average_user_time_MILP_DD, average_proportion_user_time_MILP_DD_vs_BN, proportion_time_online]
    comparative_table.loc[DD_method_string + str(number_of_neighbors), :] = comparison_DD

    return comparative_table


def update_CG_results_UC(CG_results,
                         comparative_table,
                         objective_values_benchmark,
                         threshold_equality,
                         total_number_of_instances,
                         user_time_MILP_BN):
    objective_values_CG = CG_results['obj value last UC']
    CG_time_solve_model = CG_results['CG time solve model']  # Includes the time of the last UC
    CG_time = CG_results['CG time']
    user_time_MILP_CG = CG_results['user time last UC']
    number_of_constraints_CG = CG_results['# constraints last UC']
    CG_counter = CG_results['CG counter']

    absolute_difference_optimal_values_BN_CG = abs(objective_values_benchmark - objective_values_CG)
    relative_difference_optimal_values_BN_CG = absolute_difference_optimal_values_BN_CG / objective_values_benchmark
    optimal_instances_CG = absolute_difference_optimal_values_BN_CG.loc[
        relative_difference_optimal_values_BN_CG <= threshold_equality].index
    number_of_optimal_instances_CG = len(optimal_instances_CG)
    percentage_optimal_instances_CG = 100 * (number_of_optimal_instances_CG / total_number_of_instances)
    number_of_infeasible_instances_CG = total_number_of_instances - number_of_optimal_instances_CG
    percentage_infeasible_instances_CG = 100 * (number_of_infeasible_instances_CG / total_number_of_instances)
    average_number_of_constraints_CG = number_of_constraints_CG.mean()
    minimum_number_of_constraints_CG = number_of_constraints_CG.min()
    maximum_number_of_constraints_CG = number_of_constraints_CG.max()
    average_CG_time_solve_model = CG_time_solve_model.mean()
    average_CG_time = CG_time.mean()
    average_user_time_MILP_CG = user_time_MILP_CG.mean()
    average_proportion_user_time_MILP_CG_vs_BN = (100 * (user_time_MILP_CG / user_time_MILP_BN)).mean()
    proportion_time_online = 100 * CG_time_solve_model.sum() / user_time_MILP_BN.sum()
    average_CG_counter = CG_counter.mean()
    min_CG_counter = CG_counter.min()
    max_CG_counter = CG_counter.max()
    instances_zero_CG_iterations = CG_counter[CG_counter == 0]
    percentage_instances_zero_CG_iterations = 100 * (len(instances_zero_CG_iterations) / len(CG_counter))

    comparison_CG = [number_of_infeasible_instances_CG, percentage_infeasible_instances_CG,
                     number_of_optimal_instances_CG, percentage_optimal_instances_CG, average_number_of_constraints_CG,
                     minimum_number_of_constraints_CG, maximum_number_of_constraints_CG, average_CG_counter,
                     min_CG_counter, max_CG_counter, percentage_instances_zero_CG_iterations, average_CG_time,
                     average_CG_time_solve_model, average_user_time_MILP_CG, average_proportion_user_time_MILP_CG_vs_BN,
                     proportion_time_online]
    comparative_table.loc['CG', :] = comparison_CG

    return comparative_table
