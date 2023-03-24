from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np

# define bounds for the variables
e12min = 1.1911764705882353
e12max = 1.192
e23min = 1.5432098765432098
e23max = 1.5454545454545454
e13min = 1.8389261744966443
e13max = 1.8409090909090908

# define the fixed values
fixed = [34806, 29206, 18920, 84605, 71006, 45992, 71633, 60130, 38945] #[34806, 29206, 18920, 84605, 71006, 45992, 71633, 60130, 38945]
det = 1386566

# create a model
model = ConcreteModel()

# define the variables as an array
model.a = Var(range(9), within=NonNegativeIntegers)

# define the objective function
model.obj = Objective(expr=0)

# define the diophantine equation itself
model.diophantine = Constraint(expr=model.a[0]*(model.a[4]*model.a[8] - model.a[5]*model.a[7])
                        - model.a[1]*(model.a[3]*model.a[8] - model.a[5]*model.a[6])
                        + model.a[2]*(model.a[3]*model.a[7] - model.a[4]*model.a[6]) ==det)

"""def inequality_constraint_rule(model, min, max, i, j):
    return min*model.a[j] <= model.a[i] <= max*model.a[j]"""

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

"""
model.inequality_constraint1a = Constraint(rule=lambda model: inequality_constraint_rule(model, e12min, e12max, 0, 1))
model.inequality_constraint1b = Constraint(rule=lambda model: inequality_constraint_rule(model, e23min, e23max, 1, 2))
model.inequality_constraint1c = Constraint(rule=lambda model: inequality_constraint_rule(model, e13min, e13max, 0, 2))

model.inequality_constraint2a = Constraint(rule=lambda model: inequality_constraint_rule(model, e12min, e12max, 3, 4))
model.inequality_constraint2b = Constraint(rule=lambda model: inequality_constraint_rule(model, e23min, e23max, 4, 5))
model.inequality_constraint2c = Constraint(rule=lambda model: inequality_constraint_rule(model, e13min, e13max, 3, 5))

model.inequality_constraint3a = Constraint(rule=lambda model: inequality_constraint_rule(model, e12min, e12max, 6, 7))
model.inequality_constraint3b = Constraint(rule=lambda model: inequality_constraint_rule(model, e23min, e23max, 7, 8))
model.inequality_constraint3c = Constraint(rule=lambda model: inequality_constraint_rule(model, e13min, e13max, 6, 8))
"""

# define the bounds constraints for a12, b23, and a13
"""
for i in range(3):
    model.add_component(f'a{i+1}{i+2}_bounds', Constraint(expr=e12min <= model.a[i] / model.a[i+1] <= e12max))
    model.add_component(f'a{i+2}{i+3}_bounds', Constraint(expr=e23min <= model.a[i+1] / model.a[i+2] <= e23max))
    model.add_component(f'a{i+1}{i+3}_bounds', Constraint(expr=e13min <= model.a[i] / model.a[i+2] <= e13max))"""

# define the fixed value constraints
for i in range(9):
    if fixed[i] is not None:
        model.add_component(f'a{i}_fixed', Constraint(expr=model.a[i] == fixed[i]))



# solve the model
solver = SolverFactory('bonmin')

"""solver.options['MaxIter'] = 1
solver.options['IntSol'] = 'yes'
solver.options['MaxSol'] = 1"""

# Solve the model
results = solver.solve(model, tee=True)
# print the solution
if results.solver.termination_condition == TerminationCondition.infeasible:
    print("False")

print('a:', [value(model.a[i]) for i in range(9)])

