# Pizza Knowledge Graph

This was the coursework for the Semantic Web-tech and Knowledge Graphs Coursework. I was not enrolled in this module. But decided to do this later.

The specification is [here](https://github.com/turing-knowledge-graphs/teaching/blob/main/city/2020-2021/INM713_Coursework.pdf) and the data is [here](https://www.kaggle.com/datasets/datafiniti/pizza-restaurants-and-the-pizza-they-sell?resource=download)

The final class hierarchy:

![Class Hierarchy](https://github.com/SL477/Pizza_KG/blob/6fca04b2551f58a7955025b2caf3c7821c45d3d4/images/ClassHierarchy.JPG?raw=true)

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

![Class Relationships](/images/ClassRelationships.JPG)

<!--(https://github.com/SL477/Pizza_KG/blob/main/images/ClassRelationships.JPG)-->

## Ontology Embeddings

Here I used OWL2Vec to create various models from my pizza Knowledge Graph.

### Vector Similarity

| Words | Pizza Data Model | New Seed Model | Ontology Model |
| :--: | :--: | :--: | :--: |
|pizza vs [tef:margherita](http://link477.com/ds/pizza#margherita) | 0.19777332 | 0.18296033 | 0.29705462 |
| margherita vs [tef:marherita](http://link477.com/ds/pizza#margherita) | 0.3494562 | 0.26561624 | 0.48218608 |
| pizza vs [tef:pizza](http://link477.com/ds/pizza#pizza) | 0.22770958 | 0.2965466 | 0.23359077 |
| american vs [tef:american](http://link477.com/ds/pizza#american) | 0.31192777 | 0.25724742 | 0.42699656 |
| pizzaiola vs [tef:pizzaiola](http://link477.com/ds/pizza#pizzaiola) | 0.2567482 | 0.2311137 | 0.46955892 |

### Clustering

There did not seem to be much difference in changing the number of clusters:

Pizza Ontology Model:

![Pizza Ontology Model](/images/pizzaOntologyModelClusters.png)

Pizza Data Model:

![Pizza Data Model](/images/pizzaDataModelClusters.png)

Pizza Data New Seed Model

![Pizza Data New Seed Model](/images/pizzaDataNSModelClusters.png)


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
