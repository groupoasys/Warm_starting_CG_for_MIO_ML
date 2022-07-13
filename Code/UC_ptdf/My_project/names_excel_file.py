def get_names_sheets_dataset_file():
    names_sheets_dataset_file = {'coefficients_info': 'coefficients_info',
                                 'generators_info': 'generators_info',
                                 'lines_info': 'lines_info',
                                 'general_info': 'general_info',
                                 'ptdf_info': 'ptdf_info'}
    return names_sheets_dataset_file


def get_beginning_names_columns_data():
    beginning_names_columns_data = {'demand': 'd',
                                    'wind': 'w'}
    return beginning_names_columns_data


def get_column_names_generators_info():
    column_names_generators_info = {'number_of_generator': '# gen',
                                    'number_of_node': '# bus',
                                    'cost_quadratic': 'cost_quadratic (€/Mwh)',
                                    'cost_linear': 'cost_linear (€/Mwh)',
                                    'minimum_power': 'Pmin (MW)',
                                    'maximum_power': 'Pmax (MW)'}

    return column_names_generators_info


def get_column_names_lines_info():
    column_names_lines_info = {'number_of_line': '# line',
                               'origin_node': 'from bus',
                               'end_node': 'to bus',
                               'susceptances': 'Suscep (MW)',
                               'maximum_flow': 'Pmax (MW)'}

    return column_names_lines_info


def get_column_names_general_info():
    column_names_general_info = {'line_to_be_studied': 'line_to_be_studied',
                                 'load_shedding_penalization_constant': 'load_shedding_penalization_constant'}

    return column_names_general_info


def get_names_excel_file():
    names_sheets_dataset_file = get_names_sheets_dataset_file()
    beginning_names_columns_data = get_beginning_names_columns_data()
    column_names_generators_info = get_column_names_generators_info()
    column_names_lines_info = get_column_names_lines_info()
    column_names_general_info = get_column_names_general_info()

    return (names_sheets_dataset_file,
            beginning_names_columns_data,
            column_names_generators_info,
            column_names_lines_info,
            column_names_general_info)
