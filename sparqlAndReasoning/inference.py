"""This is to perform OWL Rl reasoning on our Knowledge Graph"""
import os
from rdflib import Graph
import owlrl

org_location = os.path.join('tabularDataToKG', 'ontology_ttl.owl')
org_destination = os.path.join('sparqlAndReasoning', 'ontology_ttl.ttl')


def inference(original_location: str = org_location,
              original_format: str = 'xml',
              destination: str = org_destination,
              destination_format: str = 'ttl') -> None:
    """This is to run OWL 2 RL reasoning on our Ontology.
    It takes the Knowledge graph from tabularDataToKG, expands it and then
    saves in sparqlAndReasoning/ontology_ttl.ttl

    Parameters
    ----------
    original_location: str
        Where the graph comes from

    original_format: str
        The format of the Knowledge Graph

    destination: str
        Where the extended graph is saved

    destination_format: str
        The format of the extended Knowledge Graph

    Returns
    -------
    None"""
    g = Graph()
    g.parse(original_location, format=original_format)

    print(f'Pre-reasoning number of triples: {len(g)}')

    # run the reasoning
    # from Lab 7 OWL reasoning https://github.com/city-knowledge-graphs/python
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics,
                           axiomatic_triples=True,
                           datatype_axioms=False).expand(g)

    print(f'Post-reasoning number of triples: {len(g)}')

    # print and save
    g.serialize(format=destination_format, destination=destination)


if __name__ == '__main__':
    inference()
