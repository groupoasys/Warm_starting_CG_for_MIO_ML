import My_project as mp

folder_particular_dataset = 'MILP_500'
grid_neighbours = [1, 5, 10, 50, 100, 500, 999]
# grid_neighbours = [5]
total_number_of_constraints = 250
comparative_table_csv_name = 'MILP_comparative_results_iteratively.csv'

csv_files = {'benchmark': 'MILP_coefficients_and_labels_and_more_info.csv',
             'CG': 'MILP_performance_results_iteratively.csv',
             'DD': 'MILP_results_solve_model_old_knn_',
             'DD*': 'MILP_results_solve_model_new_knn_',
             'knn_DD': 'MILP_predictions_old_knn_',
             'knn_DD*': 'MILP_predictions_new_knn_'}

mp.get_comparison_results(folder_particular_dataset=folder_particular_dataset,
                          grid_neighbours=grid_neighbours,
                          csv_files=csv_files,
                          total_number_of_constraints=total_number_of_constraints,
                          comparative_table_csv_name=comparative_table_csv_name)
