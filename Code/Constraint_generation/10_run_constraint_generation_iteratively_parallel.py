import My_project as mp

import os

dataset_file = 'MILP_coefficients_and_labels_info.csv'
indexes_time_periods = {'start': 0,
                        'end': 1000}
folder_particular_dataset = 'MILP_500'
number_of_divisions = 100
number_of_time_periods_per_division = int(indexes_time_periods['end'] / number_of_divisions)
cases = [[number_of_time_periods_per_division * division, number_of_time_periods_per_division * (division + 1)] for
         division in range(number_of_divisions)]

case = cases[int(os.environ['SLURM_ARRAY_TASK_ID']) - 1]
os.environ['OMP_NUM_THREADS'] = '1'

division = cases.index(case)
mp.run_constraint_generation_iteratively(dataset_file=dataset_file,
                                         start_time_period_to_solve=case[0],
                                         end_time_period_to_solve=case[1],
                                         division=division,
                                         folder_particular_dataset=folder_particular_dataset)
