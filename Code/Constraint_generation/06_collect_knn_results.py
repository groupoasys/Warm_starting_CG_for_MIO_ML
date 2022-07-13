import os

import My_project as mp

number_of_divisions = 10
folder_particular_dataset = 'MILP_500'
# grid_neighbours = [5, 100, 999]
grid_neighbours = [1, 10, 50, 500]

current_directory = os.getcwd()
mp.collect_results_knn(number_of_divisions=number_of_divisions,
                       beginning_file_active_constraints='predictions_new_knn_',
                       folder_particular_dataset=folder_particular_dataset,
                       grid_neighbours=grid_neighbours)
os.chdir(current_directory)
mp.collect_results_knn(number_of_divisions=number_of_divisions,
                       beginning_file_active_constraints='predictions_old_knn_',
                       folder_particular_dataset=folder_particular_dataset,
                       grid_neighbours=grid_neighbours)
