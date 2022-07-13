import My_project as mp

import pandas as pd

folder_data = 'UC_ptdf'

n_nodes = 73
node_ref = 1
lines = pd.read_csv('../Data/' + folder_data + '/UC_lines_info.csv', sep=';', index_col=0)
#
# n_nodes = 3
# node_ref = 1
# lines = pd.read_csv('../Data/' + folder_data + '/3_nodes_example/UC_lines_info.csv', sep=';', index_col=0)

# n_nodes = 5
# node_ref = 5
# lines = pd.read_csv('../Data/' + folder_data + '/5_nodes_example/UC_lines_info.csv', sep=';', index_col=0)

ptdf_asun = mp.get_ptdf_matrix(folder_data=folder_data,
                               lines_info=lines,
                               node_ref=node_ref)

ptdf_alvaro = mp.ptdf_matrix_Alvaro(lines=lines,
                                    n_nodes=n_nodes,
                                    node_ref=node_ref)

ptdf_JMA = mp.compute_ptdf_matrix_JMA(input_data=lines,
                                      ref_node=node_ref)

aa = 0
