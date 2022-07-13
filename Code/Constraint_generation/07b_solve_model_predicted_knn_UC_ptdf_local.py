import My_project as mp

indexes_time_periods = {'start': 0,
                        'end': 8640}
folder_particular_dataset = 'UC_ptdf'
number_of_divisions = 96
grid_neighbors = [5, 20, 100, 999]
number_of_time_periods_per_division = int(indexes_time_periods['end'] / number_of_divisions)
cases = [[number_of_time_periods_per_division * division, number_of_time_periods_per_division * (division + 1)] for
         division in range(number_of_divisions)]

for case in cases:
    division = cases.index(case)
    beginning_csv_file = 'UC_predictions_old_knn_'
    end_string_file = 'old'
    mp.run_solve_model_predicted_knn(beginning_csv_file=beginning_csv_file,
                                     start_time_period_to_solve=case[0],
                                     end_time_period_to_solve=case[1],
                                     division=division,
                                     folder_particular_dataset=folder_particular_dataset,
                                     grid_neighbors=grid_neighbors,
                                     end_string_file=end_string_file)
    beginning_csv_file = 'UC_predictions_new_knn_'
    end_string_file = 'new'
    mp.run_solve_model_predicted_knn(beginning_csv_file=beginning_csv_file,
                                     start_time_period_to_solve=case[0],
                                     end_time_period_to_solve=case[1],
                                     division=division,
                                     folder_particular_dataset=folder_particular_dataset,
                                     grid_neighbors=grid_neighbors,
                                     end_string_file=end_string_file)
