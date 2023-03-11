"""This is a SPARQL request to get all the cities in the US"""
from pizza_kg.sparql_request import sparql_request
import os
import pandas as pd


def main():
    """This uses the SPARQL request get US Cities to get all the cities in the
    US"""
    cities = sparql_request(
        "https://dbpedia.org/sparql/",
        os.path.join('tabularDataToKG', 'getUSCities.sparql'))
    print(cities)
    if cities is not None:
        city_list = [r['city']['value'] for r in cities["results"]["bindings"]]
        # save to CSV
        pd.DataFrame.from_dict(
            {'city': city_list}).to_csv(
            os.path.join("tabularDataToKG", "allUSCities.csv"), index=False)
    else:
        print('Failed to get data')


if __name__ == '__main__':
    main()
