import os
import pandas as pd


def collect_results_knn(number_of_divisions,
                        grid_neighbours,
                        database_results_folder='Results',
                        beginning_file_active_constraints='coefficients_and_labels',
                        folder_particular_dataset='Unit_Commitment'):
    os.chdir(database_results_folder)
    os.chdir(folder_particular_dataset)

    for number_of_neighbors in grid_neighbours:
        dataframe_to_save = pd.DataFrame()
        for division in range(number_of_divisions):
            dataframe_to_save_per_division = pd.read_csv(
                beginning_file_active_constraints + str(number_of_neighbors) + '_' + str(division) + '.csv', sep=';',
                index_col=0)
            dataframe_to_save = pd.concat([dataframe_to_save, dataframe_to_save_per_division], axis=0)

        if folder_particular_dataset in ['MILP_500']:
            dataframe_to_save.to_csv('MILP_' + beginning_file_active_constraints + str(number_of_neighbors) + '.csv',
                                     sep=';')
            dataframe_to_save.to_csv(
                '../../../Data/' + folder_particular_dataset + '/MILP_' + beginning_file_active_constraints + str(
                    number_of_neighbors) + '.csv', sep=';')
        elif folder_particular_dataset in ['UC_ptdf']:
            dataframe_to_save.to_csv('UC_' + beginning_file_active_constraints + str(number_of_neighbors) + '.csv',
                                     sep=';')
            dataframe_to_save.to_csv(
                '../../../Data/' + folder_particular_dataset + '/UC_' + beginning_file_active_constraints + str(
                    number_of_neighbors) + '.csv', sep=';')

    return 0
