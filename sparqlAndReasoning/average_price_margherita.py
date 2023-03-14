"""This is to get the average price of a margherita pizza"""
import rdflib
import os


def main():
    """This is to get the average price of a margherita pizza"""
    g = rdflib.Graph()
    g.parse(os.path.join('sparqlAndReasoning', 'ontology_ttl.ttl'),
            format='ttl')
    with open(os.path.join('sparqlAndReasoning',
                           'average_price_margherita.sparql'), 'r') as f:
        query = f.read()

    res = g.query(query)

    for row in res:
        print(row.avgPrice)

    return row.avgPrice


if __name__ == '__main__':
    main()
