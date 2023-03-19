"""Tabular data to Knowledge graph"""
import os
import pandas as pd
from pizza_kg.data import OrgDataFiles, get_org_data
from rdflib import Graph
import rdflib
from rdflib.namespace import RDF, RDFS, XSD
from pickle import load
from .clean_menu_items import main as clean_menu_items
import urllib.parse
from .get_menu_descriptions import main as get_menu_descriptions
from datetime import datetime


dbr_url = 'http://dbpedia.org/resource/'
tef_url = 'http://link477.com/ds/pizza#'


def string_escape(org: str) -> str:
    """This is to replace special characters

    Parameters
    ----------
    org: str
        The original value

    Returns
    -------
    str
        the cleaned data"""
    return org.replace("'", "''").replace("&", "&amp;")


def print_knowledge_graph(g: Graph) -> None:
    """Print each statement in the Knowledge Graph

    Parameters
    ----------
    g: Graph
        The Knowledge graph to print

    Returns
    -------
    None"""
    # for stmt in g:
    #     pprint.pprint(stmt)
    print(g.serialize(format='ttl'))


def main(original_location: str = 'ontology_ttl.owl',
         original_format: str = 'ttl',
         destination: str = os.path.join('tabularDataToKG', 'ontology.owl'),
         destination_format: str = 'xml'):
    """This builds up and saves the Knowledge Graph

    Parameters
    ----------
    original_location: str
        WHere the ontology is saved

    original_format: str
        The format of the Knowledge Graph

    destination: str
        Where the Knowledge graph is going

    destination_format: str
        The destination format of the Knowledge Graph"""
    # get the Knowledge Graph
    # https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html
    g: Graph = rdflib.Graph()
    g.parse(original_location, format=original_format)

    # set up the namespaces
    tef = rdflib.Namespace(tef_url)
    g.namespace_manager.bind('tef', tef)
    dbr = rdflib.Namespace(dbr_url)
    g.namespace_manager.bind('dbr', dbr)

    # add the country
    country_url = rdflib.URIRef(dbr_url + 'United_States')
    label = rdflib.Literal('United States of America', datatype=XSD.string)
    comment = rdflib.Literal(
        'The country of the United States of America',
        datatype=XSD.string)

    g.add((country_url, RDF.type, tef.country))
    g.add((country_url, RDFS.label, label))
    g.add((country_url, RDFS.comment, comment))

    # open the state dictionary
    with open(os.path.join('tabularDataToKG', 'state.pkl'), 'rb') as f:
        state_dict = load(f)

    # start adding the states
    # load the data
    df: pd.DataFrame = get_org_data(OrgDataFiles.MAIN)
    # df.rename(columns={'menus.currency': 'menusCurrency'}, inplace=True)
    for state in df.province.unique():
        # set up the data
        province = rdflib.URIRef(state_dict[state])
        state_name = str(province)[28:]
        label = rdflib.Literal(state_name, datatype=XSD.string)
        comment = rdflib.Literal(
            f'The US State of {state_name}',
            datatype=XSD.string)

        g.add((province, RDF.type, tef.province))
        g.add((province, RDFS.label, label))
        g.add((province, RDFS.comment, comment))
        g.add((province, tef.provinceLocatedIn, country_url))

    # start adding the cities
    city_df = pd.read_excel(os.path.join('tabularDataToKG', 'urlsPlain.xlsx'))
    for city_tup in city_df.itertuples():
        # set up the data
        city_url = rdflib.URIRef(city_tup.CityURL.replace("'", ""))
        label = rdflib.Literal(string_escape(city_tup.city),
                               datatype=XSD.string)
        state = state_dict[city_tup.province]
        comment = rdflib.Literal('The US City of '
                                 + string_escape(city_tup.city) + ' in state '
                                 + state[28:],
                                 datatype=XSD.string)

        g.add((city_url, RDF.type, tef.city))
        g.add((city_url, RDFS.label, label))
        g.add((city_url, RDFS.comment, comment))
        g.add((city_url, tef.cityLocatedIn, rdflib.URIRef(state)))

    # start adding the restaurants
    restaurant_fields = [
        'id',
        'address',
        'categories',
        'primaryCategories',
        'city',
        'country',
        'latitude',
        'longitude',
        'menuPageURL',
        'name',
        'postalCode',
        'priceRangeCurrency',
        'priceRangeMin',
        'priceRangeMax',
        'province',
        'dateAdded',
        'dateUpdated',
        'keys'
    ]

    with open(os.path.join('tabularDataToKG', 'city.pkl'), 'rb') as f:
        city_dict: dict = load(f)

    restaurant_df = df[restaurant_fields].astype(str).value_counts()\
        .reset_index()

    for restaurant_tup in restaurant_df.itertuples():
        restaurant_url = rdflib.URIRef(tef_url + restaurant_tup.id)

        g.add((restaurant_url, RDF.type, tef.restaurant))
        g.add((restaurant_url,
               tef.id,
               rdflib.Literal(restaurant_tup.id, datatype=XSD.string)))
        g.add((restaurant_url,
               tef.address,
               rdflib.Literal(string_escape(restaurant_tup.address),
                              datatype=XSD.string)))

        # add each category
        for cat in restaurant_tup.categories.replace(' and ', ',').split(','):
            g.add((restaurant_url,
                   tef.category,
                   rdflib.Literal(string_escape(cat), datatype=XSD.string)))

        # add each primary category
        for cat in restaurant_tup.primaryCategories.split(','):
            g.add((restaurant_url,
                   tef.primaryCategories,
                   rdflib.Literal(string_escape(cat), datatype=XSD.string)))

        # get the city
        # city_url = city_dict.get(
        #     restaurant_tup.city + '_' + restaurant_tup.province, '')
        city_state = restaurant_tup.city + '_' + restaurant_tup.province
        if city_state == 'Cañon City_CO':
            city_url = 'http://dbpedia.org/resource/Ca\u00F1on_City,_Colorado'
        elif city_state == 'Española_NM':
            city_url = 'http://dbpedia.org/resource/Espa\u00F1ola,_New_Mexico'
        else:
            city_url = city_dict[city_state]
        if city_url != '':
            city_url = rdflib.URIRef(city_url.replace("'", ""))
            g.add((restaurant_url, tef.restaurantInCity, city_url))

        # latitude
        g.add((restaurant_url,
               tef.latitude,
               rdflib.Literal(restaurant_tup.latitude, datatype=XSD.decimal)))

        # longitude
        g.add((restaurant_url,
               tef.longitude,
               rdflib.Literal(restaurant_tup.longitude,
                              datatype=XSD.decimal)))

        # menu page URL
        if restaurant_tup.menuPageURL != "nan":
            g.add((restaurant_url,
                   tef.menuPageURL,
                   rdflib.Literal(restaurant_tup.menuPageURL,
                                  datatype=XSD.anyURI)))

        # restaurant name
        g.add((restaurant_url,
               tef.restaurantName,
               rdflib.Literal(string_escape(restaurant_tup.name),
                              datatype=XSD.string)))

        # postal code
        if not pd.isna(restaurant_tup.postalCode) or not restaurant_tup.postalCode == 'nan':
            g.add((restaurant_url,
                   tef.postalCode,
                   rdflib.Literal(restaurant_tup.postalCode,
                                  datatype=XSD.string)))

        # price range currency
        g.add((restaurant_url,
               tef.priceRangeCurrency,
               rdflib.Literal(restaurant_tup.priceRangeCurrency,
                              datatype=XSD.string)))

        # price range min
        g.add((restaurant_url,
               tef.priceRangeMin,
               rdflib.Literal(restaurant_tup.priceRangeMin,
                              datatype=XSD.integer)))

        # price range max
        g.add((restaurant_url,
               tef.priceRangeMax,
               rdflib.Literal(restaurant_tup.priceRangeMax,
                              datatype=XSD.integer)))

        # label and comment
        label = rdflib.Literal(string_escape(restaurant_tup.name) + '_'
                               + string_escape(restaurant_tup.city),
                               datatype=XSD.string)
        comment = rdflib.Literal(string_escape(restaurant_tup.name) + " in "
                                 + string_escape(restaurant_tup.city),
                                 datatype=XSD.string)

        g.add((restaurant_url, RDFS.label, label))
        g.add((restaurant_url, RDFS.comment, comment))

        # date Added
        date_added = datetime.strptime(restaurant_tup.dateAdded,
                                       "%Y-%m-%d %H:%M:%S%z")
        g.add((restaurant_url,
               tef.dateAdded,
               rdflib.Literal(date_added, datatype=XSD.dateTime)))

        # date updated
        date_updated = datetime.strptime(restaurant_tup.dateUpdated,
                                         "%Y-%m-%d %H:%M:%S%z")
        g.add((restaurant_url,
               tef.dateUpdated,
               rdflib.Literal(date_updated, datatype=XSD.dateTime)))

        # keys
        g.add((restaurant_url,
               tef.keys,
               rdflib.Literal(restaurant_tup.keys, datatype=XSD.string)))

    # add in the menu items
    menu_items_df = clean_menu_items()
    for menu_tup in menu_items_df.itertuples():
        menuNameEncoded = urllib.parse.quote_plus(menu_tup.menusName)
        menu_item_url = rdflib.URIRef(tef_url + menu_tup.id + menuNameEncoded)

        g.add((menu_item_url, RDF.type, tef.term(menu_tup.menuItem.strip())))

        # menu item name
        menuItemName = rdflib.Literal(menu_tup.menusName.strip(),
                                      datatype=XSD.string)
        g.add((menu_item_url, RDFS.label, menuItemName))
        g.add((menu_item_url, RDFS.comment, menuItemName))
        g.add((menu_item_url, tef.term("menus.name"), menuItemName))

        # menu currency
        menuCurrency = rdflib.Literal(menu_tup.menusCurrency.strip(),
                                      datatype=XSD.string)
        g.add((menu_item_url, tef.term('menus.currency'), menuCurrency))

        # restaurant
        restaurant_url = rdflib.URIRef(tef_url + menu_tup.id.strip())
        g.add((menu_item_url, tef.servedInRestaurant, restaurant_url))

        # date seen
        for menu_date_seen in menu_tup.menusDateSeen.split(','):
            date_updated = menu_date_seen.split('.')[0].strip('Z')
            date_updated = datetime.strptime(date_updated,
                                             "%Y-%m-%dT%H:%M:%S")
            date_updated = rdflib.Literal(date_updated, datatype=XSD.dateTime)
            g.add((menu_item_url, tef.term('menus.dateSeen'), date_updated))

        # pizza size
        if not pd.isna(menu_tup.pizzaSize):
            size = rdflib.Literal(menu_tup.pizzaSize.strip(),
                                  datatype=XSD.integer)
            g.add((menu_item_url, tef.pizzaSize, size))

        # menu description
        if not pd.isna(menu_tup.menusDescription):
            menuDesc = rdflib.Literal(menu_tup.menusDescription.strip(),
                                      datatype=XSD.string)
            g.add((menu_item_url, tef.term('menus.description'), menuDesc))

        # menus amount max
        menusAmountMax = rdflib.Literal(menu_tup.menusAmountMax,
                                        datatype=XSD.decimal)
        g.add((menu_item_url, tef.term('menus.amountMax'), menusAmountMax))

        # menus amount min
        menusAmountMin = rdflib.Literal(menu_tup.menusAmountMin,
                                        datatype=XSD.decimal)
        g.add((menu_item_url, tef.term('menus.amountMin'), menusAmountMin))

    # add in the ingredients which we know about
    ingredient_df = get_menu_descriptions()
    for ingredient_tup in ingredient_df.itertuples():
        if not pd.isna(ingredient_tup.ingredient) \
                and not ingredient_tup.ingredient.strip() == '':
            ingredient_url = rdflib.URIRef(tef_url
                                           + ingredient_tup.id.strip())
            ingredient = tef.term(ingredient_tup.ingredient.strip())
            g.add((ingredient_url, tef.hasTopping, ingredient))

    # print the knowledge graph
    print_knowledge_graph(g)

    # save the knowledge graph
    g.serialize(format=destination_format, destination=destination)


if __name__ == '__main__':
    main()
