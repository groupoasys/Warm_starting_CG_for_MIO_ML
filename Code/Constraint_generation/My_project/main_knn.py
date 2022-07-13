import My_project.utils_knn_MILP as uknnMILP
import My_project.utils_knn_UC as uknnUC


def run_knn_classification(folder_particular_dataset,
                           grid_neighbours,
                           dataset_file,
                           start_time_period_to_solve,
                           end_time_period_to_solve,
                           division,
                           number_of_constraints,
                           end_string_name,
                           data_folder='../Data/',
                           results_folder='Results/'):
    if folder_particular_dataset in ['MILP_500']:
        uknnMILP.run_knn_classification_general_MILP(data_folder=data_folder,
                                                     dataset_file=dataset_file,
                                                     division=division,
                                                     end_string_name=end_string_name,
                                                     end_time_period_to_solve=end_time_period_to_solve,
                                                     folder_particular_dataset=folder_particular_dataset,
                                                     grid_neighbours=grid_neighbours,
                                                     number_of_constraints=number_of_constraints,
                                                     results_folder=results_folder,
                                                     start_time_period_to_solve=start_time_period_to_solve)

    elif folder_particular_dataset in ['UC_ptdf']:
        uknnUC.run_knn_classification_UC(dataset_file=dataset_file,
                                         division=division,
                                         end_string_name=end_string_name,
                                         end_time_period_to_solve=end_time_period_to_solve,
                                         folder_particular_dataset=folder_particular_dataset,
                                         grid_neighbours=grid_neighbours,
                                         number_of_constraints=number_of_constraints,
                                         results_folder=results_folder,
                                         start_time_period_to_solve=start_time_period_to_solve)
        aa = 0

    return 0
