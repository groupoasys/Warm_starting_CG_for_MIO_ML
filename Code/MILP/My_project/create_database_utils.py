import pandas as pd


def extract_data_from_csv(data_folder,
                          particular_folder_results):
    coefficient_matrix = pd.read_csv(data_folder + particular_folder_results + '/coefficient_matrix.csv', sep=';',
                                     index_col=0)
    costs = pd.read_csv(data_folder + particular_folder_results + '/costs.csv', sep=';', index_col=0)
    independent_term = pd.read_csv(data_folder + particular_folder_results + '/independent_term.csv', sep=';',
                                   index_col=0)
    lower_bound_continuous_variables = pd.read_csv(
        data_folder + particular_folder_results + '/lower_bound_continuous_variables.csv', sep=';', index_col=0)
    upper_bound_continuous_variables = pd.read_csv(
        data_folder + particular_folder_results + '/upper_bound_continuous_variables.csv', sep=';', index_col=0)
    return (coefficient_matrix,
            costs,
            independent_term,
            lower_bound_continuous_variables,
            upper_bound_continuous_variables)


def create_columns_status_constraints_general_MILP(number_of_constraints):
    beginning_columns_status_constraints = define_beginning_status_constraints()
    total_number_of_constraints = define_total_number_of_constraints_general_MILP(
        number_of_constraints=number_of_constraints)
    columns_status_constraints = [beginning_columns_status_constraints + str(constraint) for constraint in
                                  range(1, total_number_of_constraints + 1)]
    return columns_status_constraints


def create_columns_elapsed_time():
    columns_elapsed_time = {'user_time': 'user time (s)',
                            'time': 'time (s)',
                            'elapsed_time': 'elapsed time (s)'}
    columns_elapsed_time = list(columns_elapsed_time.values())
    return columns_elapsed_time


def create_columns_computational_complexity():
    columns_computational_complexity = {'ticks': 'ticks',
                                        'iterations': 'iterations'}
    columns_computational_complexity = list(columns_computational_complexity.values())

    return columns_computational_complexity


def create_columns_objective_value():
    columns_objective_value = {'whole_objective_value': 'obj. value',
                               'first_term_objective_value': 'first term obj. value',
                               'second_term_objective_value': 'second term obj. value',
                               'second_term_objective_value_no_penalization': 'second term obj. value no penal.'}
    columns_objective_value = list(columns_objective_value.values())
    return columns_objective_value


def create_columns_objective_value_general_MILP():
    columns_objective_value = {'whole_objective_value': 'obj. value'}
    columns_objective_value = list(columns_objective_value.values())
    return columns_objective_value


def create_columns_gap():
    columns_gap = {'absolute_gap': 'abs. gap',
                   'relative_gap': 'rel. gap'}
    columns_gap = list(columns_gap.values())
    return columns_gap


def create_columns_termination_condition():
    columns_termination_condition = {'termination_condition': 'term. cond.'}
    columns_termination_condition = list(columns_termination_condition.values())
    return columns_termination_condition


def create_columns_nonzeros():
    columns_nonzeros = {'number_nonzeros': '# nonzeros'}
    return columns_nonzeros


def create_columns_subproblems():
    columns_subproblems = {'number_bounded_subproblems': '# bounded subp.',
                           'number_created_subproblems': '# created subp.'}
    return columns_subproblems


def update_performance_number_of_nonzeros(individual_time_period,
                                          nonzeros_dataframe,
                                          solution):
    number_of_nonzeros = solution['Problem'][0]['Number of nonzeros']
    nonzeros_dataframe.loc[individual_time_period].iloc[0] = number_of_nonzeros

    return nonzeros_dataframe


def update_performance_number_subproblems(individual_time_period,
                                          subproblems_dataframe,
                                          solution):
    number_of_bounded_subproblems = solution['Solver'][0]['Statistics']['Branch and bound'][
        'Number of bounded subproblems']
    subproblems_dataframe.loc[individual_time_period].iloc[0] = number_of_bounded_subproblems
    number_of_created_subproblems = solution['Solver'][0]['Statistics']['Branch and bound'][
        'Number of created subproblems']
    subproblems_dataframe.loc[individual_time_period].iloc[1] = number_of_created_subproblems
    return subproblems_dataframe


def update_computational_complexity_dataframe(solution,
                                              individual_time_period,
                                              computational_complexity_dataframe):
    ticks = solution['custom']['ticks']
    iterations = solution['custom']['iterations']

    computational_complexity_dataframe.loc[individual_time_period].iloc[0] = ticks
    computational_complexity_dataframe.loc[individual_time_period].iloc[1] = iterations

    return computational_complexity_dataframe


def define_beginning_status_constraints():
    beginning_columns_status_constraints = 'act_label_orig_opt_problem_c'
    return beginning_columns_status_constraints


def define_total_number_of_constraints(number_of_lines):
    # Here we assume that we focus just on the flow constraints.
    total_number_of_constraints = 2 * number_of_lines
    return total_number_of_constraints


def define_total_number_of_constraints_general_MILP(number_of_constraints):
    total_number_of_constraints = number_of_constraints
    return total_number_of_constraints


def update_activation_status_constraints(activation_constraint_status,
                                         bounds_flow,
                                         individual_time_period,
                                         multi_period_load_shedding_quadratic_cost_UC_model,
                                         number_of_lines,
                                         tolerance=1e-5):
    # Here we just focus on the lower and upper limit constraints
    for line in range(number_of_lines):
        if abs(multi_period_load_shedding_quadratic_cost_UC_model.flow_lower_limit_constraint[1, line + 1].body() - (
                -bounds_flow[line])) <= tolerance:
            activation_constraint_status.loc[individual_time_period].iloc[line] = 1
        else:
            activation_constraint_status.loc[individual_time_period].iloc[line] = -1
    for line in range(number_of_lines):
        if abs(multi_period_load_shedding_quadratic_cost_UC_model.flow_upper_limit_constraint[1, line + 1].body() -
               bounds_flow[line]) <= tolerance:
            activation_constraint_status.loc[individual_time_period].iloc[number_of_lines + line] = 1
        else:
            activation_constraint_status.loc[individual_time_period].iloc[number_of_lines + line] = -1
    return activation_constraint_status


