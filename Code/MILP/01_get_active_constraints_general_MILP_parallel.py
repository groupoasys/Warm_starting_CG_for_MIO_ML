import My_project as mp

import os

particular_folder_results = 'MILP_500'
indexes_time_periods = {'start': 0,
                        'end': 1000}
number_of_divisions = 20
number_of_time_periods_per_division = int(indexes_time_periods['end'] / number_of_divisions)
cases = [[number_of_time_periods_per_division * division, number_of_time_periods_per_division * (division + 1)] for
         division in range(number_of_divisions)]

case = cases[int(os.environ['SLURM_ARRAY_TASK_ID']) - 1]
os.environ['OMP_NUM_THREADS'] = '1'
division = cases.index(case)
mp.run_main_general_MILP(particular_folder_results=particular_folder_results,
                         division=division,
                         start_time_period_to_solve=case[0],
                         end_time_period_to_solve=case[1])
