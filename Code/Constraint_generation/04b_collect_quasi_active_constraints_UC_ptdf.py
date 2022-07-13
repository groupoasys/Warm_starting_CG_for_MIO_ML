# Since the constraint generation algorithm returns the quasi active constraints, we can simply collect them from this output

import os

import My_project as mp

number_of_divisions = 12
folder_particular_dataset = 'UC_ptdf'

current_working_directory = os.getcwd()
mp.collect_results_quasi_active_constraints(number_of_divisions=number_of_divisions,
                                            beginning_file_active_constraints='performance_results',
                                            folder_particular_dataset=folder_particular_dataset)
