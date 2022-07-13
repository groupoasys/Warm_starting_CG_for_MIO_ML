# Since the constraint generation algorithm returns the quasi active constraints, we can simply collect them from this output

import os

import My_project as mp

number_of_divisions = 100
folder_particular_dataset = 'MILP_500'

current_working_directory = os.getcwd()
mp.collect_results_CG_iteratively(number_of_divisions=number_of_divisions,
                                  beginning_file_active_constraints='performance_results_iteratively',
                                  folder_particular_dataset=folder_particular_dataset)
