import My_project as mp
import os

folder_particular_dataset = 'MILP_500'
# grid_neighbours = [5, 100, 999]
grid_neighbours = [1, 10, 50, 500]

indexes_time_periods = {'start': 0,
                        'end': 1000}
number_of_divisions = 10
number_of_constraints = 250
number_of_time_periods_per_division = int(indexes_time_periods['end'] / number_of_divisions)
cases = [[number_of_time_periods_per_division * division, number_of_time_periods_per_division * (division + 1)] for
         division in range(number_of_divisions)]

case = cases[int(os.environ['SLURM_ARRAY_TASK_ID']) - 1]
os.environ['OMP_NUM_THREADS'] = '1'

division = cases.index(case)
dataset_file = 'MILP_performance_results.csv'
end_string_name = 'new'
mp.run_knn_classification(folder_particular_dataset=folder_particular_dataset,
                          grid_neighbours=grid_neighbours,
                          dataset_file=dataset_file,
                          start_time_period_to_solve=case[0],
                          end_time_period_to_solve=case[1],
                          division=division,
                          end_string_name=end_string_name,
                          number_of_constraints=number_of_constraints)
dataset_file = 'MILP_coefficients_and_labels_and_more_info.csv'
end_string_name = 'old'
mp.run_knn_classification(folder_particular_dataset=folder_particular_dataset,
                          grid_neighbours=grid_neighbours,
                          dataset_file=dataset_file,
                          start_time_period_to_solve=case[0],
                          end_time_period_to_solve=case[1],
                          division=division,
                          end_string_name=end_string_name,
                          number_of_constraints=number_of_constraints)
