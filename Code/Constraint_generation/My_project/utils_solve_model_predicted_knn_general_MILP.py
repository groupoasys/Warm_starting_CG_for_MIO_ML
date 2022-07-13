import pandas as pd
import numpy as np
import time

import My_project.data_utils as du
import My_project.general_utils as gu
import My_project.General_MILP as GMILP
import My_project.solve_utils as su
import My_project.utils_constraint_generation as ucg


def run_solve_model_predicted_knn_general_MILP(beginning_csv_file,
                                               data_folder,
                                               division,
                                               end_string_file,
                                               end_time_period_to_solve,
                                               folder_particular_dataset,
                                               grid_neighbors,
                                               results_folder,
                                               start_time_period_to_solve):
    (coefficient_matrix,
     costs,
     independent_term_dataframe,
     lower_bound_continuous_variables,
     upper_bound_continuous_variables) = du.extract_data_from_csv(data_folder=data_folder,
                                                                  particular_folder_results=folder_particular_dataset)
    number_of_constraints = coefficient_matrix.shape[0]
    number_of_continuous_variables = coefficient_matrix.shape[1]
    columns_status_constraints = gu.create_columns_status_constraints_general_MILP(
        number_of_constraints=number_of_constraints)
    columns_flag_violated_constraints = gu.create_columns_flag_violated_constraints(
        number_of_constraints=number_of_constraints)
    range_time_periods_to_solve = range(start_time_period_to_solve, end_time_period_to_solve)
    for number_of_neighbors in grid_neighbors:
        dataset_file = beginning_csv_file + str(number_of_neighbors) + '.csv'
        coefficients_and_labels = pd.read_csv(data_folder + folder_particular_dataset + '/' + dataset_file, sep=';',
                                              index_col=0)
        updated_coefficients_and_labels = coefficients_and_labels.loc[range_time_periods_to_solve, :].iloc[:,
                                          0:(2 * number_of_constraints)].copy()
        violated_constraints_flag_dataframe = pd.DataFrame(False, index=range_time_periods_to_solve,
                                                           columns=columns_flag_violated_constraints)
        constraint_generation_time = pd.DataFrame(index=range_time_periods_to_solve, columns=['CG time'])
        constraint_generation_time_solve_model = pd.DataFrame(index=range_time_periods_to_solve,
                                                              columns=['CG time solve model'])
        constraints_generation_counter = pd.DataFrame(index=range_time_periods_to_solve, columns=['CG counter'])
        number_of_constraints_final_MILP = pd.DataFrame(index=range_time_periods_to_solve,
                                                        columns=['# constraints last MILP'])
        objective_value_final_MILP = pd.DataFrame(index=range_time_periods_to_solve, columns=['obj value last MILP'])
        user_time_final_MILP = pd.DataFrame(index=range_time_periods_to_solve, columns=['user time last MILP'])
        elapsed_time_final_MILP = pd.DataFrame(index=range_time_periods_to_solve, columns=['elapsed time last MILP'])

        for individual_time_period in range_time_periods_to_solve:
            print(individual_time_period)
            independent_term = independent_term_dataframe.iloc[individual_time_period, :]
            infeasibility_flag = True
            counter = 0
            CG_time = 0
            CG_time_solve_model = 0
            while infeasibility_flag:
                # while infeasibility_flag and counter <= 1:
                t0 = time.time()
                model = GMILP.create_optimization_model(number_of_continuous_variables=number_of_continuous_variables,
                                                        costs=costs,
                                                        lower_bound_continuous_variables=lower_bound_continuous_variables,
                                                        upper_bound_continuous_variables=upper_bound_continuous_variables,
                                                        coefficient_matrix=coefficient_matrix,
                                                        independent_term=independent_term,
                                                        number_of_constraints=number_of_constraints)
                labels_constraints_per_time_period = ucg.get_labels_constraints_per_time_period(
                    coefficients_and_labels=updated_coefficients_and_labels,
                    columns_status_constraints=columns_status_constraints,
                    individual_time_period=individual_time_period)
                non_active_constraints = (np.where(np.array(labels_constraints_per_time_period) != 1)[0] + 1).tolist()

                model = ucg.deactivate_constraints_general_MILP(model=model,
                                                                non_active_constraints=non_active_constraints)

                (model,
                 solution,
                 elapsed_time) = su.solve_model(model=model)

                (identifier_violated_constraints,
                 infeasibility_constraints_values,
                 violated_constraints_flag) = ucg.identify_violated_constraints_general_MILP(model=model,
                                                                                             non_active_constraints=non_active_constraints)
                aa = 0

                (updated_coefficients_and_labels,
                 infeasibility_flag,
                 violated_constraints_flag_dataframe,
                 counter) = ucg.update_database_including_violated_constraints(
                    columns_status_constraints=columns_status_constraints,
                    columns_flag_violated_constraints=columns_flag_violated_constraints,
                    identifier_violated_constraints=identifier_violated_constraints,
                    individual_time_period=individual_time_period,
                    infeasibility_constraints_values=infeasibility_constraints_values,
                    infeasibility_flag=infeasibility_flag,
                    updated_coefficients_and_labels=updated_coefficients_and_labels,
                    violated_constraints_flag=violated_constraints_flag,
                    violated_constraints_flag_dataframe=violated_constraints_flag_dataframe,
                    counter=counter)
                t1 = time.time()
                if counter >= 1 and infeasibility_flag:
                    CG_time += t1 - t0
                    CG_time_solve_model += solution.solver.user_time
                aa = 0
            aa = 0
            (constraint_generation_time,
             constraint_generation_time_solve_model,
             constraints_generation_counter,
             number_of_constraints_final_MILP,
             objective_value_final_MILP,
             user_time_final_MILP,
             elapsed_time_final_MILP) = ucg.get_performance_results(CG_time=CG_time,
                                                                    CG_time_solve_model=CG_time_solve_model,
                                                                    columns_status_constraints=columns_status_constraints,
                                                                    constraint_generation_time=constraint_generation_time,
                                                                    constraints_generation_counter=constraints_generation_counter,
                                                                    counter=counter,
                                                                    # Here we have to write -1 since the first iteration should be always satisfied.
                                                                    elapsed_time=elapsed_time,
                                                                    elapsed_time_final_MILP=elapsed_time_final_MILP,
                                                                    individual_time_period=individual_time_period,
                                                                    model=model,
                                                                    number_of_constraints=number_of_constraints,
                                                                    number_of_constraints_final_MILP=number_of_constraints_final_MILP,
                                                                    objective_value_final_MILP=objective_value_final_MILP,
                                                                    solution=solution,
                                                                    updated_coefficients_and_labels=updated_coefficients_and_labels,
                                                                    user_time_final_MILP=user_time_final_MILP,
                                                                    constraint_generation_time_solve_model=constraint_generation_time_solve_model)
            aa = 0
        performance_results = pd.concat(
            [updated_coefficients_and_labels, violated_constraints_flag_dataframe, constraint_generation_time,
             constraint_generation_time_solve_model, constraints_generation_counter, number_of_constraints_final_MILP,
             objective_value_final_MILP, user_time_final_MILP, elapsed_time_final_MILP], axis=1)
        gu.create_directory_if_it_does_not_exists(path=results_folder)
        gu.create_directory_if_it_does_not_exists(path=results_folder + folder_particular_dataset + '/')
        performance_results.to_csv(
            results_folder + folder_particular_dataset + '/results_solve_model_' + end_string_file + '_knn_' + str(
                number_of_neighbors) + '_' + str(division) + '.csv', sep=';')
    aa = 0
