import My_project as mp

dataset_file = "../Data/UC_ptdf/UC_coefficients_and_labels_info.csv"
indexes_time_periods = {'start': 0,
                        'end': 8640}
folder_particular_dataset = 'UC_ptdf'
number_of_divisions = 100
number_of_time_periods_per_division = int(indexes_time_periods['end'] / number_of_divisions)
cases = [[number_of_time_periods_per_division * division, number_of_time_periods_per_division * (division + 1)] for
         division in range(number_of_divisions)]
for case in cases:
    division = cases.index(case)
    mp.run_constraint_generation(dataset_file=dataset_file,
                                 start_time_period_to_solve=case[0],
                                 end_time_period_to_solve=case[1],
                                 division=division,
                                 folder_particular_dataset=folder_particular_dataset)
