import My_project.utils_CG_MILP as uCGMILP
import My_project.utils_CG_UC as uCGUC


def run_constraint_generation(dataset_file,
                              start_time_period_to_solve,
                              end_time_period_to_solve,
                              division,
                              folder_particular_dataset,
                              data_folder='../Data/',
                              results_folder='Results/'):
    if folder_particular_dataset in ['MILP_500']:
        uCGMILP.run_constraint_generation_MILP(data_folder=data_folder,
                                               dataset_file=dataset_file,
                                               division=division,
                                               end_time_period_to_solve=end_time_period_to_solve,
                                               folder_particular_dataset=folder_particular_dataset,
                                               results_folder=results_folder,
                                               start_time_period_to_solve=start_time_period_to_solve)

    elif folder_particular_dataset in ['UC_ptdf']:
        uCGUC.run_constraint_generation_UC(dataset_file=dataset_file,
                                           division=division,
                                           end_time_period_to_solve=end_time_period_to_solve,
                                           folder_particular_dataset=folder_particular_dataset,
                                           results_folder=results_folder,
                                           start_time_period_to_solve=start_time_period_to_solve)
        aa = 0

    return 0
