import os

import My_project as mp

number_of_divisions = 96
folder_particular_dataset = 'UC_ptdf'
# grid_neighbours = [5, 20, 100, 999]
grid_neighbours = [10, 50]

current_directory = os.getcwd()
mp.collect_results_solve_predicted_model_knn(number_of_divisions=number_of_divisions,
                                             beginning_file_active_constraints='results_solve_model_new_knn_',
                                             folder_particular_dataset=folder_particular_dataset,
                                             grid_neighbours=grid_neighbours)
os.chdir(current_directory)
mp.collect_results_solve_predicted_model_knn(number_of_divisions=number_of_divisions,
                                             beginning_file_active_constraints='results_solve_model_old_knn_',
                                             folder_particular_dataset=folder_particular_dataset,
                                             grid_neighbours=grid_neighbours)
