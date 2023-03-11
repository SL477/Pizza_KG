# Tabular Data To KG

This converts the original data into a Knowledge Graph. To run use:

```bash
pipenv run tabularDataToKG
```

or

```bash
python3 -m tabularDataToKG
```

## Files

- \_\_init__.py: this sets up the module
- \_\_main__.py: this runs the main code of the module
- City.pkl: the dictionary of the State code to URLs
- clean_menu_items.py: this cleans the menu items and matches them with the Ontology
- createCityDictionary.py: the code to create the city.pkl file
- createStateDictionary.py: the code to create the state.pkl file
- get_city_codes.py: the code to call the SPARQL endpoint of dbpedia to get the majority of the cities
- get_menu_descriptions.py: this gets the descriptions of the menu items and relate them to ingredients in the ontology
- get_state_codes.py: the code to call the SPARQL endpoint of dbpedia to get the state codes
- get_us_cities.py: the code to call the SPARQL endpoint of dbpedia to get all US cities
- getCityCodes.sparql: the query to get the cities and states of all US cities
- getPopulatedPlace.sparql: a query to get all populated places from the list
- getSinglePopulatedPlace.sparql: a query to get a single populated place
- getStateCodes.sparql: a query to get all of the states in the USA
- getTowns.sparql: a query to get the list of towns in the USA
- getUSCities.sparql: a query to get all US cities
- ingredientsMapping.xlsx: this maps the descriptions of the menu items and relates them to ingredients in the ontology
- main.py: the code to convert the data to a Knowledge Graph
- ontology_ttl.owl: the ontology with the CSV data in it
- pizzaMapping.xlsx: this maps the menu names to items in the ontology
- state.pkl: a dictionary of states and their URLS
- urlsPlain.xlsx: an Excel file containing the cities and their dbpedia URLs
