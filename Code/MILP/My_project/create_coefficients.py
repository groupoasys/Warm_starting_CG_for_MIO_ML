import random
import pandas as pd

import My_project.general_utils as gu


def create_coefficients(number_of_continuous_variables,
                        number_of_constraints,
                        number_of_individuals,
                        folder_particular_dataset,
                        data_folder='../Data/'):
    random.seed(1903)
    number_of_individuals_independent_term = number_of_individuals
    range_individuals = range(1, number_of_individuals_independent_term + 1)
    range_constraints = range(1, number_of_constraints + 1)
    range_continuous_variables = range(1, number_of_continuous_variables + 1)

    number_of_digits_rounding = 2

    costs = list(
        map(lambda x: round(random.gauss(0, 10), ndigits=number_of_digits_rounding), range_continuous_variables))
    costs = pd.DataFrame(data=costs,
                         index=range_continuous_variables,
                         columns=[1]).transpose()

    lower_bound_continuous_variables = list(
        map(lambda x: round(random.gauss(0, 10), ndigits=number_of_digits_rounding), range_continuous_variables))
    upper_bound_continuous_variables = list(
        map(lambda x: round(random.gauss(0, 10), ndigits=number_of_digits_rounding), range_continuous_variables))
    for variable in range_continuous_variables:
        lower_bound_per_variable = lower_bound_continuous_variables[variable - 1]
        upper_bound_per_variable = upper_bound_continuous_variables[variable - 1]
        if lower_bound_per_variable > upper_bound_per_variable:
            lower_bound_continuous_variables[variable - 1] = upper_bound_per_variable
            upper_bound_continuous_variables[variable - 1] = lower_bound_per_variable
    lower_bound_continuous_variables = pd.DataFrame(data=lower_bound_continuous_variables,
                                                    index=range_continuous_variables,
                                                    columns=[1]).transpose()
    upper_bound_continuous_variables = pd.DataFrame(data=upper_bound_continuous_variables,
                                                    index=range_continuous_variables,
                                                    columns=[1]).transpose()
    coefficient_matrix = list(
        map(lambda y: list(
            map(lambda x: round(random.gauss(0, 10), ndigits=number_of_digits_rounding), range_continuous_variables)),
            range_constraints))
    coefficient_matrix = pd.DataFrame(data=coefficient_matrix,
                                      index=range_constraints,
                                      columns=range_continuous_variables)

    independent_term_dataframe = pd.DataFrame(index=range_constraints,
                                              columns=range(0, number_of_individuals))
    for individual in range_individuals:
        independent_term = list(
            map(lambda x: round(random.gauss(0, 10), ndigits=number_of_digits_rounding), range_constraints))
        independent_term_dataframe.loc[:, individual - 1] = independent_term
    independent_term_dataframe = independent_term_dataframe.transpose()

    path = data_folder + folder_particular_dataset
    gu.create_directory_if_it_does_not_exists(path=path)

    costs.to_csv(path + '/costs.csv', sep=';')
    lower_bound_continuous_variables.to_csv(path + '/lower_bound_continuous_variables.csv', sep=';')
    upper_bound_continuous_variables.to_csv(path + '/upper_bound_continuous_variables.csv', sep=';')
    coefficient_matrix.to_csv(path + '/coefficient_matrix.csv', sep=';')
    independent_term_dataframe.to_csv(path + '/independent_term.csv', sep=';')

    return (costs,
            lower_bound_continuous_variables,
            upper_bound_continuous_variables,
            coefficient_matrix,
            independent_term_dataframe)
