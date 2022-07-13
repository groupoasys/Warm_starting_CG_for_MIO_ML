import pandas as pd

import My_project.error_handling as error


def extract_info_from_solution_UC_problem(optimal_UC_model,
                                          known_congestion_flag):
    flow_all_lines = extract_flow_from_UC_model(optimal_UC_model=optimal_UC_model)
    load_shedding_all_time_periods_and_nodes = extract_load_shedding_from_UC_model(optimal_UC_model=optimal_UC_model)

    if known_congestion_flag:
        error.my_custom_error(
            'Please, code this part. The congestion lines should correspond to the dataframe from the csv file which finishes with data_and_labels')

    else:
        congestion_all_lines = extract_congestion_lines_from_flow(flow_all_lines=flow_all_lines,
                                                                  optimal_UC_model=optimal_UC_model)

    power_generation = extract_power_generation_from_UC_model(optimal_UC_model=optimal_UC_model)
    return (flow_all_lines,
            load_shedding_all_time_periods_and_nodes,
            congestion_all_lines,
            power_generation)


def extract_power_generation_from_UC_model(optimal_UC_model):
    power_generation = [
        [round(optimal_UC_model.generations[time_period, generator].value, ndigits=2) for time_period in
         optimal_UC_model.indexes_time_periods] for generator in optimal_UC_model.indexes_generators]
    power_generation = pd.DataFrame(power_generation).T
    generators_column_names = get_generators_column_names(power_generation=power_generation)
    power_generation.columns = generators_column_names
    return power_generation


def get_generators_column_names(power_generation):
    number_of_generators = power_generation.shape[1]
    generators_column_names = []
    for generator in range(number_of_generators):
        generators_column_names.append('g' + str(generator + 1))
    return generators_column_names


def extract_congestion_lines_from_flow(flow_all_lines,
                                       optimal_UC_model):
    number_of_lines = flow_all_lines.shape[1]
    range_lines = range(1, (number_of_lines + 1))
    columns_congested_lines_dataframe = ['l' + str(line) for line in range_lines]
    congestion_lines = pd.DataFrame(index=flow_all_lines.index,
                                    columns=columns_congested_lines_dataframe)
    for line in range_lines:
        congestion_lines.iloc[:, line - 1] = (
                abs(flow_all_lines.iloc[:, line - 1]) == optimal_UC_model.bounds_flow.iloc[line - 1]).astype(int)
    congestion_lines = congestion_lines.replace(to_replace=0, value=-1)
    return congestion_lines


def extract_load_shedding_from_UC_model(optimal_UC_model):
    load_shedding_all_time_periods_and_nodes = [
        [optimal_UC_model.demand.iloc[time_period - 1, node - 1] - optimal_UC_model.demand_variables[
            time_period, node].value
         for node in optimal_UC_model.indexes_nodes] for time_period in optimal_UC_model.indexes_time_periods]
    load_shedding_all_time_periods_and_nodes = pd.DataFrame(load_shedding_all_time_periods_and_nodes)
    node_column_names = get_nodes_column_names(load_shedding_all_time_periods_and_nodes)
    load_shedding_all_time_periods_and_nodes.columns = node_column_names
    return load_shedding_all_time_periods_and_nodes


def get_nodes_column_names(load_shedding_all_time_periods_and_nodes):
    number_of_nodes = load_shedding_all_time_periods_and_nodes.shape[1]
    node_column_names = []
    for node in range(number_of_nodes):
        node_column_names.append('n' + str(node + 1))
    return node_column_names


def extract_flow_from_UC_model(optimal_UC_model):
    flow_all_lines = [
        [round(optimal_UC_model.flow_lower_limit_constraint[time_period, line].body(), ndigits=2) for time_period in
         optimal_UC_model.indexes_time_periods] for line in optimal_UC_model.indexes_lines]
    flow_all_lines = pd.DataFrame(flow_all_lines).T
    flow_column_names = get_flow_column_names(flow_all_lines=flow_all_lines)
    flow_all_lines.columns = flow_column_names
    return flow_all_lines


