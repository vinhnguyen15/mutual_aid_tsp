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
curl --location --request GET 'http://127.0.0.1:5000/shortest-route' \
--header 'Content-Type: text/plain' \
--data-raw '{
    "addresses": {
      "0": "Antwerp+Belgium",
      "1": "Bruges+Belgium",
      "2": "C-Mine+Belgium",
      "3": "Dinant+Belgium",
      "4": "Ghent+Belgium",
      "5": "Grand-Place+de+Bruxelles+Belgium",
      "6": "Hasselt+Belgium",
      "7": "Leuven+Belgium",
      "8": "Mechelen+Belgium",
      "9": "Mons+Belgium",
      "10": "Montagne+de+Bueren+Belgium",
      "11": "Namur+Belgium",
      "12": "Remouchamps+Belgium",
      "13": "Waterloo+Belgium"
    },
    "pickups": [
      "0",
      "12"
    ],
    "pickup_dropoff_constraints": {
      "0": [
        "1",
        "4",
        "5",
        "13",
        "9",
        "8"
      ],
      "12": [
        "2",
        "3",
        "6",
        "7",
        "10",
        "11"
      ]
    }
  }'
```

## Model and data

This app implements a modified version of the TSP problem as described [here](https://python-mip.readthedocs.io/en/latest/examples.html#the-traveling-salesman-problem).
Data needed in the request payload are:

- addresses: a dictionary of indices and addresses
- pickups: a list of pickup node indices
- pickup_dropoff_constraints: pickup and dropoff requirements. The keys are pickup indices and the values are dropoff indices

In addition, a "distance_matrix" field can be included in the payload (for testing purpose). If not provided, Google Distance Matrix API will be used to calculate the distance matrix. The environment variable `GOOGLE_DISTANCE_MATRIX_API_KEY` should have been setup in deployment.

Note that the modified TSP formulation has extra constraints of the form `y_i >= y_j + 1` for each pickup node i and the corresponding dropoff nodes j. These constraints are to ensure that pickup nodes are visited before dropoff nodes.

__Example__

For the dataset as provided in the above TSP example, assume that we add some extra data:

- Pickup nodes: Antwerp and Remouchamps
- Dropoff nodes: remaining nodes
- Pickup/dropoff constraints:
    - Antwerp: [Bruges, Ghent, Grand-Place de Bruxelles, Mechelen, Mons, Waterloo]
    - Remouchamps: [C-Mine, Dinant, Hasselt, Leuven, Montagne de Bueren, Namur]

The optimal route in this case is:

```
Antwerp -> Bruges -> Ghent -> Grand-Place de Bruxelles -> Waterloo -> Mons -> Remouchamps -> Dinant -> Namur -> Montagne de Bueren -> C-Mine -> Hasselt -> Leuven -> Mechelen -> Antwerp
```

![](./images/sample_opt_sol.png?raw=true)

For comparison, the original optimal route without pickup/dropoff constraints was:

```
Antwerp -> Bruges -> Ghent -> Grand-Place de Bruxelles -> Waterloo -> Mons -> Namur -> Dinant -> Remouchamps -> Montagne de Bueren -> C-Mine -> Hasselt -> Leuven -> Mechelen -> Antwerp
```

![](./images/original_opt_sol.png?raw=true)

We can see the new optimal route now respects the pickup/dropoff constraints that we introduced.



