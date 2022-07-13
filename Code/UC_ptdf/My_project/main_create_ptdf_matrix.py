import pandas as pd
import numpy as np
from dataclasses import dataclass


def get_ptdf_matrix(folder_data,
                    lines_info,
                    node_ref,
                    general_data_folder='Data/'):
    # lines_info = pd.read_csv('../' + general_data_folder + folder_data + '/UC_lines_info.csv', sep=';', index_col=0)
    slack_node = node_ref
    column_origin_bus = 'from bus'
    column_end_bus = 'to bus'
    column_susceptances = 'Suscep (MW)'
    number_of_lines = lines_info.shape[0]
    number_of_nodes = max(lines_info[column_origin_bus].max(), lines_info[column_end_bus].max())
    range_lines = range(1, number_of_lines + 1)
    range_nodes = range(1, number_of_nodes + 1)

    X = pd.DataFrame(0, index=range_lines, columns=range_lines)  # reactance matrix
    A = pd.DataFrame(0, index=range_nodes, columns=range_lines)  # incidence node line matrix
    B = pd.DataFrame(0, index=range_nodes, columns=range_nodes)  # admittance matrix

    for line in range_lines:
        susceptance = lines_info.loc[line, column_susceptances]
        X.loc[line, line] = 1 / susceptance

        origin_bus = lines_info.loc[line, column_origin_bus]
        end_bus = lines_info.loc[line, column_end_bus]
        A.loc[origin_bus, line] = 1
        A.loc[end_bus, line] = -1

    inverse_X = pd.DataFrame(np.linalg.pinv(X.values), X.columns, X.index)
    transpose_A = A.transpose()
    A_no_slack_node = A.drop(slack_node, axis=0)
    transpose_A_no_slack_node = A_no_slack_node.transpose()
    B = A.dot(inverse_X.dot(transpose_A))
    B_no_slack_node = B.drop(slack_node, axis=1)
    B_no_slack_node = B_no_slack_node.drop(slack_node, axis=0)

    inverse_B_no_slack_node = pd.DataFrame(np.linalg.pinv(B_no_slack_node.values), B_no_slack_node.columns,
                                           B_no_slack_node.index)

    ptdf_matrix = (inverse_X.dot(transpose_A_no_slack_node)).dot(inverse_B_no_slack_node)
    if slack_node == number_of_nodes:
        ptdf_matrix.loc[:, slack_node] = 0
    else:
        ptdf_matrix.insert(slack_node - 1, slack_node, 0)

    ptdf_matrix.to_csv('../' + general_data_folder + folder_data + '/UC_ptdf_info.csv', sep=';')
    # B.to_csv('../' + general_data_folder + folder_data + '/B.csv', sep=';')
    # C.to_csv('../' + general_data_folder + folder_data + '/C.csv', sep=';')
    return ptdf_matrix


def ptdf_matrix_Alvaro(lines,
                       n_nodes,
                       node_ref):
    list_nodes = list(range(1, n_nodes + 1))

    X = pd.DataFrame(0, index=lines.index, columns=lines.index)  # Diagonal matrix of branch reactances
    B = pd.DataFrame(0, index=list_nodes, columns=list_nodes)  # B is the Img of Admitance matrix
    A = pd.DataFrame(0, index=lines.index, columns=list_nodes)  # Incidence matrix

    column_origin_bus = 'from bus'
    column_end_bus = 'to bus'
    column_susceptances = 'Suscep (MW)'

    for l in lines.index:
        X.loc[l, l] = 1 / lines.loc[l, column_susceptances]
        from_bus = lines.loc[l, column_origin_bus]
        to_bus = lines.loc[l, column_end_bus]
        A.loc[l, from_bus] = 1
        A.loc[l, to_bus] = -1

    for n in list_nodes:
        node_list = lines[lines.loc[:, column_origin_bus] == n].loc[:, column_end_bus].to_list()
        line_susc = lines[lines.loc[:, column_origin_bus] == n].loc[:, column_susceptances].to_list()
        node_list += lines[lines.loc[:, column_end_bus] == n].loc[:, column_origin_bus].to_list()
        line_susc += lines[lines.loc[:, column_end_bus] == n].loc[:, column_susceptances].to_list()

        B.loc[n, n] = sum(line_susc[i] for i in range(len(node_list)))
        for i in range(len(node_list)):
            B.loc[n, node_list[i]] = -line_susc[i]

    # Convert to matrix
    B = B.drop(index=node_ref)
    B = B.drop(columns=[node_ref], axis=1)
    A = A.drop(columns=[node_ref], axis=1)

    X_m = X.values
    B_m = B.values
    A_m = A.values

    S_f = np.dot(np.linalg.inv(X_m), np.dot(A_m, np.linalg.inv(B_m)))
    list_nodes.remove(node_ref)
    PTDF = pd.DataFrame(S_f, index=lines.index, columns=list_nodes)
    PTDF.to_csv('../Data/UC_ptdf/UC_ptdf_info_Alvaro.csv', sep=';')
    # pd.DataFrame(X_m).to_csv('../Data/UC_ptdf/B_Alvaro.csv', sep=';')
    # pd.DataFrame(B_m).to_csv('../Data/UC_ptdf/C_Alvaro.csv', sep=';')

    return PTDF


