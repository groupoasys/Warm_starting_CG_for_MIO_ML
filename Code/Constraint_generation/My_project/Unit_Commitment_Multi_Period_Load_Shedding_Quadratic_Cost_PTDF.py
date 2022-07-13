import pyomo.environ as pe


def unit_commitment_multi_period_load_shedding_quadratic_cost_ptdf(demand,
                                                                   wind,
                                                                   costs,
                                                                   lower_bound_generators,
                                                                   upper_bound_generators,
                                                                   bounds_flow,
                                                                   number_of_generators,
                                                                   number_of_lines,
                                                                   number_of_nodes,
                                                                   load_shedding_penalization_constant,
                                                                   susceptances,
                                                                   relationship_lines_nodes,
                                                                   column_names_dataframe_lines_info,
                                                                   column_names_dataframe_generators_info,
                                                                   relationship_generators_nodes,
                                                                   number_of_time_periods,
                                                                   ptdf):
    model = pe.ConcreteModel("Unit_Commitment_Multi_Period_Load_Shedding_Quadratic_Cost")

    # Parameters

    model.demand = demand
    model.wind = wind
    model.costs = costs
    model.susceptances = susceptances
    model.lower_bound_generators = lower_bound_generators
    model.upper_bound_generators = upper_bound_generators
    model.number_of_generators = number_of_generators
    model.number_of_lines = number_of_lines
    model.number_of_nodes = number_of_nodes
    model.load_shedding_penalization_constant = load_shedding_penalization_constant
    model.relationship_lines_nodes = relationship_lines_nodes
    model.relationship_generators_nodes = relationship_generators_nodes
    model.column_names_dataframe_lines_info = column_names_dataframe_lines_info
    model.column_names_dataframe_generators_info = column_names_dataframe_generators_info
    model.bounds_flow = bounds_flow
    model.number_of_time_periods = number_of_time_periods
    model.ptdf = ptdf

    # Indexes
    model.indexes_generators = pe.RangeSet(model.number_of_generators)
    model.indexes_lines = pe.RangeSet(model.number_of_lines)
    model.indexes_nodes = pe.RangeSet(model.number_of_nodes)
    model.indexes_time_periods = pe.RangeSet(model.number_of_time_periods)

    # Variables

    model.generations = pe.Var(model.indexes_time_periods,
                               model.indexes_generators,
                               within=pe.NonNegativeReals)
    model.on_off_status_generators = pe.Var(model.indexes_time_periods,
                                            model.indexes_generators,
                                            within=pe.Binary)
    model.demand_variables = pe.Var(model.indexes_time_periods,
                                    model.indexes_nodes,
                                    within=pe.NonNegativeReals,
                                    bounds=bounds_rule_demand_variables)
    model.wind_variables = pe.Var(model.indexes_time_periods,
                                  model.indexes_nodes,
                                  within=pe.NonNegativeReals,
                                  bounds=bounds_rule_wind_variables)
    model.injections = pe.Var(model.indexes_time_periods,
                              model.indexes_nodes,
                              within=pe.Reals)
    model.flow = pe.Var(model.indexes_time_periods,
                        model.indexes_lines,
                        within=pe.Reals)

    # Objective Function
    model.objective_function = pe.Objective(rule=objective_function,
                                            sense=pe.minimize)
    # Constraints

    model.injections_constraint = pe.Constraint(model.indexes_time_periods,
                                                model.indexes_nodes,
                                                rule=injections_constraint)

    model.balance_constraint = pe.Constraint(model.indexes_time_periods,
                                             rule=balance_constraint)

    model.generation_upper_limit_constraint = pe.Constraint(model.indexes_time_periods,
                                                            model.indexes_generators,
                                                            rule=generation_upper_limit_constraint)

    model.generation_lower_limit_constraint = pe.Constraint(model.indexes_time_periods,
                                                            model.indexes_generators,
                                                            rule=generation_lower_limit_constraint)
    model.flow_constraint = pe.Constraint(model.indexes_time_periods,
                                          model.indexes_lines,
                                          rule=flow_constraint)
    model.flow_upper_limit_constraint = pe.Constraint(model.indexes_time_periods,
                                                      model.indexes_lines,
                                                      rule=flow_upper_limit_constraint)

    model.flow_lower_limit_constraint = pe.Constraint(model.indexes_time_periods,
                                                      model.indexes_lines,
                                                      rule=flow_lower_limit_constraint)

    return model


def bounds_rule_demand_variables(model,
                                 time_period,
                                 node):
    return (0, model.demand.iloc[time_period - 1, node - 1])


def bounds_rule_wind_variables(model,
                               time_period,
                               node):
    return (0, model.wind.iloc[time_period - 1, node - 1])


