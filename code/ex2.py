from pyomo.environ import *
from pyomo.opt import SolverFactory

model = ConcreteModel()

# Define variables
model.a = Var(list(range(2)), within=NonNegativeIntegers)

# Define the inequality constraint
def inequality_constraint_rule(model, i, j, num):
    return model.a[i]/model.a[j] <= num

model.inequality_constraint1 = Constraint(rule=lambda model: inequality_constraint_rule(model, 0,1,2))
# Define the objective function
def objective_rule(model):
    return model.a[0]* model.a[1]

model.constraint = Constraint(expr=model.a[0] + model.a[1] == 31)
model.obj = Objective(rule=objective_rule, sense=maximize)

#use baron to solve this problem and only iterate once maxmimum once a solution that identifies the constraints is found. onlhy allow integer solutions.
solver = SolverFactory('bonmin')
"""solver.options['MaxIter'] = 1
solver.options['IntSol'] = 'yes'
solver.options['MaxSol'] = 1""" 

# Solve the model
results = solver.solve(model, tee=True)


# Print the results

#print the number of variables, constraints and nonlinearities
print(results)

print('a1 =', model.a[0].value)
print('a2 =', model.a[1].value)