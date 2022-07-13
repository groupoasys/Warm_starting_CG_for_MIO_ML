import My_project as mp

number_of_continuous_variables = 500
number_of_constraints = int(number_of_continuous_variables / 2)
number_of_individuals = 1000
folder_particular_dataset = 'MILP_' + str(number_of_continuous_variables)

(costs,
 lower_bound_continuous_variables_dataframe,
 upper_bound_continuous_variables_dataframe,
 coefficient_matrix,
 independent_term_dataframe) = mp.create_coefficients(
    number_of_continuous_variables=number_of_continuous_variables,
    number_of_constraints=number_of_constraints,
    number_of_individuals=number_of_individuals,
    folder_particular_dataset=folder_particular_dataset)
