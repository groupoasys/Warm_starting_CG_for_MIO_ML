import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import time

import My_project.utils_knn as uknn


def run_knn_classification_general_MILP(data_folder,
                                        dataset_file,
                                        division,
                                        end_string_name,
                                        end_time_period_to_solve,
                                        folder_particular_dataset,
                                        grid_neighbours,
                                        number_of_constraints,
                                        results_folder,
                                        start_time_period_to_solve):
    coefficients_and_labels = pd.read_csv(data_folder + folder_particular_dataset + '/' + dataset_file, sep=';',
                                          index_col=0)
    data = coefficients_and_labels.iloc[:, 0:number_of_constraints]
    labels = coefficients_and_labels.iloc[:, (number_of_constraints):(2 * number_of_constraints)]
    total_number_of_elements = coefficients_and_labels.shape[0]
    range_time_periods = range(start_time_period_to_solve, end_time_period_to_solve)
    column_name_prediction_time_knn = 'pred knn time'
    column_name_modify_time_knn = 'mod knn time'
    column_name_total_time_knn = 'total knn time'
    columns_activation_label_constraint_status = coefficients_and_labels.columns[
                                                 number_of_constraints:(2 * number_of_constraints)]
    for number_of_neighbors in grid_neighbours:
        coefficients_and_labels_after_knn_per_number_of_neighbors = coefficients_and_labels.iloc[range_time_periods,
                                                                    0:(2 * number_of_constraints)].copy()
        elapsed_time_knn_per_number_of_neighbors = pd.DataFrame(index=range_time_periods,
                                                                columns=[column_name_prediction_time_knn,
                                                                         column_name_modify_time_knn,
                                                                         column_name_total_time_knn])
        modified_predictions = pd.DataFrame(index=range_time_periods,
                                            columns=columns_activation_label_constraint_status)
        for time_period in range_time_periods:
            (train_indexes,
             test_indexes) = uknn.get_sampling_configuration(time_period=time_period,
                                                             total_number_of_elements=total_number_of_elements)

            data_train = data.loc[train_indexes, :]
            # labels_train = labels.loc[train_indexes, 'act_label_orig_opt_problem_c3']
            labels_train = labels.loc[train_indexes, :]

            data_test = data.loc[test_indexes, :]
            # labels_test = labels.loc[test_indexes, 'act_label_orig_opt_problem_c3']
            labels_test = labels.loc[test_indexes, :]
            neigh = KNeighborsClassifier(n_neighbors=number_of_neighbors)
            # t2 = time.time()
            neigh.fit(data_train, labels_train)
            aa = 0
            t0 = time.time()
            predictions_test = neigh.predict(data_test)
            probability_test = neigh.predict_proba(data_test)
            t1 = time.time()
            modified_predictions_test = uknn.modify_predictions_test_to_be_more_conservative(
                predictions_test=predictions_test,
                probability_test=probability_test)
            t2 = time.time()
            prediction_time_knn = t1 - t0
            modify_time_knn = t2 - t1
            total_time_knn = t2 - t0

            # Toy example to check what happens.
            # data_tr = pd.DataFrame([[0, 1], [3, 3], [2, 2]]).T
            # labels_tr = pd.DataFrame(data=[[1, 1], [1, -1], [-1, -1]]).T
            # data_t = pd.DataFrame([[0.7], [3], [2]]).T
            # knn = KNeighborsClassifier(n_neighbors=2)
            # knn.fit(data_tr, labels_tr)
            # pred_t = knn.predict(data_t)
            # prob_test = knn.predict_proba(data_t)

            modified_predictions.loc[time_period, :] = modified_predictions_test[0]
            # coefficients_and_labels_after_knn_per_number_of_neighbors.iloc[:,
            # (number_of_constraints):(2 * number_of_constraints)].loc[time_period, :] = modified_predictions_test[0]
            elapsed_time_knn_per_number_of_neighbors.loc[
                time_period, column_name_prediction_time_knn] = prediction_time_knn
            elapsed_time_knn_per_number_of_neighbors.loc[time_period, column_name_modify_time_knn] = modify_time_knn
            elapsed_time_knn_per_number_of_neighbors.loc[time_period, column_name_total_time_knn] = total_time_knn
            aa = 0
        dataframe_to_save = pd.concat(
            [data.iloc[range_time_periods, :], modified_predictions, elapsed_time_knn_per_number_of_neighbors],
            axis=1)
        dataframe_to_save.to_csv(
            results_folder + folder_particular_dataset + "/predictions_" + end_string_name + "_knn_" + str(
                number_of_neighbors) + '_' + str(division) + '.csv', sep=';')
    return 0
