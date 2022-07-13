import pandas as pd

def extract_UC_configuration(data_and_labels,
                             generators_info,
                             lines_info,
                             general_info,
                             beginning_names_columns_data,
                             column_names_generators_info,
                             column_names_lines_info,
                             column_names_general_info,
                             indexes_time_periods):
    number_of_nodes = get_number_of_nodes_from_lines_info(column_names_lines_info=column_names_lines_info,
                                                          lines_info=lines_info)
    demand = get_demand_from_data_and_labels(beginning_names_columns_data=beginning_names_columns_data,
                                             data_and_labels=data_and_labels,
                                             indexes_time_periods=indexes_time_periods,
                                             number_of_nodes=number_of_nodes)
    wind = data_and_labels.loc[indexes_time_periods['start']: indexes_time_periods['end'],
           (beginning_names_columns_data['wind'] + '1'):(beginning_names_columns_data['wind'] + str(number_of_nodes))]
    demand_and_wind = pd.concat([demand, wind], axis=1)
    #data_and_labels.transpose()[
    #     ~data_and_labels.transpose().apply(tuple, 1).isin(demand_and_wind.transpose().apply(tuple, 1))]
    # columns_lines = list(set(data_and_labels.columns).symmetric_difference(demand_and_wind.columns))
    # data_and_labels.transpose().merge(demand_and_wind.transpose(), how='inner', indicator=False)

    data_and_labels.loc[:, demand_and_wind.columns]

    costs = generators_info.loc[:, [column_names_generators_info['cost_quadratic'],
                                    column_names_generators_info['cost_linear']]].values.tolist()
    lower_bound_generators = generators_info[column_names_generators_info['minimum_power']]
    upper_bound_generators = generators_info[column_names_generators_info['maximum_power']]
    bounds_flow = lines_info[column_names_lines_info['maximum_flow']]
    number_of_generators = generators_info.shape[0]
    number_of_lines = lines_info.shape[0]
    load_shedding_penalization_constant = \
        general_info[column_names_general_info['load_shedding_penalization_constant']].values[0]
    susceptances = lines_info[column_names_lines_info['susceptances']].to_list()
    relationship_lines_nodes = lines_info[
        [column_names_lines_info['number_of_line'], column_names_lines_info['origin_node'],
         column_names_lines_info['end_node']]]
    column_names_dataframe_lines_info = column_names_lines_info
    column_names_dataframe_generators_info = column_names_generators_info
    relationship_generators_nodes = generators_info[
        [column_names_generators_info['number_of_generator'], column_names_generators_info['number_of_node']]]
    number_of_time_periods = indexes_time_periods['end'] - indexes_time_periods['start']

    return (demand,
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
            number_of_time_periods)


def get_demand_from_data_and_labels(beginning_names_columns_data,
                                    data_and_labels,
                                    indexes_time_periods,
                                    number_of_nodes):
    demand = data_and_labels.loc[indexes_time_periods['start']: indexes_time_periods['end'],
             (beginning_names_columns_data['demand'] + '1'):(
                     beginning_names_columns_data['demand'] + str(number_of_nodes))]
    return demand


def get_number_of_nodes_from_lines_info(column_names_lines_info,
                                        lines_info):
    number_of_nodes = lines_info[
        [column_names_lines_info['origin_node'], column_names_lines_info['end_node']]].max().max()
    return number_of_nodes
