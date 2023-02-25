"""Get the state codes from DBPedia using SPARQL and save to CSV"""
import os
import pandas as pd
from pizza_kg.sparql_request import sparql_request

if __name__ == "__main__":
    ret = sparql_request(
        "https://dbpedia.org/sparql/",
        os.path.join('tabularDataToKG', 'getCityCodes.sparql'))
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
