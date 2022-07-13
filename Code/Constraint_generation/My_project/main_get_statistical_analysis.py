import My_project.utils_statistical_analysis_general_MILP as usagMILP
import My_project.utils_statistical_analysis_UC as usaUC


def get_statistical_analysis(folder_particular_dataset,
                             grid_neighbours,
                             csv_files,
                             total_number_of_constraints,
                             comparative_table_constraints_csv_name,
                             comparative_table_iterations_csv_name,
                             comparative_table_online_time_csv_name,
                             threshold_equality=1e-5,
                             data_folder='../Data/'):
    if folder_particular_dataset in ['MILP_500']:
        usagMILP.get_statistical_analysis_general_MILP(csv_files=csv_files,
                                                       data_folder=data_folder,
                                                       folder_particular_dataset=folder_particular_dataset,
                                                       grid_neighbours=grid_neighbours,
                                                       comparative_table_constraints_csv_name=comparative_table_constraints_csv_name,
                                                       comparative_table_iterations_csv_name=comparative_table_iterations_csv_name,
                                                       threshold_equality=threshold_equality,
                                                       total_number_of_constraints=total_number_of_constraints,
                                                       comparative_table_online_time_csv_name=comparative_table_online_time_csv_name)
    elif folder_particular_dataset in ['UC_ptdf']:
        usaUC.get_statistical_analysis_UC(csv_files=csv_files,
                                          data_folder=data_folder,
                                          folder_particular_dataset=folder_particular_dataset,
                                          grid_neighbours=grid_neighbours,
                                          threshold_equality=threshold_equality,
                                          total_number_of_constraints=total_number_of_constraints,
                                          comparative_table_constraints_csv_name=comparative_table_constraints_csv_name,
                                          comparative_table_iterations_csv_name=comparative_table_iterations_csv_name,
                                          comparative_table_online_time_csv_name=comparative_table_online_time_csv_name)

    return 0
