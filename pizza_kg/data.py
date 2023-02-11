"""This is to return the various data sources"""
import pandas as pd
import os
from rdflib import Graph


class OrgDataFiles:
    MINI: str = '8358_1'
    MAIN: str = 'Datafiniti_Pizza_Restaurants_and_the_Pizza_They_Sell_May19'


def get_orgData(fileName : str) -> pd.DataFrame:
    """Pass a datafile from OrgDataFiles to this to get a dataframe of the data"""
    return pd.read_csv(os.path.join('orgData', fileName + '.csv'), parse_dates=['dateAdded', 'dateUpdated'])

def get_Graph() -> Graph:
    """Get the Knowledge Graph"""
    g: Graph = Graph()
    g.parse('ontology_ttl.owl', format='ttl')
    return g
