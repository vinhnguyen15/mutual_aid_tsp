from itertools import product
from mip import Model, xsum, minimize, BINARY
from distance_matrix_calculator import create_distance_matrix

MAX_SOL_TIME_SECS = 30

def solve_tsp(data):
    # set of nodes
    V = []
    addresses = []
    for k, v in data['addresses'].items():
        V.append(int(k))
        addresses.append(v)
    V = set(V)

    # set of pickup nodes
    pickups = [int(i) for i in data['pickups']]
    V0 = set(pickups)

    P = {int(k):v for k, v in data['pickup_dropoff_constraints'].items()}

    # number of nodes
    n = len(addresses)
    
    # for testing, pass distance_matrix as a data field
    if 'distance_matrix' in data:
        c = data['distance_matrix']
    else:
        c = create_distance_matrix(addresses)
        
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

    # if pickups are not provided, use an arbitrary node
    if len(V0)==0:
        first_node = 0
    else:
        first_node = list(V0)[0]
    model += y[first_node]== n-1

    # pickup before delivery constraints
    for i in P:
        for j in P[i]:
            model += y[i] >= y[int(j)] + 1

    # optimizing
    model.optimize(max_seconds=MAX_SOL_TIME_SECS)

    # get optimal solution
    opt_obj = model.objective_value
    opt_sol = [first_node]
    nc = 0
    while True:
        nc = [i for i in V if x[nc][i].x >= 0.99][0]
        opt_sol.append(nc)
        if nc == 0:
            break
    return opt_obj, opt_sol
