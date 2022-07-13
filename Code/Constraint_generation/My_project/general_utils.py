import os


def define_beginning_status_constraints():
    beginning_columns_status_constraints = 'act_label_orig_opt_problem_c'
    return beginning_columns_status_constraints


def create_directory_if_it_does_not_exists(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    return 0


def create_columns_status_constraints_general_MILP(number_of_constraints):
    beginning_columns_status_constraints = define_beginning_status_constraints()
    total_number_of_constraints = define_total_number_of_constraints_general_MILP(
        number_of_constraints=number_of_constraints)
    columns_status_constraints = [beginning_columns_status_constraints + str(constraint) for constraint in
                                  range(1, total_number_of_constraints + 1)]
    return columns_status_constraints


def define_total_number_of_constraints_general_MILP(number_of_constraints):
    total_number_of_constraints = number_of_constraints
    return total_number_of_constraints


def create_columns_flag_violated_constraints(number_of_constraints):
    beginning_column_name = define_beginning_flag_violated_constraints()
    total_number_of_constraints = define_total_number_of_constraints_general_MILP(
        number_of_constraints=number_of_constraints)
    columns_flag_violated_constraints = [beginning_column_name + str(constraint) for constraint in
                                         range(1, total_number_of_constraints + 1)]
    return columns_flag_violated_constraints


def define_beginning_flag_violated_constraints():
    beginning_columns_flag_violated_constraints = 'flag_viol_c'
    return beginning_columns_flag_violated_constraints
