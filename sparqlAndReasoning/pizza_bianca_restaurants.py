"""This is to get the details of the restaurants that sell pizza without
tomato"""
import rdflib
import os
import pandas as pd
import pprint


def main():
    """Get the details of the restaurants that sell pizza without tomato.
    Saves to pizza_bianca_restaurants.csv"""
    g = rdflib.Graph()
    g.parse(os.path.join('sparqlAndReasoning', 'ontology_ttl.ttl'),
            format='ttl')
    with open(os.path.join('sparqlAndReasoning',
                           'pizza_bianca_restaurants.sparql'), 'r') as f:
        query = f.read()

    res = g.query(query)
    cols = [
        'restaurant',
        'restaurantLabel',
        'restaurantComment',
        'cityLabel',
        'restaurantLongitude',
        'restaurantLatitude',
        'restaurantDateAdded',
        'dateUpdated',
        'restaurantID',
        'restaurantPostCode',
        'restaurantCurrency',
        'restaurantPriceMax',
        'restaurantPriceMin',
        'primaryCategories',
        'restaurantAddress',
        'restaurantName',
        'keys',
        'categories',
        'stateLabel',
        'countryLabel'
    ]
    df = pd.DataFrame.from_records([row for row in res], columns=cols)
    file_name = os.path.join('sparqlAndReasoning',
                             'pizzaBiancaRestaurants.csv')

    df.to_csv(file_name, index=False)
    pprint.pprint(df)


if __name__ == '__main__':
    main()
