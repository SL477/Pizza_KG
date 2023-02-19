"""Get the state codes from DBPedia using SPARQL and save to CSV"""
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import pandas as pd

if __name__ == "__main__":
    sparql = SPARQLWrapper("https://dbpedia.org/sparql/")
    sparql.setReturnFormat(JSON)
    with open(os.path.join('tabularDataToKG', 'getStateCodes.sparql'), 'r') as f:
        # print(f.read())
        sparql.setQuery(f.read())

    try:
        ret = sparql.queryAndConvert()

        states = []
        codes = []

        for r in ret["results"]["bindings"]:
            print(r)
            states.append(r['state']['value'])
            codes.append(r['isoCode']['value'])

        # save to CSV
        pd.DataFrame.from_dict({'states': states, 'codes': codes}).to_csv(os.path.join("tabularDataToKG", "states.csv"))
    except Exception as e:
        print(e)
