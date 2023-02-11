#%%
%load_ext autoreload
%autoreload 2
#%% imports
from pizza_kg.data import OrgDataFiles, get_orgData, get_Graph
from rdflib import Graph
import pprint
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
# %%

for stmt in g:
    pprint.pprint(stmt)
# %%
