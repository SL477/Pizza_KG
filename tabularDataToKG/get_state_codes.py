"""Get the state codes from DBPedia using SPARQL and save to CSV"""
import os
import pandas as pd
from pizza_kg.sparql_request import sparql_request


def main():
    """This runs the get State Codes SPARQL query on DBPedia and saves the
    results to states2.csv"""
    ret = sparql_request(
        "https://dbpedia.org/sparql/",
        os.path.join('tabularDataToKG', 'getStateCodes.sparql'))

    states = []
    codes = []

    for r in ret["results"]["bindings"]:
        print(r)
        states.append(r['state']['value'])
        codes.append(r['isoCode']['value'])

    # save to CSV
    df = pd.DataFrame.from_dict({'states': states, 'codes': codes})
    df.to_csv(os.path.join("tabularDataToKG", "states2.csv"), index=False)

if __name__ == "__main__":
    main()
