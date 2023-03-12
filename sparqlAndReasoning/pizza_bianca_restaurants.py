"""This is to get the details of the restaurants that sell pizza without
tomato"""
import rdflib
import os
import pandas as pd


def main():
    """Get the details of the restaurants that sell pizza without tomato"""
    g = rdflib.Graph()
    g.parse(os.path.join('sparqlAndReasoning', 'ontology_ttl.ttl'),
            format='ttl')
    query = """
    SELECT DISTINCT 
        ?restaurant
        ?restaurantLabel
        ?restaurantComment
        ?cityLabel
        ?restaurantLongitude
        ?restaurantLatitude
        ?restaurantDateAdded
        (group_concat(?restaurantDateUpdated) AS ?dateUpdated)
        ?restaurantID
        ?restaurantPostCode
        ?restaurantCurrency
        ?restaurantPriceMax
        ?restaurantPriceMin
        (group_concat(?primaryCategory) AS ?primaryCategories)
        ?restaurantAddress
        ?restaurantName
        ?keys
        (GROUP_CONCAT(?category) AS ?categories)
    WHERE {
        ?restaurant rdf:type tef:restaurant .
        ?restaurant tef:hasMenuItem ?item .
        ?item rdfs:label ?itemLabel .
        ?restaurant rdfs:label ?restaurantLabel .
        ?restaurant rdfs:comment ?restaurantComment .
        ?restaurant tef:restaurantInCity ?city .
        ?city rdfs:label ?cityLabel .
        ?restaurant tef:longitude ?restaurantLongitude .
        ?restaurant tef:latitude ?restaurantLatitude .
        ?restaurant tef:dateAdded ?restaurantDateAdded .
        ?restaurant tef:dateUpdated ?restaurantDateUpdated .
        ?restaurant tef:priceRangeCurrency ?restaurantCurrency .
        ?restaurant tef:id ?restaurantID .
        ?restaurant tef:priceRangeMax ?restaurantPriceMax .
        ?restaurant tef:priceRangeMin ?restaurantPriceMin .
        ?restaurant tef:primaryCategories ?primaryCategory .
        ?restaurant tef:address ?restaurantAddress .
        ?restaurant tef:restaurantName ?restaurantName .
        ?restaurant tef:keys ?keys .
        ?restaurant tef:category ?category .
        OPTIONAL {
            ?restaurant tef:postalCode ?restaurantPostCode .
        }
        FILTER ( regex(lcase(str(?itemLabel)), "bianca") || regex(lcase(str(?itemLabel)), "white"))
    }
    GROUP BY ?restaurant
        ?restaurantLabel
        ?restaurantComment
        ?cityLabel
        ?restaurantLongitude
        ?restaurantLatitude
        ?restaurantDateAdded
        ?restaurantID
        ?restaurantPostCode
        ?restaurantCurrency
        ?restaurantPriceMax
        ?restaurantPriceMin
        ?restaurantAddress
        ?restaurantName
        ?keys
    LIMIT 100
    """

    res = g.query(query)
    cnt = 0
    for row in res:
        print(row.restaurant, row.restaurantLabel, row.restaurantComment,
              row.cityLabel, row.restaurantLongitude,
              row.restaurantLatitude, row.restaurantDateAdded,
              row.dateUpdated, row.restaurantID, row.restaurantPostCode,
              row.restaurantCurrency, row.restaurantPriceMax,
              row.restaurantPriceMin, row.primaryCategories,
              row.restaurantAddress, row.restaurantName, row.keys,
              row.categories)
        cnt += 1
    print(f"Number of rows: {cnt}")


if __name__ == '__main__':
    main()