def update_activation_status_constraints_CVRP(activation_constraint_status,
                                              individual_time_period,
                                              model,
                                              range_customers_and_depot,
                                              tolerance=1e-5):
    # Here we just focus on the lower and upper limit constraints
    index_constraint = -1
    for customer_or_depot_1 in range_customers_and_depot:
        for customer_or_depot_2 in range_customers_and_depot:
            # print([customer_or_depot_1, customer_or_depot_2])
            index_constraint += 1
            if int(model.assignment[customer_or_depot_1, customer_or_depot_2].value) == 0:
                activation_constraint_status.loc[individual_time_period].iloc[index_constraint] = -1
            else:
                body_constraint = model.lower_bound_flow_constraint[customer_or_depot_1, customer_or_depot_2].body()
                lower_bound_constraint = model.lower_bound_flow_constraint[
                    customer_or_depot_1, customer_or_depot_2].lower()

                # print(index_constraint)
                if abs(body_constraint - lower_bound_constraint) <= tolerance:
                    activation_constraint_status.loc[individual_time_period].iloc[index_constraint] = 1
                else:
                    activation_constraint_status.loc[individual_time_period].iloc[index_constraint] = -1
    index_constraint = -1
    for customer_or_depot_1 in range_customers_and_depot:
        for customer_or_depot_2 in range_customers_and_depot:
            body_constraint = model.upper_bound_flow_constraint[customer_or_depot_1, customer_or_depot_2].body()
            upper_bound_constraint = model.upper_bound_flow_constraint[customer_or_depot_1, customer_or_depot_2].upper()
            index_constraint += 1
            squared_number_of_customers_and_depot = len(range_customers_and_depot) ** 2
            if abs(body_constraint - upper_bound_constraint) <= tolerance:
                activation_constraint_status.loc[individual_time_period].iloc[
                    squared_number_of_customers_and_depot + index_constraint] = 1
            else:
                activation_constraint_status.loc[individual_time_period].iloc[
                    squared_number_of_customers_and_depot + index_constraint] = -1
    return activation_constraint_status


def update_activation_status_constraints_general_MILP(activation_constraint_status,
                                                      individual_time_period,
                                                      model,
                                                      range_constraints,
                                                      tolerance=1e-4):
    for constraint in range_constraints:
        body_constraint = model.inequality_constraint[constraint].body()
        upper_bound_constraint = model.inequality_constraint[constraint].upper()
        if abs(body_constraint - upper_bound_constraint) <= tolerance:
            activation_constraint_status.loc[individual_time_period].iloc[constraint - 1] = 1
        else:
            activation_constraint_status.loc[individual_time_period].iloc[constraint - 1] = -1

    return activation_constraint_status


def update_termination_condition_dataframe(individual_time_period,
                                           termination_condition_dataframe,
                                           solution):
    termination_condition_dataframe.loc[individual_time_period].iloc[0] = solution.solver(
        0).termination_condition.value

    return termination_condition_dataframe


def update_elapsed_time_dataframe(elapsed_time_dataframe,
                                  user_time,
                                  individual_time_period,
                                  time,
                                  elapsed_time):
    elapsed_time_dataframe.loc[individual_time_period].iloc[0] = user_time
    elapsed_time_dataframe.loc[individual_time_period].iloc[1] = time
    elapsed_time_dataframe.loc[individual_time_period].iloc[2] = elapsed_time

    return elapsed_time_dataframe


def update_objective_value_dataframe_CVRP(individual_time_period,
                                          model,
                                          objective_value_dataframe):
    objective_value = model.objective_function()
    objective_value_dataframe.loc[individual_time_period].iloc[0] = objective_value

    return objective_value_dataframe


def update_objective_value_dataframe(individual_time_period,
                                     model,
                                     objective_value_dataframe):
    demand_variables = extract_demand_variables_from_optimal_problem(model=model)

    second_term_without_penalization = (model.demand - demand_variables).sum(axis=1).values[0]
    second_term = second_term_without_penalization * model.load_shedding_penalization_constant
    objective_value = model.objective_function()
    first_term = objective_value - second_term

    objective_value_dataframe.loc[individual_time_period].iloc[0] = objective_value
    objective_value_dataframe.loc[individual_time_period].iloc[1] = first_term
    objective_value_dataframe.loc[individual_time_period].iloc[2] = second_term
    objective_value_dataframe.loc[individual_time_period].iloc[3] = second_term_without_penalization

    return objective_value_dataframe


def extract_demand_variables_from_optimal_problem(model):
    demand_variables = pd.DataFrame(index=model.demand.index,
                                    columns=model.demand.columns)
    for node in range(len(demand_variables.columns)):
        demand_variables.iloc[0, node] = model.demand_variables[1, node + 1].value
    return demand_variables


def update_gap_dataframe(gap_dataframe,
                         model,
                         solution,
                         individual_time_period):
    absolute_gap = solution.solution(0).gap
    objective_value = model.objective_function.expr()
    if objective_value != 0:
        relative_gap = 100 * (solution.solution.gap / objective_value)
    else:
        relative_gap = 0.0
    gap_dataframe.loc[individual_time_period].iloc[0] = absolute_gap
    gap_dataframe.loc[individual_time_period].iloc[1] = relative_gap
    return gap_dataframe
