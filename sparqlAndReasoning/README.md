# SPARQL and Reasoning

To run reasoning use:

```bash
python3 sparqlAndReasoning/inference.py
```

## Files

- \_\_init__.py: this sets this folder up as a Python module
- average_price_margherita.py: the code to get the average price of a margherita pizza
- average_price_margherita.sparql: the query to get the average price of a margherita pizza
- inference.py: this runs OWL 2 RL inference on the Knowledge Graph from the end of tabularDataToKG
- number_restaurants.csv: the states, cities and the number of restaurants in them
- number_restaurants.py: this runs the SPARQL query and saves to number_restaurants.csv
- number_restaurants.sparql: this gets the number of restaurants in each city/state combo
- ontology_ttl.ttl: this is the data post inference
- pizza_bianca_restaurants_short.sparql: the query to just bring back the restaurant name, city and state
- pizza_bianca_restaurants.py: this uses the SPARQL query on the Knowledge Graph
- pizza_bianca_restaurants.sparql: the full query to get everything
- pizzaBiancaRestaurants.csv: the results of pizza_bianca_restaurants.py
