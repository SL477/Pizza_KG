"""Sends a SPARQL request to the URL"""
from SPARQLWrapper import SPARQLWrapper, JSON

def sparql_request(url: str, sparql_file: str) -> dict:
    """This is to make a request to the URL given with the SPARQL query"""
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
        return None