def get_flow_column_names(flow_all_lines):
    number_of_lines = flow_all_lines.shape[1]
    flow_column_names = []
    for line in range(number_of_lines):
        flow_column_names.append('fl' + str(line + 1))
    return flow_column_names


def write_csv_file_info_from_solution_UC_problem(dataset_file,
                                                 flow_all_lines,
                                                 indexes_time_periods,
                                                 load_shedding_all_time_periods_and_nodes,
                                                 data_and_wind,
                                                 congestion_all_lines,
                                                 line_to_be_studied,
                                                 power_generation):
    write_flow_in_csv_file(dataset_file=dataset_file,
                           flow_all_lines=flow_all_lines,
                           indexes_time_periods=indexes_time_periods)

    write_load_shedding_in_csv_file(dataset_file=dataset_file,
                                    indexes_time_periods=indexes_time_periods,
                                    load_shedding_all_time_periods_and_nodes=load_shedding_all_time_periods_and_nodes)

    write_data_and_labels_in_csv_file(congestion_all_lines=congestion_all_lines,
                                      data_and_wind=data_and_wind,
                                      dataset_file=dataset_file)
    write_data_and_labels_line_to_be_studied_in_csv_file(congestion_all_lines=congestion_all_lines,
                                                         data_and_wind=data_and_wind,
                                                         dataset_file=dataset_file,
                                                         line_to_be_studied=line_to_be_studied)

    write_power_generation_in_csv_file(dataset_file=dataset_file,
                                       power_generation=power_generation,
                                       indexes_time_periods=indexes_time_periods)
    return 0


def write_data_and_labels_line_to_be_studied_in_csv_file(congestion_all_lines,
                                                         data_and_wind,
                                                         dataset_file,
                                                         line_to_be_studied):
    data_and_labels_line_to_be_studied_file = '../' + dataset_file.strip(".xslx") + '_data_and_labels_line_' + str(
        line_to_be_studied) + '.csv'
    pd.concat([data_and_wind, congestion_all_lines.iloc[:, line_to_be_studied - 1]], axis=1).to_csv(
        data_and_labels_line_to_be_studied_file, sep=';')
    return 0


def write_data_and_labels_in_csv_file(congestion_all_lines,
                                      data_and_wind,
                                      dataset_file):
    data_and_labels_file = '../' + dataset_file.strip(".xslx") + '_data_and_labels.csv'
    pd.concat([data_and_wind, congestion_all_lines], axis=1).to_csv(data_and_labels_file, sep=';')
    return 0


def write_load_shedding_in_csv_file(dataset_file,
                                    indexes_time_periods,
                                    load_shedding_all_time_periods_and_nodes):
    load_shedding_all_time_periods_and_nodes_file = '../' + dataset_file.strip(
        ".xslx") + '_load_shedding_all_nodes_' + str(
        indexes_time_periods['start']) + '_' + str(indexes_time_periods['end']) + '.csv'
    load_shedding_all_time_periods_and_nodes.to_csv(load_shedding_all_time_periods_and_nodes_file, sep=";")

    return 0


def write_flow_in_csv_file(dataset_file,
                           flow_all_lines,
                           indexes_time_periods):
    flow_all_lines_file = '../' + dataset_file.strip(".xslx") + '_flow_all_lines_' + str(
        indexes_time_periods['start']) + '_' + str(indexes_time_periods['end']) + '.csv'
    flow_all_lines.to_csv(flow_all_lines_file, sep=";")

    return 0


def write_power_generation_in_csv_file(dataset_file,
                                       power_generation,
                                       indexes_time_periods):
    power_generation_file = '../' + dataset_file.strip(".xslx") + '_power_generation_' + str(
        indexes_time_periods['start']) + '_' + str(indexes_time_periods['end']) + '.csv'
    power_generation.to_csv(power_generation_file, sep=";")

    return 0
