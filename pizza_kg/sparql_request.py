"""Sends a SPARQL request to the URL"""
from SPARQLWrapper import SPARQLWrapper, JSON


def sparql_request(url: str, sparql_file: str) -> dict:
    """This is to make a request to the URL given with the SPARQL query

    Parameters
    ----------
    url: str
        The URL to send the data to

    sparql_file: str
        the file path where the SPARQL query is located

    Raises
    ------
    Exception
        If there were any problems connecting to the SPARQL

    Returns
    -------
    dict | None
        The dictionary with the query results or nothing if there was an
        issue"""
    sparql = SPARQLWrapper(url)
    sparql.setReturnFormat(JSON)
    with open(sparql_file, 'r') as f:
        # print(f.read())
        sparql.setQuery(f.read())

    try:
        ret = sparql.queryAndConvert()
        return ret

    except Exception as e:
        print(e)
        raise
        return None
