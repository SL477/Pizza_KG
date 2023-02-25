"""Tabular data to Knowledge graph"""
import os
import pandas as pd
from pizza_kg.data import OrgDataFiles, get_orgData, get_Graph
from rdflib import Graph
import rdflib
from rdflib.namespace import RDF, RDFS, XSD
from pickle import load

dbr_url = 'http://dbpedia.org/resource/'


def print_knowledge_graph(g: Graph) -> None:
    """Print each statement in the Knowledge Graph"""
    # for stmt in g:
    #     pprint.pprint(stmt)
    print(g.serialize(format='ttl'))


def main():
    # get the Knowledge Graph
    # https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html
    g: Graph = get_Graph()

    # set up the namespaces
    tef = rdflib.Namespace('http://link477.com/ds/pizza#')
    g.namespace_manager.bind('tef', tef)
    dbr = rdflib.Namespace(dbr_url)
    g.namespace_manager.bind('dbr', dbr)

    # add the country
    country_url = rdflib.URIRef(dbr_url + 'United_States')
    label = rdflib.Literal('United States of America', datatype=XSD.string)
    comment = rdflib.Literal('The country of the United States of America', datatype=XSD.string)

    g.add((country_url, RDF.type, tef.Country))
    g.add((country_url, RDFS.label, label))
    g.add((country_url, RDFS.comment, comment))

    # open the state dictionary
    with open(os.path.join('tabularDataToKG', 'state.pkl'), 'rb') as f:
        state_dict = load(f)

    # start adding the states
    # load the data
    df: pd.DataFrame = get_orgData(OrgDataFiles.MAIN)
    for state in df.province.unique():
        # set up the data
        province = rdflib.URIRef(state_dict[state])
        state_name = str(province)[28:]
        label = rdflib.Literal(state_name, datatype=XSD.string)
        comment = rdflib.Literal('The US State of ' + state_name, datatype=XSD.string)

        g.add((province, RDF.type, tef.province))
        g.add((province, RDFS.label, label))
        g.add((province, RDFS.comment, comment))
        g.add((province, tef.provinceLocatedIn, country_url))

    # start adding the cities
    city_df = pd.read_excel(os.path.join('tabularDataToKG', 'urlsPlain.xlsx'))
    for city_tup in city_df.itertuples():
        # setup the data
        city_url = rdflib.URIRef(city_tup.CityURL)
        label = rdflib.Literal(city_tup.city, datatype=XSD.string)
        state = state_dict[city_tup.province]
        comment = rdflib.Literal("The US City of " + city_tup.city + " in state " + state[28:], datatype=XSD.string)

        g.add((city_url, RDF.type, tef.city))
        g.add((city_url, RDFS.label, label))
        g.add((city_url, RDFS.comment, comment))
        g.add((city_url, tef.provinceLocatedIn, rdflib.URIRef(state)))

    # print the knowledge graph
    print_knowledge_graph(g)

    # save the knowledge graph
    g.serialize(format='ttl', destination=os.path.join('tabularDataToKG', 'ontology_ttl.owl'))


if __name__ == '__main__':
    main()
