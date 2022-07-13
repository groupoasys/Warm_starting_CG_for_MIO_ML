import numpy as np
import pandas as pd


def deactivate_constraints_general_MILP(model,
                                        non_active_constraints):
    for constraint in non_active_constraints:
        model.inequality_constraint[constraint].deactivate()
    return model


def deactivate_constraints_UC(model,
                              non_active_constraints,
                              number_of_lines):
    for constraint in non_active_constraints:
        if constraint <= number_of_lines:
            # Since the model is only solved with one time period, the first index of the constraint should be always one. However, note that the demand and wind values are taken according to the index given by individual_time_period
            model.flow_lower_limit_constraint[1, constraint].deactivate()
        else:
            model.flow_upper_limit_constraint[1, constraint - number_of_lines].deactivate()
    return model


def get_labels_constraints_per_time_period(coefficients_and_labels,
                                           columns_status_constraints,
                                           individual_time_period):
    labels_constraints_per_time_period = coefficients_and_labels.loc[:, columns_status_constraints]
    labels_constraints_per_time_period = labels_constraints_per_time_period.loc[
        individual_time_period].values.tolist()
    return labels_constraints_per_time_period


def identify_violated_constraints_general_MILP(model,
                                               non_active_constraints,
                                               tolerance=1e-5):
    violated_constraints_flag = []
    infeasibility_constraints_values = []
    identifier_violated_constraints = []
    for constraint in non_active_constraints:
        upper_bound_constraint = model.inequality_constraint[constraint].upper()
        body_constraint = model.inequality_constraint[constraint].body()
        difference_body_and_upper_bound_constraint = body_constraint - upper_bound_constraint
        if difference_body_and_upper_bound_constraint > tolerance:
            violated_constraints_flag.append(True)
            infeasibility_constraints_values.append(abs(difference_body_and_upper_bound_constraint))
            identifier_violated_constraints.append(constraint)
        else:
            violated_constraints_flag.append(False)

    return (identifier_violated_constraints,
            infeasibility_constraints_values,
            violated_constraints_flag)


def update_database_including_violated_constraints(columns_status_constraints,
                                                   columns_flag_violated_constraints,
                                                   identifier_violated_constraints,
                                                   individual_time_period,
                                                   infeasibility_constraints_values,
                                                   infeasibility_flag,
                                                   updated_coefficients_and_labels,
                                                   violated_constraints_flag,
                                                   violated_constraints_flag_dataframe,
                                                   counter):
    if sum(violated_constraints_flag) == 0:
        infeasibility_flag = False
    else:
        indexes_violated_constraints_sorted_by_infeasibility_values = [constraint for _, constraint in sorted(
            zip(infeasibility_constraints_values, identifier_violated_constraints), reverse=True)]
        identifier_most_infeasible_constraint = indexes_violated_constraints_sorted_by_infeasibility_values[0]
        print("Most violated constraint = " + str(identifier_most_infeasible_constraint))
        updated_coefficients_and_labels.loc[
            individual_time_period, columns_status_constraints[identifier_most_infeasible_constraint - 1]] = 1
        violated_constraints_flag_dataframe.loc[
            individual_time_period, columns_flag_violated_constraints[identifier_most_infeasible_constraint - 1]] = True
        counter += 1
    return (updated_coefficients_and_labels,
            infeasibility_flag,
            violated_constraints_flag_dataframe,
            counter)


def get_performance_results(CG_time,
                            columns_status_constraints,
                            constraint_generation_time,
                            constraints_generation_counter,
                            counter,
                            elapsed_time,
                            elapsed_time_final_MILP,
                            individual_time_period,
                            model,
                            number_of_constraints,
                            number_of_constraints_final_MILP,
                            objective_value_final_MILP,
                            solution,
                            updated_coefficients_and_labels,
                            user_time_final_MILP,
                            CG_time_solve_model=-1,
                            constraint_generation_time_solve_model=pd.DataFrame()):
    labels_constraints_per_time_period = get_labels_constraints_per_time_period(
        coefficients_and_labels=updated_coefficients_and_labels,
        columns_status_constraints=columns_status_constraints,
        individual_time_period=individual_time_period)
    non_active_constraints = (np.where(np.array(labels_constraints_per_time_period) != 1)[0] + 1).tolist()
    constraint_generation_time.loc[individual_time_period, :] = CG_time
    constraint_generation_time_solve_model.loc[individual_time_period, :] = CG_time_solve_model
    constraints_generation_counter.loc[individual_time_period, :] = counter
    number_of_constraints_final_MILP.loc[individual_time_period, :] = number_of_constraints - len(
        non_active_constraints)
    objective_value_final_MILP.loc[individual_time_period, :] = model.objective_function()
    user_time_final_MILP.loc[individual_time_period, :] = solution.solver.user_time
    elapsed_time_final_MILP.loc[individual_time_period, :] = elapsed_time
    return (constraint_generation_time,
            constraint_generation_time_solve_model,
            constraints_generation_counter,
            number_of_constraints_final_MILP,
            objective_value_final_MILP,
            user_time_final_MILP,
            elapsed_time_final_MILP)


def identify_violated_constraints_UC(model,
                                     non_active_constraints,
                                     number_of_lines):
    violated_constraints_flag = []
    infeasibility_constraints_values = []
    identifier_violated_constraints = []
    for constraint in non_active_constraints:
        if constraint <= number_of_lines:
            # Since the model is only solved with one time period, the first index of the constraint should be always one. However, note that the demand and wind values are taken according to the index given by individual_time_period
            lower_bound_constraint = model.flow_lower_limit_constraint[1, constraint].lower()
            body_constraint = model.flow_lower_limit_constraint[1, constraint].body()
            difference_body_and_lower_bound_constraint = body_constraint - lower_bound_constraint
            if difference_body_and_lower_bound_constraint < 0:
                violated_constraints_flag.append(True)
                infeasibility_constraints_values.append(100 * (
                        abs(difference_body_and_lower_bound_constraint) / abs(
                    lower_bound_constraint)))  # We measure the infeasibility in terms of the relative errors
                identifier_violated_constraints.append(constraint)
            else:
                violated_constraints_flag.append(False)

        else:
            # Since the model is only solved with one time period, the first index of the constraint should be always one. However, note that the demand and wind values are taken according to the index given by individual_time_period
            upper_bound_constraint = model.flow_upper_limit_constraint[1, constraint - number_of_lines].upper()
            body_constraint = model.flow_upper_limit_constraint[1, constraint - number_of_lines].body()
            difference_body_and_upper_bound_constraint = body_constraint - upper_bound_constraint
            if difference_body_and_upper_bound_constraint > 0:
                violated_constraints_flag.append(True)
                infeasibility_constraints_values.append(
                    100 * (abs(difference_body_and_upper_bound_constraint) / abs(upper_bound_constraint)))
                identifier_violated_constraints.append(constraint)
            else:
                violated_constraints_flag.append(False)
    return (identifier_violated_constraints,
            infeasibility_constraints_values,
            violated_constraints_flag)
