import pyomo.environ as pe


def create_optimization_model(number_of_continuous_variables,
                              costs,
                              lower_bound_continuous_variables,
                              upper_bound_continuous_variables,
                              coefficient_matrix,
                              independent_term,
                              number_of_constraints):
    model = pe.ConcreteModel("model")

    # Parameters
    model.number_of_continuous_variables = number_of_continuous_variables
    model.costs = costs
    model.lower_bound_continuous_variables = lower_bound_continuous_variables
    model.upper_bound_continuous_variables = upper_bound_continuous_variables
    model.coefficient_matrix = coefficient_matrix
    model.independent_term = independent_term
    model.number_of_constraints = number_of_constraints

    # Indexes
    model.indexes_continuous_variables = pe.RangeSet(model.number_of_continuous_variables)
    model.indexes_binary_variables = pe.RangeSet(model.number_of_continuous_variables)
    model.indexes_constraints = pe.RangeSet(model.number_of_constraints)

    # Variables

    model.continuous_variables = pe.Var(model.indexes_continuous_variables,
                                        within=pe.Reals)
    model.binary_variables = pe.Var(model.indexes_binary_variables,
                                    within=pe.Binary)

    # Objective Function

    model.objective_function = pe.Objective(rule=objective_function,
                                            sense=pe.minimize)

    # Constraints
    # model.equality_constraint = pe.Constraint(rule=equality_constraint)
    model.lower_bound_constraint = pe.Constraint(model.indexes_continuous_variables,
                                                 rule=lower_bound_constraint)
    model.upper_bound_constraint = pe.Constraint(model.indexes_continuous_variables,
                                                 rule=upper_bound_constraint)
    model.inequality_constraint = pe.Constraint(model.indexes_constraints,
                                                rule=inequality_constraint)
    # model.inequality_constraint_redundant = pe.Constraint(model.indexes_constraints,
    #                                                       rule=inequality_constraint_redundant)
    # model.inequality_constraint_redundant_2 = pe.Constraint(model.indexes_constraints,
    #                                                         rule=inequality_constraint_redundant_2)
    # model.inequality_constraint_redundant_3 = pe.Constraint(model.indexes_constraints,
    #                                                         rule=inequality_constraint_redundant_3)
    # model.inequality_constraint_redundant_4 = pe.Constraint(model.indexes_constraints,
    #                                                         rule=inequality_constraint_redundant_4)
    # model.inequality_constraint_redundant_5 = pe.Constraint(model.indexes_constraints,
    #                                                         rule=inequality_constraint_redundant_5)
    # model.inequality_constraint_redundant_6 = pe.Constraint(model.indexes_constraints,
    #                                                         rule=inequality_constraint_redundant_6)

    return model


def objective_function(model):
    objective_value = sum(model.costs.iloc[0, variable - 1] * model.continuous_variables[variable] for variable in
                          model.indexes_continuous_variables)
    return objective_value


#
# def equality_constraint(model):
#     constraint_value = sum(
#         model.zero_or_one_coefficient[variable - 1] * model.continuous_variables[variable] for variable in
#         model.indexes_continuous_variables) == model.independent_term_zero_or_one_constraint
#     return constraint_value


def lower_bound_constraint(model,
                           variable):
    constraint_value = model.continuous_variables[variable] >= model.binary_variables[variable] * \
                       model.lower_bound_continuous_variables.iloc[0, variable - 1]

    return constraint_value


def upper_bound_constraint(model,
                           variable):
    constraint_value = model.continuous_variables[variable] <= model.binary_variables[variable] * \
                       model.upper_bound_continuous_variables.iloc[0, variable - 1]

    return constraint_value


def inequality_constraint(model,
                          constraint):
    constraint_value = sum(
        model.coefficient_matrix.iloc[constraint - 1, variable - 1] * model.continuous_variables[variable] for variable
        in model.indexes_continuous_variables) <= model.independent_term[constraint - 1]

    return constraint_value


# def inequality_constraint_redundant(model,
#                                     constraint):
#     constraint_value = sum(
#         model.coefficient_matrix[constraint - 1][variable - 1] * model.continuous_variables[variable] for variable in
#         model.indexes_continuous_variables) <= 2 * model.independent_term[constraint - 1]
#
#     return constraint_value
#
#
# def inequality_constraint_redundant_2(model,
#                                       constraint):
#     constraint_value = sum(
#         model.coefficient_matrix[constraint - 1][variable - 1] * model.continuous_variables[variable] for variable in
#         model.indexes_continuous_variables) <= 5 * model.independent_term[constraint - 1]
#
#     return constraint_value
#
#
# def inequality_constraint_redundant_3(model,
#                                       constraint):
#     constraint_value = sum(
#         model.coefficient_matrix[constraint - 1][variable - 1] * model.continuous_variables[variable] for variable in
#         model.indexes_continuous_variables) <= 10 * model.independent_term[constraint - 1]
#
#     return constraint_value
#
#
# def inequality_constraint_redundant_4(model,
#                                       constraint):
#     constraint_value = sum(
#         model.coefficient_matrix[constraint - 1][variable - 1] * model.continuous_variables[variable] for variable in
#         model.indexes_continuous_variables) <= 20 * model.independent_term[constraint - 1]
#
#     return constraint_value
#
#
# def inequality_constraint_redundant_5(model,
#                                       constraint):
#     constraint_value = sum(
#         model.coefficient_matrix[constraint - 1][variable - 1] * model.continuous_variables[variable] for variable in
#         model.indexes_continuous_variables) <= 25 * model.independent_term[constraint - 1]
#
#     return constraint_value
#
#
# def inequality_constraint_redundant_6(model,
#                                       constraint):
#     constraint_value = sum(
#         model.coefficient_matrix[constraint - 1][variable - 1] * model.continuous_variables[variable] for variable in
#         model.indexes_continuous_variables) <= 30 * model.independent_term[constraint - 1]
#
#     return constraint_value
