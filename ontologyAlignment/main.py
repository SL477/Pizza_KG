# imports
import os
import rdflib
from rdflib.namespace import RDF, RDFS, XSD, OWL

tef_url = 'http://link477.com/ds/pizza#'
pizza_url = 'http://co-ode.org/ontologies/pizza/pizza.owl#'
pizza_ontology_loc = os.path.join('orgData', 'pizza.owl')

g: rdflib.Graph = rdflib.Graph()
g.parse('ontology.owl', format='xml')

pizza_ontology = rdflib.Graph()
pizza_ontology.parse(pizza_ontology_loc, format='xml')

# for subj, obj in pizza_ontology.subject_objects(predicate=RDFS.subClassOf):
#     print(subj.rsplit('#')[-1])
pizza_classes = list(set([subj.rsplit('#')[-1] for subj, _ in
                          pizza_ontology.subject_objects(
                              predicate=RDFS.subClassOf)]))
print(pizza_classes)

tef_classes = list(set([subj.rsplit('#')[-1] for subj, _ in
                          g.subject_objects(predicate=RDFS.subClassOf)]))
print(tef_classes)

# set up the namespaces
tef = rdflib.Namespace(tef_url)
g.namespace_manager.bind('tef', tef)
pizza = rdflib.Namespace(pizza_url)
g.namespace_manager.bind('pizza', pizza)
g.parse(pizza_ontology_loc, format='xml')

for tef_class in tef_classes:
    try:
        ind = [c.lower() for c in pizza_classes].index(tef_class.lower())
        g.add((tef.term(tef_class), OWL.equivalentClass, pizza.term(pizza_classes[ind])))
    except:
        pass

#print(g.serialize(format='ttl'))
g.serialize(format='ttl',
            destination=os.path.join('ontologyAlignment',
                                     'alignedOntology.ttl'))