def objective_function(model):
    objective_value = sum(sum(
        model.costs[generator - 1][0] * model.generations[time_period, generator] * model.generations[
            time_period, generator] + model.costs[generator - 1][1] * model.generations[time_period, generator] for
        generator in model.indexes_generators) + model.load_shedding_penalization_constant * sum(
        (model.demand.iloc[time_period - 1, node - 1] - model.demand_variables[time_period, node]) for node in
        model.indexes_nodes) for time_period in model.indexes_time_periods)

    return objective_value


def injections_constraint(model,
                          time_period,
                          node):
    constraint_value = model.injections[time_period, node] == (
        sum(model.generations[time_period, generator] for generator in model.indexes_generators if
            model.relationship_generators_nodes[
                model.column_names_dataframe_generators_info['number_of_node']][
                generator - 1] == node)) + model.wind_variables[time_period, node] - \
                       model.demand_variables[time_period, node]  # + (
    # model.demand.iloc[time_period - 1, node - 1] - model.demand_variables[
    #   time_period, node])

    return constraint_value


def balance_constraint(model,
                       time_period):
    constraint_value = sum(model.injections[time_period, node] for node in model.indexes_nodes) == 0
    # column_name_origin_bus_line = model.column_names_dataframe_lines_info['origin_node']
    # column_name_end_bus_line = model.column_names_dataframe_lines_info['end_node']
    #
    # constraint_value = sum(model.susceptances[line - 1] * (
    #         model.phase_angles[time_period, model.relationship_lines_nodes[column_name_origin_bus_line][line - 1]] -
    #         model.phase_angles[time_period, model.relationship_lines_nodes[column_name_end_bus_line][
    #             line - 1]]) for line in model.indexes_lines if
    #                        model.relationship_lines_nodes[column_name_origin_bus_line][
    #                            line - 1] == node) - sum(model.susceptances[line - 1] * (
    #         model.phase_angles[time_period, model.relationship_lines_nodes[column_name_origin_bus_line][line - 1]] -
    #         model.phase_angles[time_period, model.relationship_lines_nodes[column_name_end_bus_line][
    #             line - 1]]) for line in model.indexes_lines if model.relationship_lines_nodes[column_name_end_bus_line][
    #                                                         line - 1] == node) == sum(
    #     model.generations[time_period, generator] for generator in model.indexes_generators if
    #     model.relationship_generators_nodes[model.column_names_dataframe_generators_info['number_of_node']][
    #         generator - 1] == node) + model.wind_variables[time_period, node] - model.demand_variables[
    #                        time_period, node]
    return constraint_value


def generation_upper_limit_constraint(model,
                                      time_period,
                                      generator):
    constraint_value = model.generations[time_period, generator] <= model.on_off_status_generators[
        time_period, generator] * model.upper_bound_generators[generator - 1]
    return constraint_value


def generation_lower_limit_constraint(model,
                                      time_period,
                                      generator):
    constraint_value = model.generations[time_period, generator] >= model.on_off_status_generators[
        time_period, generator] * model.lower_bound_generators[generator - 1]
    return constraint_value


def flow_constraint(model,
                    time_period,
                    line):
    constraint_value = model.flow[time_period, line] == sum(
        model.ptdf.iloc[line - 1, node - 1] * model.injections[time_period, node] for node in model.indexes_nodes)
    return constraint_value


def flow_upper_limit_constraint(model,
                                time_period,
                                line):
    constraint_value = model.flow[time_period, line] <= model.bounds_flow[line - 1]

    # constraint_value = (model.susceptances[line - 1] * (model.phase_angles[time_period, model.relationship_lines_nodes[
    #     model.column_names_dataframe_lines_info['origin_node']][line - 1]] - model.phase_angles[time_period,
    #                                                                                             model.relationship_lines_nodes[
    #                                                                                                 model.column_names_dataframe_lines_info[
    #                                                                                                     'end_node']][
    #                                                                                                 line - 1]])) <= \
    #                    model.bounds_flow[line - 1]
    return constraint_value


def flow_lower_limit_constraint(model,
                                time_period,
                                line):
    constraint_value = model.flow[time_period, line] >= -model.bounds_flow[line - 1]

    # constraint_value = (model.susceptances[line - 1] * (model.phase_angles[time_period, model.relationship_lines_nodes[
    #     model.column_names_dataframe_lines_info['origin_node']][line - 1]] - model.phase_angles[time_period,
    #                                                                                             model.relationship_lines_nodes[
    #                                                                                                 model.column_names_dataframe_lines_info[
    #                                                                                                     'end_node']][
    #                                                                                                 line - 1]])) >= - \
    #                        model.bounds_flow[
    #                            line - 1]
    return constraint_value


def slack_node_first_bus_constraint(model,
                                    time_period):
    constraint_value = model.phase_angles[time_period, 1] == 0
    return constraint_value
