import pandas as pd
import os

import My_project.create_database_utils as cdu


def collect_results_active_constraints_UC(number_of_divisions,
                                          database_results_folder='Results',
                                          beginning_file_active_constraints='coefficients_and_labels',
                                          folder_particular_dataset='Unit_Commitment'):
    coefficients_and_labels_and_more_info = pd.DataFrame()
    coefficients_and_labels = pd.DataFrame()

    columns_elapsed_time = cdu.create_columns_elapsed_time()
    columns_objective_value = cdu.create_columns_objective_value()
    columns_gap = cdu.create_columns_gap()
    columns_termination_condition = cdu.create_columns_termination_condition()
    columns_to_drop = columns_elapsed_time + columns_objective_value + columns_gap + columns_termination_condition

    os.chdir(database_results_folder + '//' + folder_particular_dataset)
    for division in range(number_of_divisions):
        coefficients_and_labels_and_more_info_per_division = pd.read_csv(
            beginning_file_active_constraints + '_' + str(division) + '.csv', index_col=0, sep=';')

        coefficients_and_labels_per_division = coefficients_and_labels_and_more_info_per_division.copy()
        coefficients_and_labels_per_division = coefficients_and_labels_per_division.drop(columns_to_drop, axis=1)

        coefficients_and_labels_and_more_info = pd.concat(
            [coefficients_and_labels_and_more_info, coefficients_and_labels_and_more_info_per_division], axis=0)
        coefficients_and_labels = pd.concat([coefficients_and_labels, coefficients_and_labels_per_division], axis=0)

    indexes_train = range(0, 7200)
    indexes_test = range(7200, 8640)

    averaged_performance_results_train = coefficients_and_labels_and_more_info.loc[
        indexes_train, columns_elapsed_time + columns_gap].mean()
    averaged_performance_results_train = pd.concat([averaged_performance_results_train, (
            coefficients_and_labels_and_more_info.loc[
                indexes_train, columns_termination_condition] == 'optimal').sum()], axis=0)
    averaged_performance_results_test = coefficients_and_labels_and_more_info.loc[
        indexes_test, columns_elapsed_time + columns_gap].mean()
    averaged_performance_results_test = pd.concat([averaged_performance_results_test, (
            coefficients_and_labels_and_more_info.loc[
                indexes_test, columns_termination_condition] == 'optimal').sum()], axis=0)

    averaged_performance_results_train.to_csv('00_summary_performance_UC_train.csv', sep=';')
    averaged_performance_results_test.to_csv('00_summary_performance_UC_test.csv', sep=';')

    coefficients_and_labels_and_more_info.to_csv('UC_' + beginning_file_active_constraints + '_and_more_info.csv',
                                                 sep=';')
    coefficients_and_labels_and_more_info.to_csv(
        '../../../Data/' + folder_particular_dataset + '/UC_' + beginning_file_active_constraints + '_and_more_info.csv',
        sep=';')

    coefficients_and_labels.to_csv('UC_' + beginning_file_active_constraints + '_info.csv', sep=';')
    coefficients_and_labels.to_csv(
        '../../../Data/' + folder_particular_dataset + '/UC_' + beginning_file_active_constraints + '_info.csv',
        sep=';')
    return 0
