# Ontology Embeddings

Here we use [Owl2Vec](https://github.com/KRR-Oxford/OWL2Vec-Star) to create word embeddings for the Knowledge graph.
Download Owl2Vec ZIP file, extract it and then put in the files.

```bash
py OWL2Vec_Standalone.py -config_file default.cfg
```

Change size to vector-size and remove iter parameter (using version 0.1), line 227. Change line 85/119/214 to use utf-8 encoding.

In pizzaOntology is the run on the ontology.

```bash
owl2vec_star standalone --config_file default.cfg --ontology_file ..\..\ontology.owl
```
