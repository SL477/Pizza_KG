"""Tabular data to Knowledge graph"""
import os
import pandas as pd
from pizza_kg.data import OrgDataFiles, get_org_data, get_graph
from rdflib import Graph
import rdflib
from rdflib.namespace import RDF, RDFS, XSD
from pickle import load


dbr_url = 'http://dbpedia.org/resource/'
tef_url = 'http://link477.com/ds/pizza#'


def string_escape(org: str) -> str:
    """This is to replace special characters

    Parameters
    ----------
    org: str
        The original value

    Returns
    -------
    str
        the cleaned data"""
    return org.replace("'", "''").replace("&", "&amp;")


def print_knowledge_graph(g: Graph) -> None:
    """Print each statement in the Knowledge Graph

    Parameters
    ----------
    g: Graph
        The Knowledge graph to print

    Returns
    -------
    None"""
    # for stmt in g:
    #     pprint.pprint(stmt)
    print(g.serialize(format='ttl'))


def main():
    """This builds up and saves the Knowledge Graph"""
    # get the Knowledge Graph
    # https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html
    g: Graph = get_graph()

    # set up the namespaces
    tef = rdflib.Namespace(tef_url)
    g.namespace_manager.bind('tef', tef)
    dbr = rdflib.Namespace(dbr_url)
    g.namespace_manager.bind('dbr', dbr)

    # add the country
    country_url = rdflib.URIRef(dbr_url + 'United_States')
    label = rdflib.Literal('United States of America', datatype=XSD.string)
    comment = rdflib.Literal(
        'The country of the United States of America',
        datatype=XSD.string)

    g.add((country_url, RDF.type, tef.country))
    g.add((country_url, RDFS.label, label))
    g.add((country_url, RDFS.comment, comment))

    # open the state dictionary
    with open(os.path.join('tabularDataToKG', 'state.pkl'), 'rb') as f:
        state_dict = load(f)

    # start adding the states
    # load the data
    df: pd.DataFrame = get_org_data(OrgDataFiles.MAIN)
    df.rename(columns={'menus.currency': 'menusCurrency'}, inplace=True)
    for state in df.province.unique():
        # set up the data
        province = rdflib.URIRef(state_dict[state])
        state_name = str(province)[28:]
        label = rdflib.Literal(state_name, datatype=XSD.string)
        comment = rdflib.Literal(
            f'The US State of {state_name}',
            datatype=XSD.string)

        g.add((province, RDF.type, tef.province))
        g.add((province, RDFS.label, label))
        g.add((province, RDFS.comment, comment))
        g.add((province, tef.provinceLocatedIn, country_url))

    # start adding the cities
    city_df = pd.read_excel(os.path.join('tabularDataToKG', 'urlsPlain.xlsx'))
    for city_tup in city_df.itertuples():
        # set up the data
        city_url = rdflib.URIRef(city_tup.CityURL.replace("'", ""))
        label = rdflib.Literal(string_escape(city_tup.city), datatype=XSD.string)
        state = state_dict[city_tup.province]
        comment = rdflib.Literal(
            f'The US City of {string_escape(city_tup.city)} in state {state[28:]}',
            datatype=XSD.string)

        g.add((city_url, RDF.type, tef.city))
        g.add((city_url, RDFS.label, label))
        g.add((city_url, RDFS.comment, comment))
        g.add((city_url, tef.provinceLocatedIn, rdflib.URIRef(state)))

    # start adding the restaurants
    restaurant_fields = [
        'id',
        'address',
        'categories',
        'primaryCategories',
        'city',
        'country',
        'latitude',
        'longitude',
        'menuPageURL',
        'menusCurrency',
        'name',
        'postalCode',
        'priceRangeCurrency',
        'priceRangeMin',
        'priceRangeMax',
        'province'
    ]

    with open(os.path.join('tabularDataToKG', 'city.pkl'), 'rb') as f:
        city_dict: dict = load(f)

    # restaurant_count = 0
    for restaurant_tup in df[restaurant_fields].astype(str).value_counts().reset_index().itertuples():
        restaurant_url = rdflib.URIRef(tef_url + restaurant_tup.id)
        restaurant_id = rdflib.Literal(restaurant_tup.id, datatype=XSD.string)
        restaurant_addr = rdflib.Literal(string_escape(restaurant_tup.address), datatype=XSD.string)

        g.add((restaurant_url, RDF.type, tef.restaurant))
        g.add((restaurant_url, tef.id, restaurant_id))
        g.add((restaurant_url, tef.address, restaurant_addr))

        # add each category
        for cat in restaurant_tup.categories.replace(' and ', ',').split(','):
            cat_literal = rdflib.Literal(string_escape(cat), datatype=XSD.string)
            g.add((restaurant_url, tef.category, cat_literal))

        # add each primary category
        for cat in restaurant_tup.primaryCategories.split(','):
            cat_literal = rdflib.Literal(string_escape(cat), datatype=XSD.string)
            g.add((restaurant_url, tef.primaryCategories, cat_literal))

        # get the city
        city_url = city_dict.get(restaurant_tup.city + '_' + restaurant_tup.province, '')
        if city_url != '':
            city_url = rdflib.URIRef(city_url.replace("'", ""))
            g.add((restaurant_url, tef.restaurantInCity, city_url))

        # latitude
        restaurant_latitude = rdflib.Literal(restaurant_tup.latitude, datatype=XSD.decimal)
        g.add((restaurant_url, tef.latitude, restaurant_latitude))

        # longitude
        restaurant_longitude = rdflib.Literal(restaurant_tup.longitude, datatype=XSD.decimal)
        g.add((restaurant_url, tef.longitude, restaurant_longitude))

        # menu page URL
        if restaurant_tup.menuPageURL != "nan":
            restaurant_menu_page_url = rdflib.Literal(restaurant_tup.menuPageURL, datatype=XSD.anyURI)
            g.add((restaurant_url, tef.menuPageURL, restaurant_menu_page_url))

        # menu currency
        restaurant_menu_curr = rdflib.Literal(restaurant_tup.menusCurrency, datatype=XSD.string)
        g.add((restaurant_url, tef.term('menus.currency'), restaurant_menu_curr))

        # restaurant name
        restaurant_name = rdflib.Literal(string_escape(restaurant_tup.name), datatype=XSD.string)
        g.add((restaurant_url, tef.resaurantName, restaurant_name))

        # postal code
        restaurant_post_code = rdflib.Literal(restaurant_tup.postalCode, datatype=XSD.string)
        g.add((restaurant_url, tef.postalCode, restaurant_post_code))

        # price range currency
        restaurant_price_range_currency = rdflib.Literal(restaurant_tup.priceRangeCurrency, datatype=XSD.string)
        g.add((restaurant_url, tef.priceRangeCurrency, restaurant_price_range_currency))

        # price range min
        restaurant_price_range_min = rdflib.Literal(restaurant_tup.priceRangeMin, datatype=XSD.integer)
        g.add((restaurant_url, tef.priceRangeMin, restaurant_price_range_min))

        # price range max
        restaurant_price_range_max = rdflib.Literal(restaurant_tup.priceRangeMax, datatype=XSD.integer)
        g.add((restaurant_url, tef.priceRangeMax, restaurant_price_range_max))

        # label and comment
        label = rdflib.Literal(string_escape(restaurant_tup.name) + '_' + string_escape(restaurant_tup.city), datatype=XSD.string)
        comment = rdflib.Literal(string_escape(restaurant_tup.name) + " in " + string_escape(restaurant_tup.city), datatype=XSD.string)

        g.add((restaurant_url, RDFS.label, label))
        g.add((restaurant_url, RDFS.comment, comment))

    # print the knowledge graph
    print_knowledge_graph(g)

    # save the knowledge graph
    g.serialize(
        format='ttl',
        destination=os.path.join('tabularDataToKG', 'ontology_ttl.owl'))


if __name__ == '__main__':
    main()
