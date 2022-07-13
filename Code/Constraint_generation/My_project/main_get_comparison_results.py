import My_project.utils_comparison_results_general_MILP as ucrgMILP
import My_project.utils_comparison_results_UC as ucrUC


def get_comparison_results(folder_particular_dataset,
                           grid_neighbours,
                           csv_files,
                           total_number_of_constraints,
                           comparative_table_csv_name,
                           threshold_equality=1e-5,
                           data_folder='../Data/',
                           database_results_folder='Results'):
    if folder_particular_dataset in ['MILP_500']:
        ucrgMILP.get_comparative_results_general_MILP(csv_files=csv_files,
                                                      data_folder=data_folder,
                                                      folder_particular_dataset=folder_particular_dataset,
                                                      grid_neighbours=grid_neighbours,
                                                      threshold_equality=threshold_equality,
                                                      total_number_of_constraints=total_number_of_constraints,
                                                      comparative_table_csv_name=comparative_table_csv_name)
    elif folder_particular_dataset in ['UC_ptdf']:
        ucrUC.get_comparative_results_UC(csv_files=csv_files,
                                         data_folder=data_folder,
                                         folder_particular_dataset=folder_particular_dataset,
                                         grid_neighbours=grid_neighbours,
                                         threshold_equality=threshold_equality,
                                         total_number_of_constraints=total_number_of_constraints,
                                         comparative_table_csv_name=comparative_table_csv_name)

    return 0
