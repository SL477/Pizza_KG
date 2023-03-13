# SPARQL and Reasoning

To run reasoning use:

```bash
python3 sparqlAndReasoning/inference.py
```

## Files

- \_\_init__.py: this sets this folder up as a Python module
- inference.py: this runs OWL 2 RL inference on the Knowledge Graph from the end of tabularDataToKG
- ontology_ttl.ttl: this is the data post inference
- pizza_bianca_restaurants_short.sparql: the query to just bring back the restaurant name, city and state
- pizza_bianca_restaurants.py: this uses the SPARQL query on the Knowledge Graph
- pizza_bianca_restaurants.sparql: the full query to get everything
- pizzaBiancaRestaurants.csv: the results of pizza_bianca_restaurants.py
