import My_project.utils_solve_model_predicted_knn_general_MILP as usmpknngMILP
import My_project.utils_solve_model_predicted_knn_UC as usmpknnUC


def run_solve_model_predicted_knn(beginning_csv_file,
                                  grid_neighbors,
                                  start_time_period_to_solve,
                                  end_time_period_to_solve,
                                  division,
                                  folder_particular_dataset,
                                  end_string_file,
                                  data_folder='../Data/',
                                  results_folder='Results/'):
    if folder_particular_dataset in ['MILP_500']:
        usmpknngMILP.run_solve_model_predicted_knn_general_MILP(beginning_csv_file=beginning_csv_file,
                                                                data_folder=data_folder,
                                                                division=division,
                                                                end_string_file=end_string_file,
                                                                end_time_period_to_solve=end_time_period_to_solve,
                                                                folder_particular_dataset=folder_particular_dataset,
                                                                grid_neighbors=grid_neighbors,
                                                                results_folder=results_folder,
                                                                start_time_period_to_solve=start_time_period_to_solve)
    elif folder_particular_dataset in ['UC_ptdf']:
        usmpknnUC.run_solve_model_predicted_knn_UC(beginning_csv_file=beginning_csv_file,
                                                   data_folder=data_folder,
                                                   division=division,
                                                   end_string_file=end_string_file,
                                                   end_time_period_to_solve=end_time_period_to_solve,
                                                   folder_particular_dataset=folder_particular_dataset,
                                                   grid_neighbors=grid_neighbors,
                                                   results_folder=results_folder,
                                                   start_time_period_to_solve=start_time_period_to_solve)
    return 0