@dataclass
class Labels:
    from_bus: str = 'from bus'
    to_bus: str = 'to bus'
    impedance: str = 'Z'
    resistance: str = 'R'
    reactance: str = 'X'
    admittance: str = 'Y'
    conductance: str = 'G'
    susceptance: str = 'Suscep (MW)'
    capacity: str = 'C'
    shunt_susceptance: str = 'b_shunt'


def build_admittance_matrix(input_data, ref_node=None):
    """Computes the B matrix. It assumes pandas DataFrame input of the form:
    index, from bus, to bus, X
    2,     101,      102,    0.013
    17,    101,      104,    0.015
    where the index of the DataFrame is the index of each line (row).
    """

    input_data = input_data.copy()
    line_index = list(input_data.index)
    columns = input_data.columns

    # Checks
    if Labels.reactance in columns and Labels.susceptance in columns:
        raise ValueError('X and B was specified, erase one to compute the matrix.\n'
                         'Rename B as b_shunt if B refers to shunt susceptance.')
    elif Labels.reactance in columns:
        mode = 'from_impedance'
        try:
            input_data[Labels.resistance]
        except KeyError:
            input_data[Labels.resistance] = 0
    elif Labels.susceptance in columns:
        mode = 'from_admittance'
        try:
            input_data[Labels.conductance]
        except KeyError:
            input_data[Labels.conductance] = 0
    else:
        raise ValueError('Neither reactance nor susceptance was indicated. ')

    if len(line_index) != len(set(line_index)):
        raise ValueError('There are two lines with the same index.')

    if ref_node is not None:
        ref_node = int(ref_node)

    from_set = set(list(input_data[Labels.from_bus].values))
    to_set = set(list(input_data[Labels.to_bus].values))
    node_set = from_set.union(to_set)
    n_nodes = len(node_set)

    B_N = pd.DataFrame(np.zeros((n_nodes, n_nodes)), index=node_set, columns=node_set)
    G_N = pd.DataFrame(np.zeros((n_nodes, n_nodes)), index=node_set, columns=node_set)

    # Off-diagonal elements B-matrix
    for i in line_index:
        from_bus = input_data.at[i, Labels.from_bus]
        to_bus = input_data.at[i, Labels.to_bus]
        if mode == 'from_impedance':
            r_i = input_data.at[i, Labels.resistance]
            x_i = input_data.at[i, Labels.reactance]
            # G-matrix
            G_N.at[from_bus, to_bus] = -1 * (r_i / (r_i ** 2 + x_i ** 2))
            G_N.at[to_bus, from_bus] = -1 * (r_i / (r_i ** 2 + x_i ** 2))
            # B-matrix
            B_N.at[from_bus, to_bus] = -1 * (x_i / (r_i ** 2 + x_i ** 2))
            B_N.at[to_bus, from_bus] = -1 * (x_i / (r_i ** 2 + x_i ** 2))
        elif mode == 'from_admittance':
            g_i = input_data.at[i, Labels.conductance]
            b_i = input_data.at[i, Labels.susceptance]
            # G-matrix
            G_N.at[from_bus, to_bus] = -1 * g_i
            G_N.at[to_bus, from_bus] = -1 * g_i
            # B-matrix
            B_N.at[from_bus, to_bus] = -1 * b_i
            B_N.at[to_bus, from_bus] = -1 * b_i

    # Diagonal elements B-matrix
    for node in node_set:
        B_N.at[node, node] = -1 * sum(B_N.loc[node, :].values)
        G_N.at[node, node] = -1 * sum(G_N.loc[node, :].values)

    # Admittance shunt
    B_N = B_N + admittance_shunt_per_node(input_data)

    # Remove reference node
    if ref_node:
        B_N.drop(index=[ref_node], columns=[ref_node], inplace=True)
        G_N.drop(index=[ref_node], columns=[ref_node], inplace=True)

    Y_N = G_N - 1j * B_N

    return Y_N, G_N, B_N


def admittance_shunt_per_node(input_data):
    line_index = list(input_data.index)
    from_set = set(list(input_data[Labels.from_bus].values))
    to_set = set(list(input_data[Labels.to_bus].values))
    node_set = from_set.union(to_set)
    n_nodes = len(node_set)

    B_sh = pd.DataFrame(np.zeros((n_nodes, n_nodes)), index=node_set, columns=node_set)
    if Labels.shunt_susceptance in input_data.columns:
        for i in line_index:
            from_bus = input_data.at[i, Labels.from_bus]
            to_bus = input_data.at[i, Labels.to_bus]
            B_sh.at[from_bus, from_bus] += input_data.at[i, Labels.shunt_susceptance] / 2
            B_sh.at[to_bus, to_bus] += input_data.at[i, Labels.shunt_susceptance] / 2
    return B_sh


