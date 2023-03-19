# imports
import os

import rdflib
from rdflib.namespace import RDFS, OWL

tef_url = 'http://link477.com/ds/pizza#'
pizza_url = 'http://www.co-ode.org/ontologies/pizza/pizza.owl#'
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

# mini aligned ontology
mini_aligned = rdflib.Graph()
mini_aligned.namespace_manager.bind('tef', tef)
mini_aligned.namespace_manager.bind('pizza', pizza)

# main aligned ontology
main_aligned = rdflib.Graph()
main_aligned.parse(os.path.join('ontologyAlignment', 'ontology.owl'),
                   format='xml')
main_aligned.namespace_manager.bind('tef', tef)
main_aligned.namespace_manager.bind('pizza', pizza)

for tef_class in tef_classes:
    try:
        ind = [c.lower() for c in pizza_classes].index(tef_class.lower())
        if tef_class.lower() == 'capricciosa':
            continue
        mini_aligned.add((tef.term(tef_class), OWL.equivalentClass,
                          pizza.term(pizza_classes[ind])))
        main_aligned.add((tef.term(tef_class), OWL.equivalentClass,
                          pizza.term(pizza_classes[ind])))
    except:
        pass

otherEqivalentClasses = [
    ('menuItem', 'Food'),
    # ('quattroStagioni', 'FourSeasons'),
    ('parmese', 'Parmense'),
    # ('sicilian', 'Siciliana'),
    ('cheese', 'CheeseTopping'),
    ('meat', 'MeatTopping'),
    ('seafood', 'FishTopping'),
    ('anchovies', 'AnchoviesTopping'),
    ('mixedSeafood', 'MixedSeafoodTopping'),
    ('prawns', 'PrawnsTopping'),
    ('goatsCheese', 'GoatsCheeseTopping'),
    ('gorgonzola', 'GorgonzolaTopping'),
    ('mozzarella', 'MozzarellaTopping'),
    ('parmezan', 'ParmesanTopping'),
    ('sultana', 'SultanaTopping'),
    ('cajunSpice', 'CajunSpiceTopping'),
    ('rosemary', 'RosemaryTopping'),
    ('chicken', 'ChickenTopping'),
    ('ham', 'HamTopping'),
    ('hotSpicedBeef', 'HotSpicedBeefTopping'),
    ('pepperoni', 'PeperoniSausageTopping'),
    ('pineKernel', 'PineKernels'),
    ('artichokes', 'ArtichokeTopping'),
    ('asparagus', 'AsparagusTopping'),
    ('capers', 'CaperTopping'),
    ('garlic', 'GarlicTopping'),
    ('leek', 'LeekTopping'),
    ('mushrooms', 'MushroomTopping'),
    ('olives', 'OliveTopping'),
    ('onion', 'OnionTopping'),
    ('pepper', 'PepperTopping'),
    ('hotGreenPepper', 'HotGreenPepperTopping'),
    ('jalapenoPepper', 'JalapenoPepperTopping'),
    ('peperonata', 'PeperonataTopping'),
    ('sweetPepper', 'SweetPepperTopping'),
    ('petitPois', 'PetitPoisTopping'),
    ('rocket', 'RocketTopping'),
    ('spinach', 'SpinachTopping'),
    ('tomato', 'TomatoTopping'),
    ('sundriedTomato', 'SundriedTomatoTopping'),
    ('country', 'Country'),
    ('fruitTopping', 'FruitTopping')
]
for t_class, p_class in otherEqivalentClasses:
    mini_aligned.add((tef.term(t_class), OWL.equivalentClass,
                      pizza.term(p_class)))
    main_aligned.add((tef.term(t_class), OWL.equivalentClass,
                      pizza.term(p_class)))

# sub-properties
equivalentSubProperties = [
    ('isIngredientOf', 'isIngredientOf'),
    ('isBaseOf', 'isBaseOf'),
    ('isToppingOf', 'isToppingOf'),
    ('hasIngredient', 'hasIngredient'),
    ('hasBase', 'hasBase'),
    ('hasTopping', 'hasTopping')
]
for t_prop, p_prop in equivalentSubProperties:
    mini_aligned.add((tef.term(t_prop), OWL.equivalentProperty,
                      pizza.term(p_prop)))
    main_aligned.add((tef.term(t_prop), OWL.equivalentProperty,
                      pizza.term(p_prop)))

# print(g.serialize(format='ttl'))
mini_aligned.serialize(format='ttl',
                       destination=os.path.join('ontologyAlignment',
                                                'miniAlignedOntology.ttl'))
main_aligned.serialize(format='ttl',
                       destination=os.path.join('ontologyAlignment',
                                                'mainAlignedOntology.ttl'))
