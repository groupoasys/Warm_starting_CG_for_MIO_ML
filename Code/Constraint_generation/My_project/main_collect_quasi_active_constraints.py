import os
import pandas as pd


def collect_results_quasi_active_constraints(number_of_divisions,
                                             database_results_folder='Results',
                                             beginning_file_active_constraints='coefficients_and_labels',
                                             folder_particular_dataset='Unit_Commitment'):
    coefficients_and_labels = pd.DataFrame()
    os.chdir(database_results_folder)
    os.chdir(folder_particular_dataset)

    for division in range(number_of_divisions):
        coefficients_and_labels_per_division = pd.read_csv('performance_results_' + str(division) + '.csv', sep=';',
                                                           index_col=0)
        coefficients_and_labels = pd.concat([coefficients_and_labels, coefficients_and_labels_per_division], axis=0)

    if folder_particular_dataset in ['MILP_500']:
        coefficients_and_labels.to_csv('MILP_' + beginning_file_active_constraints + '.csv', sep=';')
        coefficients_and_labels.to_csv(
            '../../../Data/' + folder_particular_dataset + '/MILP_' + beginning_file_active_constraints + '.csv',
            sep=';')
    elif folder_particular_dataset in ['UC_ptdf']:
        coefficients_and_labels.to_csv('UC_' + beginning_file_active_constraints + '.csv', sep=';')
        coefficients_and_labels.to_csv(
            '../../../Data/' + folder_particular_dataset + '/UC_' + beginning_file_active_constraints + '.csv',
            sep=';')

    return 0
