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

    # print the knowledge graph
    print_knowledge_graph(g)

    # save the knowledge graph
    g.serialize(format='ttl', destination=os.path.join('tabularDataToKG', 'ontology_ttl.owl'))


if __name__ == '__main__':
    main()


# old code
# """Convert the tabular data to a Knowledge Graph"""
# from pizza_kg.data import OrgDataFiles, get_orgData, get_Graph
# from rdflib import Graph
# import rdflib
# from rdflib.namespace import RDF, RDFS, XSD
# import pprint
# import urllib.parse
#
# def main()
#
# tef = rdflib.Namespace('http://link477.com/ds/pizza#')
# g.namespace_manager.bind('tef', tef)
# # %% get the CSV data
# df = get_orgData(OrgDataFiles.MAIN)
# df.head()
# # %% Get the Knowledge Graph
# # https://rdflib.readthedocs.io/en/stable/
# # g.serialize(destination="tbl.ttl") # save as ttl
# # g.serialize(format="xml") # save as rdf/xml
#
# # https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html
# g: Graph = get_Graph()
# # g
# # %% print the Knowledge Graph
#
# for stmt in g:
#     pprint.pprint(stmt)
#
# # %% start adding States to knowledge graph
# g: Graph = get_Graph()
# for state in df.province.unique():
#     # set up the data
#     province = rdflib.URIRef(f'http://link477.com/ds/pizza#{state}')
#     label = rdflib.Literal(state, datatype=XSD.string)
#     comment = rdflib.Literal(f'The US state with a code of {state}', datatype=XSD.string)
#
#     g.add((province, RDF.type, tef.province))
#     g.add((province, RDFS.label, label))
#     g.add((province, RDFS.comment, comment))
#     g.add((province, tef.provinceLocatedIn, tef.US))
#
# print(g.serialize(format='ttl'))
#
# # %% get the cities and states
# for _, city, province, _ in df[['city', 'province']].value_counts().reset_index().itertuples():
#     # print('city', city, 'province', province)
#     city_url = city.replace(' ', '_')
#     city_url = rdflib.URIRef(f'http://link477/ds/pizza#{city_url}')
#     print(city_url, city, type(city))
#     label = rdflib.Literal(city, datatype=XSD.string)
#     comment = rdflib.Literal(f'The city of {city} in {province}', datatype=XSD.string)
#
#     g.add((city_url, RDF.type, tef.city))
#     g.add((city_url, RDFS.label, label))
#     g.add((city_url, RDFS.comment, comment))
#     g.add((city_url, tef.cityLocatedIn, rdflib.URIRef(f'http://link477/ds/pizza#{province}')))
#
# print(g.serialize(format='ttl'))
#
# # %% Save
# g.serialize(format='ttl', destination='ontology_ttl.owl')
# # %%
