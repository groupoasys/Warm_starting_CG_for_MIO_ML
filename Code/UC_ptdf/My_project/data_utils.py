import pandas as pd


def extract_problem_info_from_excel(dataset_file,
                                    names_sheets_dataset_file):
    data_and_labels = read_sheet_from_excel(dataset_file=dataset_file,
                                            sheet_name=names_sheets_dataset_file['data_and_labels'])
    generators_info = read_sheet_from_excel(dataset_file=dataset_file,
                                            sheet_name=names_sheets_dataset_file['generators_info'])
    lines_info = read_sheet_from_excel(dataset_file=dataset_file,
                                       sheet_name=names_sheets_dataset_file['lines_info'])
    general_info = read_sheet_from_excel(dataset_file=dataset_file,
                                         sheet_name=names_sheets_dataset_file['general_info'])

    return (data_and_labels,
            generators_info,
            lines_info,
            general_info)


def read_sheet_from_excel(dataset_file,
                          sheet_name):
    dataframe_from_excel = pd.read_excel(io=dataset_file,
                                         sheet_name=sheet_name)
    return dataframe_from_excel


def extract_problem_info_from_csv(dataset_file,
                                  names_sheets_dataset_file):
    (dataset_file_coefficients_info,
     dataset_file_generators_info,
     dataset_file_lines_info,
     dataset_file_general_info,
     dataset_file_ptdf_info) = get_dataset_file_name_csv_from_excel_file(dataset_file=dataset_file,
                                                                         names_sheets_dataset_file=names_sheets_dataset_file)

    coefficients_info = read_csv_sheet(csv_sheet=dataset_file_coefficients_info)
    generators_info = read_csv_sheet(csv_sheet=dataset_file_generators_info)
    lines_info = read_csv_sheet(csv_sheet=dataset_file_lines_info)
    general_info = read_csv_sheet(csv_sheet=dataset_file_general_info)
    ptdf_info = read_csv_sheet(csv_sheet=dataset_file_ptdf_info)
    return (coefficients_info,
            generators_info,
            lines_info,
            general_info,
            ptdf_info)


def read_csv_sheet(csv_sheet):
    dataframe_from_csv = pd.read_csv(filepath_or_buffer=csv_sheet,
                                     sep=';')
    if dataframe_from_csv.columns[0] == 'Unnamed: 0':
        dataframe_from_csv = pd.read_csv(filepath_or_buffer=csv_sheet,
                                         sep=';',
                                         index_col=0)
    return dataframe_from_csv


def get_dataset_file_name_csv_from_excel_file(dataset_file,
                                              names_sheets_dataset_file):
    dataset_file_coefficients_info = get_csv_file_name_per_sheet(dataset_file=dataset_file,
                                                                 sheet_name=names_sheets_dataset_file[
                                                                     'coefficients_info'])
    dataset_file_generators_info = get_csv_file_name_per_sheet(dataset_file=dataset_file,
                                                               sheet_name=names_sheets_dataset_file['generators_info'])
    dataset_file_lines_info = get_csv_file_name_per_sheet(dataset_file=dataset_file,
                                                          sheet_name=names_sheets_dataset_file['lines_info'])
    dataset_file_general_info = get_csv_file_name_per_sheet(dataset_file=dataset_file,
                                                            sheet_name=names_sheets_dataset_file['general_info'])

    dataset_file_ptdf_info = get_csv_file_name_per_sheet(dataset_file=dataset_file,
                                                         sheet_name=names_sheets_dataset_file['ptdf_info'])
    return (dataset_file_coefficients_info,
            dataset_file_generators_info,
            dataset_file_lines_info,
            dataset_file_general_info,
            dataset_file_ptdf_info)


def get_csv_file_name_per_sheet(dataset_file,
                                sheet_name):
    csv_file_per_sheet = '..' + dataset_file.strip("coefficients_info.csv") + '_' + sheet_name + ".csv"
    return csv_file_per_sheet


def update_indexes_time_periods_when_necessary(data_and_labels,
                                               indexes_time_periods):
    if indexes_time_periods == {}:
        indexes_time_periods = {'start': 0,
                                'end': data_and_labels.shape[0]}
    return indexes_time_periods