def susceptance_shunt_per_line(input_data):
    line_index = list(input_data.index)
    from_set = set(list(input_data[Labels.from_bus].values))
    to_set = set(list(input_data[Labels.to_bus].values))
    node_set = from_set.union(to_set)
    n_nodes = len(node_set)

    b = pd.DataFrame(np.zeros((n_nodes, n_nodes)), index=node_set, columns=node_set)
    if Labels.shunt_susceptance in input_data.columns:
        for i in line_index:
            from_bus = input_data.at[i, Labels.from_bus]
            to_bus = input_data.at[i, Labels.to_bus]
            b.at[from_bus, to_bus] = input_data.at[i, Labels.shunt_susceptance]
            b.at[to_bus, from_bus] = input_data.at[i, Labels.shunt_susceptance]
    return b


def compute_impedance_matrix(admittance_matrix=None, input_data=None, ref_node=None):
    if (admittance_matrix is None) and (input_data is None):
        raise ValueError('Either admittance matrix or input data is required.')
    if (input_data is not None) and (admittance_matrix is None):
        admittance_matrix, _, _ = build_admittance_matrix(input_data, ref_node)
    elif (admittance_matrix is not None) and (input_data is not None):
        print('Input data not used. Only admittance matrix is considered.')

    # Invert the admittance matrix
    impedance_matrix = pd.DataFrame(
        np.linalg.inv(admittance_matrix.values),
        index=admittance_matrix.index,
        columns=admittance_matrix.columns,
    )

    return impedance_matrix


def build_b_l_matrix(input_data, ref_node=None):
    """Computes the B_L matrix. It assumes pandas DataFrame input of the form:
    index, from bus, to bus, X
    2,     101,      102,    0.013
    17,    101,      104,    0.015
    where the index of the DataFrame is the index of each line (row).
    """

    input_data = input_data.copy()
    line_index = list(input_data.index)
    columns = input_data.columns

    # Checks
    if Labels.reactance in columns and Labels.susceptance in columns:
        raise ValueError('X and B was specified, erase one to compute the matrix.\n'
                         'Rename B as b_shunt if B refers to shunt susceptance.')
    elif Labels.reactance in columns:
        mode = 'from_impedance'
        try:
            input_data[Labels.resistance]
        except KeyError:
            input_data[Labels.resistance] = 0
    elif Labels.susceptance in columns:
        mode = 'from_admittance'
        try:
            input_data[Labels.conductance]
        except KeyError:
            input_data[Labels.conductance] = 0
    else:
        raise ValueError('Neither reactance nor susceptance was indicated. ')

    if len(line_index) != len(set(line_index)):
        raise ValueError('There are two lines with the same index.')

    if ref_node is not None:
        ref_node = int(ref_node)

    from_set = set(list(input_data[Labels.from_bus].values))
    to_set = set(list(input_data[Labels.to_bus].values))
    node_set = from_set.union(to_set)
    n_nodes = len(node_set)

    # B_L matrix
    B_L = pd.DataFrame(np.zeros((len(line_index), n_nodes)), index=line_index, columns=node_set)

    # Off-diagonal elements B-matrix

    for i in line_index:
        from_bus = input_data.at[i, Labels.from_bus]
        to_bus = input_data.at[i, Labels.to_bus]

        if mode == 'from_impedance':
            r_i = input_data.at[i, Labels.resistance]
            x_i = input_data.at[i, Labels.reactance]
            # B-matrix
            B_L.at[i, from_bus] = 1 * (x_i / (r_i ** 2 + x_i ** 2))
            B_L.at[i, to_bus] = -1 * (x_i / (r_i ** 2 + x_i ** 2))
        elif mode == 'from_admittance':
            g_i = input_data.at[i, Labels.conductance]
            b_i = input_data.at[i, Labels.susceptance]
            # B-matrix
            B_L.at[i, from_bus] = b_i
            B_L.at[i, to_bus] = -1 * b_i

    # Remove reference node

    if ref_node:
        B_L.drop(columns=[ref_node], inplace=True)

    return B_L


def compute_ptdf_matrix_JMA(input_data, ref_node=None):
    """Computes the PTDF matrix. It assumes pandas DataFrame input of the form:
    index, from bus, to bus, X
    2,     101,      102,    0.013
    17,    101,      104,    0.015
    where the index of the DataFrame is the index of each line (row).
    """

    input_data = input_data.copy()
    if ref_node is not None:
        ref_node = int(ref_node)

    _, _, B_NN = build_admittance_matrix(input_data, ref_node)
    B_LL = build_b_l_matrix(input_data, ref_node)
    # B_NN.to_csv('../Data/UC_ptdf/C_JMA.csv', sep=';')
    # B_LL.to_csv('../Data/UC_ptdf/B_JMA.csv', sep=';')

    PTDF_nrf = B_LL.values @ np.linalg.inv(B_NN.values)
    PTDF_nrf = pd.DataFrame(PTDF_nrf, index=B_LL.index, columns=B_LL.columns)
    PTDF_nrf.to_csv('../Data/UC_ptdf/UC_ptdf_info_JMA.csv', sep=';')

    return PTDF_nrf
