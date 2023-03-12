"""This is to perform OWL Rl reasoning on our Knowledge Graph"""
import os
from rdflib import Graph
import owlrl


def inference() -> None:
    """This is to run OWL 2 RL reasoning on our Ontology.
    It takes the Knowledge graph from tabularDataToKG, expands it and then
    saves in sparqlAndReasoning/ontology_ttl.ttl

    Returns
    -------
    None"""
    g = Graph()
    tabularDataToKG_graph = os.path.join('tabularDataToKG',
                                         'ontology_ttl.owl')
    g.parse(tabularDataToKG_graph, format='ttl')

    print(f'Pre-reasoning number of triples: {len(g)}')

    # run the reasoning
    # from Lab 7 OWL reasoning https://github.com/city-knowledge-graphs/python
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics,
                           axiomatic_triples=True,
                           datatype_axioms=False).expand(g)

    print(f'Post-reasoning number of triples: {len(g)}')

    # print and save
    # print(g.serialize(format='ttl'))
    g.serialize(format='ttl',
                destination=os.path.join('sparqlAndReasoning',
                                         'ontology_ttl.ttl'))


if __name__ == '__main__':
    inference()
