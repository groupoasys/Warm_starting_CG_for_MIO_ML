import time
import pandas as pd

import My_project.create_database_utils as cdu
import My_project.data_utils as du
import My_project.general_utils as gu
import My_project.names_excel_file as nef
import My_project.UC_configuration as UCc
import My_project.Unit_Commitment_Multi_Period_Load_Shedding_Quadratic_Cost_PTDF as UCMPLSQCP
import My_project.solver_utils as su


def run_main_UC(dataset_file,
                start_time_period_to_solve,
                end_time_period_to_solve,
                division,
                particular_folder_results,
                indexes_time_periods={},
                database_results_folder='Results'):
    (names_sheets_dataset_file,
     beginning_names_columns_data,
     column_names_generators_info,
     column_names_lines_info,
     column_names_general_info) = nef.get_names_excel_file()

    (data_and_labels,
     generators_info,
     lines_info,
     general_info,
     ptdf_info) = du.extract_problem_info_from_csv(dataset_file=dataset_file,
                                                   names_sheets_dataset_file=names_sheets_dataset_file)

    indexes_time_periods = du.update_indexes_time_periods_when_necessary(data_and_labels=data_and_labels,
                                                                         indexes_time_periods=indexes_time_periods)
    (demand,
     wind,
     costs,
     lower_bound_generators,
     upper_bound_generators,
     bounds_flow,
     number_of_generators,
     number_of_lines,
     number_of_nodes,
     load_shedding_penalization_constant,
     susceptances,
     relationship_lines_nodes,
     column_names_dataframe_lines_info,
     column_names_dataframe_generators_info,
     relationship_generators_nodes,
     number_of_time_periods) = UCc.extract_UC_configuration(data_and_labels=data_and_labels,
                                                            generators_info=generators_info,
                                                            lines_info=lines_info,
                                                            general_info=general_info,
                                                            beginning_names_columns_data=beginning_names_columns_data,
                                                            column_names_generators_info=column_names_generators_info,
                                                            column_names_lines_info=column_names_lines_info,
                                                            column_names_general_info=column_names_general_info,
                                                            indexes_time_periods=indexes_time_periods)
    number_of_time_periods = 1
    range_time_periods_to_solve_UC = range(start_time_period_to_solve, end_time_period_to_solve)
    # range_time_periods_to_solve_UC = range(8148, 8149)
    columns_status_constraints = cdu.create_columns_status_constraints(
        number_of_lines=number_of_lines)
    columns_elapsed_time = cdu.create_columns_elapsed_time()
    columns_computational_complexity = cdu.create_columns_computational_complexity()
    columns_objective_value = cdu.create_columns_objective_value()
    columns_gap = cdu.create_columns_gap()
    columns_termination_condition = cdu.create_columns_termination_condition()
    columns_nonzeros = cdu.create_columns_nonzeros()
    columns_subproblems = cdu.create_columns_subproblems()

    activation_constraint_status = pd.DataFrame(index=range_time_periods_to_solve_UC,
                                                columns=columns_status_constraints)
    elapsed_time_dataframe = pd.DataFrame(index=range_time_periods_to_solve_UC,
                                          columns=columns_elapsed_time)
    computational_complexity_dataframe = pd.DataFrame(index=range_time_periods_to_solve_UC,
                                                      columns=columns_computational_complexity)
    objective_value_dataframe = pd.DataFrame(index=range_time_periods_to_solve_UC,
                                             columns=columns_objective_value)
    gap_dataframe = pd.DataFrame(index=range_time_periods_to_solve_UC,
                                 columns=columns_gap)
    termination_condition_dataframe = pd.DataFrame(index=range_time_periods_to_solve_UC,
                                                   columns=columns_termination_condition)

    nonzeros_dataframe = pd.DataFrame(index=range_time_periods_to_solve_UC,
                                      columns=columns_nonzeros)
    subproblems_dataframe = pd.DataFrame(index=range_time_periods_to_solve_UC,
                                         columns=columns_subproblems)
    initial_time = time.time()
    for individual_time_period in range_time_periods_to_solve_UC:
        model_ptdf = UCMPLSQCP.unit_commitment_multi_period_load_shedding_quadratic_cost_ptdf(
            demand=pd.DataFrame(demand.iloc[individual_time_period, :]).transpose(),
            wind=pd.DataFrame(wind.iloc[individual_time_period, :]).transpose(),
            costs=costs,
            lower_bound_generators=lower_bound_generators,
            upper_bound_generators=upper_bound_generators,
            bounds_flow=bounds_flow,
            number_of_generators=number_of_generators,
            number_of_lines=number_of_lines,
            number_of_nodes=number_of_nodes,
            load_shedding_penalization_constant=load_shedding_penalization_constant,
            susceptances=susceptances,
            relationship_lines_nodes=relationship_lines_nodes,
            column_names_dataframe_lines_info=column_names_dataframe_lines_info,
            column_names_dataframe_generators_info=column_names_dataframe_generators_info,
            relationship_generators_nodes=relationship_generators_nodes,
            number_of_time_periods=number_of_time_periods,
            ptdf=ptdf_info)

        aa = 0
        (model_ptdf,
         solution,
         elapsed_time_per_individual) = su.solve_model(model=model_ptdf)
        # print("========================")
        # print("objective value = " + str(model_ptdf.objective_function()))
        # print("========================")
        aa = 0
        termination_condition_dataframe = cdu.update_termination_condition_dataframe(
            individual_time_period=individual_time_period,
            termination_condition_dataframe=termination_condition_dataframe,
            solution=solution)
        activation_constraint_status = cdu.update_activation_status_constraints(
            activation_constraint_status=activation_constraint_status,
            bounds_flow=bounds_flow,
            individual_time_period=individual_time_period,
            multi_period_load_shedding_quadratic_cost_UC_model=model_ptdf,
            number_of_lines=number_of_lines)
        elapsed_time_dataframe = cdu.update_elapsed_time_dataframe(elapsed_time_dataframe=elapsed_time_dataframe,
                                                                   elapsed_time=elapsed_time_per_individual,
                                                                   user_time=solution.solver(0).user_time,
                                                                   time=solution.solver(0).time,
                                                                   individual_time_period=individual_time_period)

        computational_complexity_dataframe = cdu.update_computational_complexity_dataframe(solution=solution,
                                                                                           individual_time_period=individual_time_period,
                                                                                           computational_complexity_dataframe=computational_complexity_dataframe)
        objective_value_dataframe = cdu.update_objective_value_dataframe(individual_time_period=individual_time_period,
                                                                         model=model_ptdf,
                                                                         objective_value_dataframe=objective_value_dataframe)

        gap_dataframe = cdu.update_gap_dataframe(gap_dataframe=gap_dataframe,
                                                 model=model_ptdf,
                                                 solution=solution,
                                                 individual_time_period=individual_time_period)
        nonzeros_dataframe = cdu.update_performance_number_of_nonzeros(individual_time_period=individual_time_period,
                                                                       nonzeros_dataframe=nonzeros_dataframe,
                                                                       solution=solution)
        subproblems_dataframe = cdu.update_performance_number_subproblems(individual_time_period=individual_time_period,
                                                                          subproblems_dataframe=subproblems_dataframe,
                                                                          solution=solution)

    final_time = time.time()
    print("Elapsed time load and solve UC = " + str(final_time - initial_time))

    coefficients_and_labels_database = pd.concat(
        [demand.iloc[range_time_periods_to_solve_UC, :], wind.iloc[range_time_periods_to_solve_UC, :],
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
