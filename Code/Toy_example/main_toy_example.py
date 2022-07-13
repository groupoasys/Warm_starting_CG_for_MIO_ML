import pyomo.environ as pe
from pyomo.opt import SolverFactory


def create_model():
    model = pe.ConcreteModel("model")
    # Variables

    model.x = pe.Var(within=pe.Reals)
    model.y = pe.Var(within=pe.Integers)

    model.objective_function = pe.Objective(rule=objective_function,
                                            sense=pe.minimize)
    #model.constraint_1 = pe.Constraint(rule=constraint_1)
    model.constraint_2 = pe.Constraint(rule=constraint_2)
    model.constraint_3 = pe.Constraint(rule=constraint_3)
    model.constraint_4 = pe.Constraint(rule=constraint_4)
    model.constraint_5 = pe.Constraint(rule=constraint_5)
    model.constraint_6 = pe.Constraint(rule=constraint_6)

    return model


def objective_function(model):
    objective_value = model.x - model.y
    return objective_value


def constraint_1(model):
    constraint_value = model.y <= 1.5
    return constraint_value


def constraint_2(model):
    constraint_value = model.y >= 0
    return constraint_value


def constraint_3(model):
    constraint_value = model.x >= 0.5
    return constraint_value


def constraint_4(model):
    constraint_value = model.x <= 1.5
    return constraint_value


def constraint_5(model):
    constraint_value = model.y <= 3
    return constraint_value


def constraint_6(model):
    constraint_value = model.x + model.y >= 1.5
    return constraint_value


model = create_model()
opt = SolverFactory('cplex')
solver_output = opt.solve(model)
print(model.x.value)
print(model.y.value)
print(model.objective_function())
model.display()
aa = 0
