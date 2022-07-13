import pandas as pd

import time

import My_project.General_MILP as GMILP
import My_project.create_database_utils as cdu
import My_project.general_utils as gu
import My_project.solve_utils as su


def run_main_general_MILP(particular_folder_results,
                          division,
                          start_time_period_to_solve,
                          end_time_period_to_solve,
                          data_folder='../Data/',
                          database_results_folder='Results'):
    (coefficient_matrix,
     costs,
     independent_term_dataframe,
     lower_bound_continuous_variables,
     upper_bound_continuous_variables) = cdu.extract_data_from_csv(data_folder=data_folder,
                                                                   particular_folder_results=particular_folder_results)

    number_of_constraints = coefficient_matrix.shape[0]
    number_of_continuous_variables = coefficient_matrix.shape[1]
    range_constraints = range(1, number_of_constraints + 1)
    range_individuals_to_solve = range(start_time_period_to_solve, end_time_period_to_solve)

    columns_termination_condition = cdu.create_columns_termination_condition()
    termination_condition_dataframe = pd.DataFrame(index=range_individuals_to_solve,
                                                   columns=columns_termination_condition)

    columns_status_constraints = cdu.create_columns_status_constraints_general_MILP(
        number_of_constraints=number_of_constraints)
    activation_constraint_status = pd.DataFrame(index=range_individuals_to_solve,
                                                columns=columns_status_constraints)

    columns_elapsed_time = cdu.create_columns_elapsed_time()
    elapsed_time_dataframe = pd.DataFrame(index=range_individuals_to_solve,
                                          columns=columns_elapsed_time)

    columns_computational_complexity = cdu.create_columns_computational_complexity()
    computational_complexity_dataframe = pd.DataFrame(index=range_individuals_to_solve,
                                                      columns=columns_computational_complexity)

    columns_objective_value = cdu.create_columns_objective_value_general_MILP()
    objective_value_dataframe = pd.DataFrame(index=range_individuals_to_solve,
                                             columns=columns_objective_value)

    columns_gap = cdu.create_columns_gap()
    gap_dataframe = pd.DataFrame(index=range_individuals_to_solve,
                                 columns=columns_gap)

    columns_nonzeros = cdu.create_columns_nonzeros()
    nonzeros_dataframe = pd.DataFrame(index=range_individuals_to_solve,
                                      columns=columns_nonzeros)
    columns_subproblems = cdu.create_columns_subproblems()
    subproblems_dataframe = pd.DataFrame(index=range_individuals_to_solve,
                                         columns=columns_subproblems)
    for individual in range_individuals_to_solve:
        print(individual)
        independent_term = independent_term_dataframe.iloc[individual, :]
        model = GMILP.create_optimization_model(number_of_continuous_variables=number_of_continuous_variables,
                                                costs=costs,
                                                lower_bound_continuous_variables=lower_bound_continuous_variables,
                                                upper_bound_continuous_variables=upper_bound_continuous_variables,
                                                coefficient_matrix=coefficient_matrix,
                                                independent_term=independent_term,
                                                number_of_constraints=number_of_constraints)

        (model,
         solution,
         elapsed_time_per_individual) = su.solve_model(model=model)

        termination_condition_dataframe = cdu.update_termination_condition_dataframe(
            individual_time_period=individual,
            termination_condition_dataframe=termination_condition_dataframe,
            solution=solution)
        activation_constraint_status = cdu.update_activation_status_constraints_general_MILP(
            activation_constraint_status=activation_constraint_status,
            individual_time_period=individual,
            model=model,
            range_constraints=range_constraints)
        elapsed_time_dataframe = cdu.update_elapsed_time_dataframe(elapsed_time_dataframe=elapsed_time_dataframe,
                                                                   elapsed_time=elapsed_time_per_individual,
                                                                   user_time=solution.solver(0).user_time,
                                                                   time=solution.solver(0).time,
                                                                   individual_time_period=individual)
        computational_complexity_dataframe = cdu.update_computational_complexity_dataframe(solution=solution,
                                                                                           individual_time_period=individual,
                                                                                           computational_complexity_dataframe=computational_complexity_dataframe)
        objective_value_dataframe = cdu.update_objective_value_dataframe_CVRP(individual_time_period=individual,
                                                                              model=model,
                                                                              objective_value_dataframe=objective_value_dataframe)
        gap_dataframe = cdu.update_gap_dataframe(gap_dataframe=gap_dataframe,
                                                 model=model,
                                                 solution=solution,
                                                 individual_time_period=individual)

        nonzeros_dataframe = cdu.update_performance_number_of_nonzeros(individual_time_period=individual,
                                                                       nonzeros_dataframe=nonzeros_dataframe,
                                                                       solution=solution)
        subproblems_dataframe = cdu.update_performance_number_subproblems(individual_time_period=individual,
                                                                          subproblems_dataframe=subproblems_dataframe,
                                                                          solution=solution)

    coefficients_and_labels_database = pd.concat(
        [independent_term_dataframe.iloc[range_individuals_to_solve, :],
         activation_constraint_status,
         elapsed_time_dataframe,
         computational_complexity_dataframe,
         objective_value_dataframe,
         gap_dataframe,
         termination_condition_dataframe,
         nonzeros_dataframe,
         subproblems_dataframe], axis=1)

    gu.create_directory_if_it_does_not_exists(path=database_results_folder)
    gu.create_directory_if_it_does_not_exists(path=database_results_folder + '/' + particular_folder_results)

    coefficients_and_labels_database.to_csv(
        database_results_folder + '//' + particular_folder_results + '//' + 'coefficients_and_labels_' + str(
            division) + '.csv', sep=';')
    return 0
