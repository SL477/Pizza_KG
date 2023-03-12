"""This is to get the details of the restaurants that sell pizza without
tomato"""
import rdflib
import os
import pandas as pd


def main():
    """Get the details of the restaurants that sell pizza without tomato"""
    g = rdflib.Graph()
    g.parse(os.path.join('sparqlAndReasoning', 'ontology_ttl.ttl'),
            format='ttl')
    query = """
    SELECT DISTINCT ?restaurant
    WHERE {
        ?restaurant rdf:type tef:country
    } LIMIT 100
    """

    res = g.query(query)
    for row in res:
        print(row)


if __name__ == '__main__':
    main()
