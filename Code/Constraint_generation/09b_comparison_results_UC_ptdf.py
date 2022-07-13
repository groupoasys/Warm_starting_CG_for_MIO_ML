import My_project as mp

folder_particular_dataset = 'UC_ptdf'
# grid_neighbours = [5, 20, 100, 999]
grid_neighbours = [5, 10, 20, 50, 100]
total_number_of_constraints = 240

csv_files = {'benchmark': 'UC_coefficients_and_labels_and_more_info.csv',
             'CG': 'UC_performance_results.csv',
             'DD': 'UC_results_solve_model_old_knn_',
             'DD*': 'UC_results_solve_model_new_knn_',
             'knn_DD': 'UC_predictions_old_knn_',
             'knn_DD*': 'UC_predictions_new_knn_'}

mp.get_comparison_results(folder_particular_dataset=folder_particular_dataset,
                          grid_neighbours=grid_neighbours,
                          csv_files=csv_files,
                          total_number_of_constraints=total_number_of_constraints)
