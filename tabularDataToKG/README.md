# Tabular Data To KG

This converts the original data into a Knowledge Graph

## Files

- City.pkl: the dictionary of the State code to URLs
- createCityDictionary.py: the code to create the city.pkl file
- createStateDictionary.py: the code to create the state.pkl file
- get_city_codes.py: the code to call the SPARQL endpoint of dbpedia to get the majority of the cities
- get_state_codes.py: the code to call the SPARQL endpoint of dbpedia to get the state codes
- get_us_cities.py: the code to call the SPARQL endpoint of dbpedia to get all US cities
- getCityCodes.sparql: the query to get the cities and states of all US cities
- getPopulatedPlace.sparql: a query to get all populated places from the list
- getSinglePopulatedPlace.sparql: a query to get a single populated place
- getStateCodes.sparql: a query to get all of the states in the USA
- getTowns.sparql: a query to get the list of towns in the USA
- getUSCities.sparql: a query to get all US cities
- main.py: the code to convert the data to a Knowledge Graph
- state.pkl: a dictionary of states and their URLS
- urlsPlain.xlsx: an Excel file containing the cities and their dbpedia URLs
