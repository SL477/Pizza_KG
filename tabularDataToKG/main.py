# %% Setup
%load_ext autoreload
%autoreload
# %% imports
from pizza_kg.data import OrgDataFiles, get_orgData, get_Graph
from rdflib import Graph
import rdflib
from rdflib.namespace import RDF, RDFS, XSD
import pprint
import urllib.parse

tef = rdflib.Namespace('http://link477.com/ds/pizza#')
g.namespace_manager.bind('tef', tef)
# %% get the CSV data
df = get_orgData(OrgDataFiles.MAIN)
df.head()
# %% Get the Knowledge Graph
# https://rdflib.readthedocs.io/en/stable/
# g.serialize(destination="tbl.ttl") # save as ttl
# g.serialize(format="xml") # save as rdf/xml

# https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html
g: Graph = get_Graph()
g
# %% print the Knowledge Graph

for stmt in g:
    pprint.pprint(stmt)

# %% start adding States to knowledge graph
g: Graph = get_Graph()
for state in df.province.unique():
    # set up the data
    province = rdflib.URIRef(f'http://link477.com/ds/pizza#{state}')
    label = rdflib.Literal(state, datatype=XSD.string)
    comment = rdflib.Literal(f'The US state with a code of {state}', datatype=XSD.string)

    g.add((province, RDF.type, tef.province))
    g.add((province, RDFS.label, label))
    g.add((province, RDFS.comment, comment))
    g.add((province, tef.provinceLocatedIn, tef.US))

print(g.serialize(format='ttl'))

# %% get the cities and states
for _, city, province, _ in df[['city', 'province']].value_counts().reset_index().itertuples():
    # print('city', city, 'province', province)
    city_url = city.replace(' ', '_')    
    city_url = rdflib.URIRef(f'http://link477/ds/pizza#{city_url}')
    print(city_url, city, type(city))
    label = rdflib.Literal(city, datatype=XSD.string)
    comment = rdflib.Literal(f'The city of {city} in {province}', datatype=XSD.string)

    g.add((city_url, RDF.type, tef.city))
    g.add((city_url, RDFS.label, label))
    g.add((city_url, RDFS.comment, comment))
    g.add((city_url, tef.cityLocatedIn, rdflib.URIRef(f'http://link477/ds/pizza#{province}')))

print(g.serialize(format='ttl'))

# %% Save
g.serialize(format='ttl', destination='ontology_ttl.owl')
# %%
