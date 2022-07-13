import numpy as np
import pandas as pd
import time

import My_project.create_database_utils as cdu
import My_project.data_utils as du
import My_project.general_utils as gu
import My_project.names_excel_file as nef
import My_project.solve_utils as su
import My_project.UC_configuration as UCc
import My_project.Unit_Commitment_Multi_Period_Load_Shedding_Quadratic_Cost_PTDF as UCMPLSQCP
import My_project.utils_constraint_generation as ucg


def run_constraint_generation_UC(dataset_file,
                                 division,
                                 end_time_period_to_solve,
                                 folder_particular_dataset,
                                 results_folder,
                                 start_time_period_to_solve,
                                 indexes_time_periods={}):
    coefficients_and_labels = pd.read_csv(dataset_file, sep=';', index_col=0)
    (names_sheets_dataset_file,
     beginning_names_columns_data,
     column_names_generators_info,
     column_names_lines_info,
     column_names_general_info) = nef.get_names_excel_file()

    # os.chdir(path=data_folder + folder_particular_dataset)

    (data_and_labels,
     generators_info,
     lines_info,
     general_info,
     ptdf_info) = du.extract_problem_info_from_csv(dataset_file=dataset_file,
                                                   names_sheets_dataset_file=names_sheets_dataset_file)
    # os.chdir(path=current_working_directory)
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
    columns_status_constraints = cdu.create_columns_status_constraints(
        number_of_lines=number_of_lines)
    columns_flag_violated_constraints = gu.create_columns_flag_violated_constraints(
        number_of_constraints=2 * number_of_lines)
    range_time_periods_to_solve = range(start_time_period_to_solve, end_time_period_to_solve)
    # range_time_periods_to_solve = range(8148, 8149)

    updated_coefficients_and_labels = coefficients_and_labels.loc[range_time_periods_to_solve, :].copy()
    violated_constraints_flag_dataframe = pd.DataFrame(False, index=range_time_periods_to_solve,
                                                       columns=columns_flag_violated_constraints)
    constraint_generation_time = pd.DataFrame(index=range_time_periods_to_solve, columns=['CG time'])
    constraint_generation_time_solve_model = pd.DataFrame(index=range_time_periods_to_solve,
                                                          columns=['CG time solve model'])
    constraints_generation_counter = pd.DataFrame(index=range_time_periods_to_solve, columns=['CG counter'])
    number_of_constraints_final_UC = pd.DataFrame(index=range_time_periods_to_solve,
                                                  columns=['# constraints last UC'])
    objective_value_final_UC = pd.DataFrame(index=range_time_periods_to_solve, columns=['obj value last UC'])
    user_time_final_UC = pd.DataFrame(index=range_time_periods_to_solve, columns=['user time last UC'])
    elapsed_time_final_UC = pd.DataFrame(index=range_time_periods_to_solve, columns=['elapsed time last UC'])
    number_of_time_periods = 1
    # for individual_time_period in [8148]:  # range_time_periods_to_solve:
    for individual_time_period in range_time_periods_to_solve:
        print(individual_time_period)
        infeasibility_flag = True
        counter = 0
        CG_time_solve_model = 0
        t0 = time.time()
        while infeasibility_flag:
            # while infeasibility_flag and counter <= 1:
            demand_per_individual = pd.DataFrame(demand.iloc[individual_time_period, :]).transpose()
            wind_per_individual = pd.DataFrame(wind.iloc[individual_time_period, :]).transpose()
            model_ptdf = UCMPLSQCP.unit_commitment_multi_period_load_shedding_quadratic_cost_ptdf(
                demand=demand_per_individual,
                wind=wind_per_individual,
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
            labels_constraints_per_time_period = ucg.get_labels_constraints_per_time_period(
                coefficients_and_labels=updated_coefficients_and_labels,
                columns_status_constraints=columns_status_constraints,
                individual_time_period=individual_time_period)
            non_active_constraints = (np.where(np.array(labels_constraints_per_time_period) != 1)[0] + 1).tolist()

            model_ptdf = ucg.deactivate_constraints_UC(model=model_ptdf,
                                                       non_active_constraints=non_active_constraints,
                                                       number_of_lines=number_of_lines)

            aa = 0
            (model_ptdf,
             solution,
             elapsed_time) = su.solve_model(model=model_ptdf)
            # print("========================")
            # print("objective value = " + str(model_ptdf.objective_function()))
            # # print(model_ptdf.on_off_status_generators.display())
            # print(model_ptdf.generations.display())
            # print("========================")
            aa = 0
            CG_time_solve_model += solution.solver.user_time

            (identifier_violated_constraints,
             infeasibility_constraints_values,
             violated_constraints_flag) = ucg.identify_violated_constraints_UC(model=model_ptdf,
                                                                               non_active_constraints=non_active_constraints,
                                                                               number_of_lines=number_of_lines)
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
            aa = 0

        t1 = time.time()
        CG_time = t1 - t0

        aa = 0
        (constraint_generation_time,
         constraint_generation_time_solve_model,
         constraints_generation_counter,
         number_of_constraints_final_UC,
         objective_value_final_UC,
         user_time_final_UC,
         elapsed_time_final_UC) = ucg.get_performance_results(CG_time=CG_time,
                                                              CG_time_solve_model=CG_time_solve_model,
                                                              columns_status_constraints=columns_status_constraints,
                                                              constraint_generation_time=constraint_generation_time,
                                                              constraints_generation_counter=constraints_generation_counter,
                                                              counter=counter,
                                                              elapsed_time=elapsed_time,
                                                              elapsed_time_final_MILP=elapsed_time_final_UC,
                                                              individual_time_period=individual_time_period,
                                                              model=model_ptdf,
                                                              number_of_constraints=2 * number_of_lines,
                                                              number_of_constraints_final_MILP=number_of_constraints_final_UC,
                                                              objective_value_final_MILP=objective_value_final_UC,
                                                              solution=solution,
                                                              updated_coefficients_and_labels=updated_coefficients_and_labels,
                                                              user_time_final_MILP=user_time_final_UC,
                                                              constraint_generation_time_solve_model=constraint_generation_time_solve_model)
        aa = 0
    aa = 0
    performance_results = pd.concat(
        [updated_coefficients_and_labels, violated_constraints_flag_dataframe, constraint_generation_time,
         constraint_generation_time_solve_model, constraints_generation_counter, number_of_constraints_final_UC,
         objective_value_final_UC, user_time_final_UC, elapsed_time_final_UC], axis=1)
    gu.create_directory_if_it_does_not_exists(path=results_folder)
    gu.create_directory_if_it_does_not_exists(path=results_folder + folder_particular_dataset + '/')
    performance_results.to_csv(
        results_folder + folder_particular_dataset + '/performance_results_' + str(division) + '.csv', sep=';')

    return 0


def run_constraint_generation_iteratively_UC(dataset_file,
                                             division,
                                             end_time_period_to_solve,
                                             folder_particular_dataset,
                                             results_folder,
                                             start_time_period_to_solve,
                                             indexes_time_periods={}):
    coefficients_and_labels = pd.read_csv(dataset_file, sep=';', index_col=0)
    (names_sheets_dataset_file,
     beginning_names_columns_data,
     column_names_generators_info,
     column_names_lines_info,
     column_names_general_info) = nef.get_names_excel_file()

    # os.chdir(path=data_folder + folder_particular_dataset)

    (data_and_labels,
     generators_info,
     lines_info,
     general_info,
     ptdf_info) = du.extract_problem_info_from_csv(dataset_file=dataset_file,
                                                   names_sheets_dataset_file=names_sheets_dataset_file)
    # os.chdir(path=current_working_directory)
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
    columns_status_constraints = cdu.create_columns_status_constraints(
        number_of_lines=number_of_lines)
    columns_flag_violated_constraints = gu.create_columns_flag_violated_constraints(
        number_of_constraints=2 * number_of_lines)
    range_time_periods_to_solve = range(start_time_period_to_solve, end_time_period_to_solve)
    # range_time_periods_to_solve = range(8148, 8149)

    updated_coefficients_and_labels = coefficients_and_labels.loc[range_time_periods_to_solve, :].copy()
    updated_coefficients_and_labels.loc[:, columns_status_constraints] = -1
    violated_constraints_flag_dataframe = pd.DataFrame(False, index=range_time_periods_to_solve,
                                                       columns=columns_flag_violated_constraints)
    constraint_generation_time = pd.DataFrame(index=range_time_periods_to_solve, columns=['CG time'])
    constraint_generation_time_solve_model = pd.DataFrame(index=range_time_periods_to_solve,
                                                          columns=['CG time solve model'])
    constraints_generation_counter = pd.DataFrame(index=range_time_periods_to_solve, columns=['CG counter'])
    number_of_constraints_final_UC = pd.DataFrame(index=range_time_periods_to_solve,
                                                  columns=['# constraints last UC'])
    objective_value_final_UC = pd.DataFrame(index=range_time_periods_to_solve, columns=['obj value last UC'])
    user_time_final_UC = pd.DataFrame(index=range_time_periods_to_solve, columns=['user time last UC'])
    elapsed_time_final_UC = pd.DataFrame(index=range_time_periods_to_solve, columns=['elapsed time last UC'])
    number_of_time_periods = 1
    # for individual_time_period in [8148]:  # range_time_periods_to_solve:
    for individual_time_period in range_time_periods_to_solve:
        print(individual_time_period)
        infeasibility_flag = True
        counter = 0
        CG_time_solve_model = 0
        t0 = time.time()
        while infeasibility_flag:
            # while infeasibility_flag and counter <= 1:
            demand_per_individual = pd.DataFrame(demand.iloc[individual_time_period, :]).transpose()
            wind_per_individual = pd.DataFrame(wind.iloc[individual_time_period, :]).transpose()
            model_ptdf = UCMPLSQCP.unit_commitment_multi_period_load_shedding_quadratic_cost_ptdf(
                demand=demand_per_individual,
                wind=wind_per_individual,
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
            labels_constraints_per_time_period = ucg.get_labels_constraints_per_time_period(
                coefficients_and_labels=updated_coefficients_and_labels,
                columns_status_constraints=columns_status_constraints,
                individual_time_period=individual_time_period)
            non_active_constraints = (np.where(np.array(labels_constraints_per_time_period) != 1)[0] + 1).tolist()

            model_ptdf = ucg.deactivate_constraints_UC(model=model_ptdf,
                                                       non_active_constraints=non_active_constraints,
                                                       number_of_lines=number_of_lines)

            aa = 0
            (model_ptdf,
             solution,
             elapsed_time) = su.solve_model(model=model_ptdf)
            # print("========================")
            # print("objective value = " + str(model_ptdf.objective_function()))
            # # print(model_ptdf.on_off_status_generators.display())
            # print(model_ptdf.generations.display())
            # print("========================")
            aa = 0
            CG_time_solve_model += solution.solver.user_time

            (identifier_violated_constraints,
             infeasibility_constraints_values,
             violated_constraints_flag) = ucg.identify_violated_constraints_UC(model=model_ptdf,
                                                                               non_active_constraints=non_active_constraints,
                                                                               number_of_lines=number_of_lines)
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
            aa = 0

        t1 = time.time()
        CG_time = t1 - t0

        aa = 0
        (constraint_generation_time,
         constraint_generation_time_solve_model,
         constraints_generation_counter,
         number_of_constraints_final_UC,
         objective_value_final_UC,
         user_time_final_UC,
         elapsed_time_final_UC) = ucg.get_performance_results(CG_time=CG_time,
                                                              CG_time_solve_model=CG_time_solve_model,
                                                              columns_status_constraints=columns_status_constraints,
                                                              constraint_generation_time=constraint_generation_time,
                                                              constraints_generation_counter=constraints_generation_counter,
                                                              counter=counter,
                                                              elapsed_time=elapsed_time,
                                                              elapsed_time_final_MILP=elapsed_time_final_UC,
                                                              individual_time_period=individual_time_period,
                                                              model=model_ptdf,
                                                              number_of_constraints=2 * number_of_lines,
                                                              number_of_constraints_final_MILP=number_of_constraints_final_UC,
                                                              objective_value_final_MILP=objective_value_final_UC,
                                                              solution=solution,
                                                              updated_coefficients_and_labels=updated_coefficients_and_labels,
                                                              user_time_final_MILP=user_time_final_UC,
                                                              constraint_generation_time_solve_model=constraint_generation_time_solve_model)
        aa = 0
    aa = 0
    performance_results = pd.concat(
        [updated_coefficients_and_labels, violated_constraints_flag_dataframe, constraint_generation_time,
         constraint_generation_time_solve_model, constraints_generation_counter, number_of_constraints_final_UC,
         objective_value_final_UC, user_time_final_UC, elapsed_time_final_UC], axis=1)
    gu.create_directory_if_it_does_not_exists(path=results_folder)
    gu.create_directory_if_it_does_not_exists(path=results_folder + folder_particular_dataset + '/')
    performance_results.to_csv(
        results_folder + folder_particular_dataset + '/performance_results_iteratively_' + str(division) + '.csv',
        sep=';')

    return 0
