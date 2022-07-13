import numpy as np


def get_sampling_configuration(time_period,
                               total_number_of_elements):
    train_indexes = sorted(list(set(list(range(0, total_number_of_elements))) - set([time_period])))
    test_indexes = [time_period]

    return (train_indexes,
            test_indexes)


def modify_predictions_test_to_be_more_conservative(predictions_test,
                                                    probability_test):
    modified_predictions_test = predictions_test.copy()
    probability_test_of_being_class_minus_1 = np.array(list(map(lambda x: x[0][0], probability_test)))
    modified_predictions_test[
        np.logical_and(predictions_test == -1, probability_test_of_being_class_minus_1 != 1)] = 1
    return modified_predictions_test


def modify_predictions_test_to_be_more_conservative_proof(predictions_test,
                                                          probability_test):
    modified_predictions_test = predictions_test.copy()
    probability_test_of_being_class_minus_1 = np.array(list(map(lambda x: x[0], probability_test)))
    modified_predictions_test[
        np.logical_and(predictions_test == -1, probability_test_of_being_class_minus_1 != 1)] = 1
    return modified_predictions_test
