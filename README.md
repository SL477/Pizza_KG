# Pizza Knowledge Graph

This was the coursework for the Semantic Web-tech and Knowledge Graphs Coursework. I was not enrolled in this module. But decided to do this later.

The specification is [here](https://github.com/turing-knowledge-graphs/teaching/blob/main/city/2020-2021/INM713_Coursework.pdf) and the data is [here](https://www.kaggle.com/datasets/datafiniti/pizza-restaurants-and-the-pizza-they-sell?resource=download)

The final class hierarchy:

![Class Hierarchy](/images/ClassHierarchy.JPG)

## Ontology Modelling

The original ontology/Knowledge Graph is stored in the ontologyModelling folder.

## Tabular Data to Knowledge Graph

This converts the CSV data to a Knowledge Graph. To run use:

```bash
python3 -m tabularDataToKG
```

## SPARQL and Reasoning

To run reasoning use:

```bash
python3 sparqlAndReasoning/inference.py
```

### Restaurants which sell Margherita pizza

[Pizza Bianca Restaurants CSV](https://github.com/SL477/Pizza_KG/blob/main/sparqlAndReasoning/pizzaBiancaRestaurants.csv)

```bash
python3 sparqlAndReasoning/pizza_bianca_restaurants.py
```

### Average price of a Margherita Pizza

Average price of a Margherita pizza: $12.05

```bash
python3 sparqlAndReasoning/average_price_margherita.py
```

### Number of restaurants

[Number of Restaurants CSV](https://github.com/SL477/Pizza_KG/blob/main/sparqlAndReasoning/number_restaurants.csv)

```bash
python3 sparqlAndReasoning/number_restaurants.py
```

### Restaurant with no postcode

[Restaurants missing postcode csv](https://github.com/SL477/Pizza_KG/blob/main/sparqlAndReasoning/restaurants_missing_postcode.csv)

```bash
python3 sparqlAndReasoning/restaurants_missing_postcode.py
```

## Ontology Alignment

To run use:

```bash
python3 ontologyAlignment/alignment.py
```

Recreate the data using:

```bash
python3 -m ontologyAlignment.recreate_data
```

Then load the data into GraphDB, setting up the repository using the settings given in the file.
Add all the namespaces from the turtle file.
Then run the query in the SPARQL file.

Class Relationships:

![Class Relationships](https://github.com/SL477/Pizza_KG/blob/main/images/ClassRelationships.JPG)

## Ontology Embeddings

Here I used OWL2Vec to create various models from my pizza Knowledge Graph.

## Files

- data.ttl: the data in the original ontology
- dataPostAlignment.ttl: the data in the aligned ontology
- mainAlignedOntology.tll: the merged (and modified) Pizza.owl ontology and my ontology
- ontology.owl: my pizza ontology
- Pipfile: the various Python dependencies

## Documentation

To run use:

```bash
pipenv run dynamic_docs
```

To save use:

```bash
pipenv run save_docs
```
