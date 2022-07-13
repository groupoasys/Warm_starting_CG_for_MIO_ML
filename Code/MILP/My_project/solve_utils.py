import io
import re
from contextlib import redirect_stdout
from pyomo.opt import SolverFactory
import time


def get_ticks_from_output(output):
    ticks = float(re.search(r"Deterministic time = (\d*.\d+) ticks", output).group(1))
    return ticks


def get_iterations_from_output(output):
    iterations = float(re.search(r"Iterations = (\d+)", output).group(1))
    return iterations


def solve_and_get_cplex_ticks(model,
                              solver,
                              solve_options=None):
    solve_options = {} if solve_options is None else solve_options
    print_tee = False
    try:
        print_tee = solve_options['tee']
    except KeyError:
        pass

    solve_options['tee'] = True
    with io.StringIO() as buf, redirect_stdout(buf):
        solver_output = solver.solve(model, **solve_options)
        output = buf.getvalue()

    if print_tee:
        print(output)

    solver_output['custom'] = {}
    try:
        solver_output['custom']['ticks'] = get_ticks_from_output(output)
        solver_output['custom']['iterations'] = get_iterations_from_output(output)

    except:
        solver_output['custom']['ticks'] = -1.
        solver_output['custom']['iterations'] = -1.

    return solver_output


def set_solver_options(solver_name='cplex'):
    if solver_name == 'cplex':
        solver_options = {'mipgap': 1e-10,
                          'threads': 1}

    return solver_options


def set_optimizer_options():
    optimizer_options = {'tee': False,
                         'load_solutions': False}
    return optimizer_options


def solve_model(model,
                solver_name='cplex'):
    opt = SolverFactory(solver_name)
    solver_options = set_solver_options(solver_name=solver_name)
    for key in solver_options:
        opt.options[key] = solver_options[key]
    optimizer_options = set_optimizer_options()
    initial_time_per_individual = time.time()
    solution = solve_and_get_cplex_ticks(model,
                                         solver=opt,
                                         solve_options=optimizer_options)
    end_time_per_individual = time.time()
    model.solutions.load_from(solution)
    elapsed_time = end_time_per_individual - initial_time_per_individual

    return (model,
            solution,
            elapsed_time)
