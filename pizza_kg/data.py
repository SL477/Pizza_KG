"""This is to return the various data sources"""
import pandas as pd
import os
from rdflib import Graph


class OrgDataFiles:
    """Constants to hold the datafile names"""
    MINI: str = '8358_1'
    MAIN: str = 'Datafiniti_Pizza_Restaurants_and_the_Pizza_They_Sell_May19'


def get_org_data(file_name: str) -> pd.DataFrame:
    """Pass a datafile from OrgDataFiles to this to get a dataframe of the
    data

    Parameters
    ----------
    file_name: str
        the file name from OrgDataFiles

    Returns
    -------
    pd.DataFrame"""
    return pd.read_csv(
        os.path.join('orgData', file_name + '.csv'),
        parse_dates=['dateAdded', 'dateUpdated'])


def get_graph() -> Graph:
    """Get the Knowledge Graph

    Returns
    -------
    Graph"""
    g: Graph = Graph()
    g.parse('ontology_ttl.owl', format='ttl')
    return g
