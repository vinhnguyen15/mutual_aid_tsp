# TSP with pickup and dropoff constraints

This app demonstrates the solution to the TSP problem with pickup and delivery constrains. 

## Deployment

To deploy on Heroku:

```bash
heroku login
heroku create mutualaid-tsp
git push heroku master
```

Sample request:
```bash
curl --location --request GET 'https://mutualaid-tsp.herokuapp.com/shortest-route' \
--header 'Content-Type: text/plain' \
--data-raw '{"n": 14, "V": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "c": [[0, 83, 81, 113, 52, 42, 73, 44, 23, 91, 105, 90, 124, 57], [83, 0, 161, 160, 39, 89, 151, 110, 90, 99, 177, 143, 193, 100], [81, 161, 0, 90, 125, 82, 13, 57, 71, 123, 38, 72, 59, 82], [113, 160, 90, 0, 123, 77, 81, 71, 91, 72, 64, 24, 62, 63], [52, 39, 125, 123, 0, 51, 114, 72, 54, 69, 139, 105, 155, 62], [42, 89, 82, 77, 51, 0, 70, 25, 22, 52, 90, 56, 105, 16], [73, 151, 13, 81, 114, 70, 0, 45, 61, 111, 36, 61, 57, 70], [44, 110, 57, 71, 72, 25, 45, 0, 23, 71, 67, 48, 85, 29], [23, 90, 71, 91, 54, 22, 61, 23, 0, 74, 89, 69, 107, 36], [91, 99, 123, 72, 69, 52, 111, 71, 74, 0, 117, 65, 125, 43], [105, 177, 38, 64, 139, 90, 36, 67, 89, 117, 0, 54, 22, 84], [90, 143, 72, 24, 105, 56, 61, 48, 69, 65, 54, 0, 60, 44], [124, 193, 59, 62, 155, 105, 57, 85, 107, 125, 22, 60, 0, 97], [57, 100, 82, 63, 62, 16, 70, 29, 36, 43, 84, 44, 97, 0]], "V0": [0, 12], "V1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13], "P": {"0": [1, 4, 5, 13, 9, 8], "12": [2, 3, 6, 7, 10, 11]}}'
```

## Model and data

This app implements a modified version of the TSP problem as described [here](https://python-mip.readthedocs.io/en/latest/examples.html#the-traveling-salesman-problem).
Data needed in the request payload are:

- n: number of nodes
- V: set of nodes
- V0: set of pickup nodes
- V1: set of dropoff nodes
- c: distance matrix
- P: pickup/dropoff requirements. The keys are pickup nodes and the values are dropoff nodes

Note that the modified TSP formulation has extra constraints of the form $y_i \ge y_j + 1$ for each pickup node $i$ and the corresponding dropoff nodes $j$. These constraints are to ensure that pickup nodes are visited before dropoff nodes.

__Example__

For the dataset as provided in the above TSP example, assume that we add some extra data:

- Pickup nodes: Antwerp and Remouchamps
- Dropoff nodes: remaining nodes
- Pickup/dropoff constraints:
    - Antwerp: [Bruges, Ghent, Grand-Place de Bruxelles, Mechelen, Mons, Waterloo]
    - Remouchamps: [C-Mine, Dinant, Hasselt, Leuven, Montagne de Bueren, Namur]

The optimal route in this case is:

```
Antwerp -> Mechelen -> Grand-Place de Bruxelles -> Waterloo -> Remouchamps -> Montagne de Bueren -> C-Mine -> Hasselt -> Leuven -> Namur -> Dinant -> Mons -> Bruges -> Ghent -> Antwerp
```
![](./images/sample_opt_sol.png?raw=true)

For comparison, the original optimal route without pickup/dropoff constraints was:

```
Antwerp -> Bruges -> Ghent -> Grand-Place de Bruxelles -> Waterloo -> Mons -> Namur -> Dinant -> Remouchamps -> Montagne de Bueren -> C-Mine -> Hasselt -> Leuven -> Mechelen -> Antwerp
```

![](./images/original_opt_sol.png?raw=true)

We can see the new optimal route now respects the pickup/dropoff constraints that we introduced.



