from itertools import product
from mip import Model, xsum, minimize, BINARY

def solve_tsp(data):
    n = data['n']
    V = set(data['V'])
    c = data['c']
    V0 = set(data['V0'])
    V1 = set(data['V1'])
    P = data['P']
    
    model = Model()

    # binary variables indicating if arc (i,j) is used on the route or not
    x = [[model.add_var(var_type=BINARY) for j in V] for i in V]

    # continuous variable to prevent subtours: each city will have a
    # different sequential id in the planned route except the first one
    y = [model.add_var() for i in V]

    # objective function: minimize the distance
    model.objective = minimize(xsum(c[i][j]*x[i][j] for i in V for j in V))

    # constraint : leave each city only once
    for i in V:
        model += xsum(x[i][j] for j in V - {i}) == 1

    # constraint : enter each city only once
    for i in V:
        model += xsum(x[j][i] for j in V - {i}) == 1

    # subtour elimination
    for (i, j) in product(V - {0}, V - {0}):
        if i != j:
            model += y[i] - (n+1)*x[i][j] >= y[j]-n

    # pickup before delivery constraint
    model += y[0] == n-1
    for i in P:
        # make sure i is int
        for j in P[i]:
            model += y[int(i)] >= y[j] + 1

    # optimizing
    model.optimize(max_seconds=30)

    # get optimal solution
    opt_obj = model.objective_value
    opt_sol = [list(V)[0]]
    nc = 0
    while True:
        nc = [i for i in V if x[nc][i].x >= 0.99][0]
        opt_sol.append(nc)
        if nc == 0:
            break
    return opt_obj, opt_sol
