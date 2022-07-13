import os

import My_project as mp

dataset_file = "../Data/UC_ptdf/UC_coefficients_info.csv"
particular_folder_results = 'UC_ptdf'

indexes_time_periods = {'start': 0,
                        'end': 8640}
number_of_divisions = 12
number_of_time_periods_per_division = int(indexes_time_periods['end'] / number_of_divisions)
cases = [[number_of_time_periods_per_division * division, number_of_time_periods_per_division * (division + 1)] for
         division in range(number_of_divisions)]

case = cases[int(os.environ['SLURM_ARRAY_TASK_ID']) - 1]
os.environ['OMP_NUM_THREADS'] = '1'
division = cases.index(case)
mp.run_main_UC(dataset_file=dataset_file,
               start_time_period_to_solve=case[0],
               end_time_period_to_solve=case[1],
               division=division,
               particular_folder_results=particular_folder_results)
