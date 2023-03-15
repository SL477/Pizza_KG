"""This is to get the number of restaurants by city and state"""
import rdflib
import os
import pandas as pd
import pprint


def main():
    """Get the number of restaurants by city and state"""
    g = rdflib.Graph()
    g.parse(os.path.join('sparqlAndReasoning', 'ontology_ttl.ttl'),
            format='ttl')
    with open(os.path.join('sparqlAndReasoning',
                           'number_restaurants.sparql'), 'r') as f:
        query = f.read()

    res = g.query(query)
    cols = [
        'cityLabel',
        'stateLabel',
        'restaurantCount'
    ]
    df = pd.DataFrame.from_records([row for row in res], columns=cols)\
        .rename(columns={'cityLabel': 'City', 'stateLabel': 'State'})
    file_name = os.path.join('sparqlAndReasoning',
                             'number_restaurants.csv')

    df.to_csv(file_name, index=False)
    pprint.pprint(df)


if __name__ == '__main__':
    main()
