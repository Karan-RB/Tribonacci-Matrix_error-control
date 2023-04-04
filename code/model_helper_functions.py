from pyomo.environ import *

def get_base_model(e12min, e12max, e23min, e23max, e13min, e13max, n_bits_msg, max_num_enc_matrix):
    # create a model
    model = ConcreteModel()

    # define the variables as an array
    model.a = Var(range(9), within=NonNegativeIntegers, bounds=(1, 2**n_bits_msg * max_num_enc_matrix * 3))

    # define the objective function
    model.obj = Objective(expr=0)

    # define the constraints
    model.con111 = Constraint(expr=model.a[1]*e12min <=model.a[0])
    model.con112 = Constraint(expr=model.a[0] <= model.a[1]*e12max)
    model.con121 = Constraint(expr=model.a[2]*e23min <=model.a[1])
    model.con122 = Constraint(expr=model.a[1] <= model.a[2]*e23max)
    model.con131 = Constraint(expr=model.a[2]*e13min <=model.a[0])
    model.con132 = Constraint(expr=model.a[0] <= model.a[2]*e13max)

    model.con211 = Constraint(expr=model.a[4]*e12min <=model.a[3])
    model.con212 = Constraint(expr=model.a[3] <= model.a[4]*e12max)
    model.con221 = Constraint(expr=model.a[5]*e23min <=model.a[4])
    model.con222 = Constraint(expr=model.a[4] <= model.a[5]*e23max)
    model.con231 = Constraint(expr=model.a[5]*e13min <=model.a[3])
    model.con232 = Constraint(expr=model.a[3] <= model.a[5]*e13max)

    model.con311 = Constraint(expr=model.a[7]*e12min <=model.a[6])
    model.con312 = Constraint(expr=model.a[6] <= model.a[7]*e12max)
    model.con321 = Constraint(expr=model.a[8]*e23min <=model.a[7])
    model.con322 = Constraint(expr=model.a[7] <= model.a[8]*e23max)
    model.con331 = Constraint(expr=model.a[8]*e13min <=model.a[6])
    model.con332 = Constraint(expr=model.a[6] <= model.a[8]*e13max)

    return model


def create_instance(model, det):

    instance = model.create_instance()
    # define the diophantine equation itself
    instance.diophantine = Constraint(expr=instance.a[0]*(instance.a[4]*instance.a[8] - instance.a[5]*instance.a[7])
                            - instance.a[1]*(instance.a[3]*instance.a[8] - instance.a[5]*instance.a[6])
                            + instance.a[2]*(instance.a[3]*instance.a[7] - instance.a[4]*instance.a[6]) ==det)
    
    return instance


def create_problem(instance, fixed, values):

    problem = instance.create_instance()

    # fix the variables
    for index in fixed:
        problem.a[index].fix(values[index])
    
    return problem

def solve_problem(problem, solver):

    results = solver.solve(problem)
    return results.solver.termination_condition == TerminationCondition.optimal
    
