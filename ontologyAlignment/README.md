# Ontology Alignment

Run the alignment using:

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

## Files

- \_\_init\_\_.py: to initialise this as a Python package
- alignment.py: this code aligns my pizza ontology with the one from Stanford
- catalog-v001.xml: this imports the Stanford Pizza Ontology into my one
- GetMeatyPizzas.sparql: the query to get the meaty pizzas
- GraphDBPizza_KG-config.ttl: the settings for the GraphDB repository
- mainAlignedOntology.ttl: this is the full ontology of both with the alignments added
- meatyPizzas.csv: the results of the GetMeatyPizza query
- miniAlignedOntology.ttl: this just has the equivalent classes in both
- ontology.owl: the ontology pre alignment
- recreate\_data.py: used to regenerate the data using the combined ontology
