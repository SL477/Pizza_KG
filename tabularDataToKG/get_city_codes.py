"""Get the state codes from DBPedia using SPARQL and save to CSV"""
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import pandas as pd

if __name__ == "__main__":
    sparql = SPARQLWrapper("https://dbpedia.org/sparql/")
    sparql.setReturnFormat(JSON)
    with open(os.path.join('tabularDataToKG', 'getCityCodes.sparql'), 'r') as f:
        # print(f.read())
        sparql.setQuery(f.read())

    try:
        ret = sparql.queryAndConvert()

        states = []
        cities = []

        for r in ret["results"]["bindings"]:
            print(r)
            states.append(r['state']['value'])
            cities.append(r['city']['value'])

        # save to CSV
        pd.DataFrame.from_dict(
            {'state': states, 'city': cities}).to_csv(
            os.path.join("tabularDataToKG", "cities.csv"), index=False)
    except Exception as e:
        print(e)
