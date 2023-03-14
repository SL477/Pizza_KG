# Pizza Knowledge Graph

This was the coursework for the Semantic Web-tech and Knowledge Graphs Coursework. I was not enrolled in this module. But decided to do this later.

The specification is [here](https://github.com/turing-knowledge-graphs/teaching/blob/main/city/2020-2021/INM713_Coursework.pdf) and the data is [here](https://www.kaggle.com/datasets/datafiniti/pizza-restaurants-and-the-pizza-they-sell?resource=download)

## Ontology Modelling

The original ontology/Knowledge Graph is stored in the ontologyModelling folder.

## Tabular Data to Knowledge Graph

This converts the CSV data to a Knowledge Graph. To run use:

```bash
python3 -m tabularDataToKG
```

## SPARQL and Reasoning

### Restaurants which sell margherita pizza

[Pizza Bianca Restaurants CSV](/sparqlAndReasoning/pizzaBiancaRestaurants.csv)

### Average prixe of a Margherita Pizza

Average price of a Margherita pizza: $12.05

## Documentation

To run use:

```bash
pipenv run dynamic_docs
```

To save use:

```bash
pipenv run save_docs
```
