# Ontology Embeddings

## Run Owl2Vec Star

Here we use [Owl2Vec](https://github.com/KRR-Oxford/OWL2Vec-Star) to create word embeddings for the Knowledge graph.

```bash
py OWL2Vec_Standalone.py -config_file default.cfg
```

Update all calls to open in owl2vec_star to include `encoding="utf-8"`.
This is because some of the URLs from DBPedia have UTF-8 encodings.

### pizzaOntology

In pizzaOntology is the run on the ontology.

```bash
owl2vec_star standalone --config_file default.cfg --ontology_file ..\..\ontology.owl
```

### Pizza Data

Pizza data stores the data on the run on the data.

```bash
owl2vec_star standalone --config_file default.cfg --ontology_file data.owl
```

### Pizza Data New Seed

This uses a new random seed.

```bash
owl2vec_star standalone --config_file pizzaData.cfg --ontology_file data.owl
```

## Vector Comparison

Here we compare the different models and pairs of words. Using:

```bash
python3 ontologyEmbeddings/vector_comparison.py
```

## Clustering

To get the clusters use:

```bash
python3 ontologyEmbeddings/clustering.py
```

## Files

- clustering.py: the code to generate the PCA/KMeans graphs
- vector_comparison.py: Compare various different word vectors
- pizzaData: this folder contains the model for the Pizza Data Turtle file converted to RDF format
- pizzaDataNewSeed: this folder contains the model for the Pizza Data Turtle file converted to RDF format with a different seed
- pizzaOntology: this folder contains the model for the Pizza Ontology file
