"""This is to select 5 pairs of entities and compare them"""
from gensim.models import KeyedVectors
import os

mainPath = 'ontologyEmbeddings'
"""The folder for ontology embeddings"""

pizzaDataEmbeddings = os.path.join(mainPath, 'pizzaData', 'cache',
                                   'outputontology.embeddings')
"""The path to the pizza data embeddings"""

pizzaDataNewSeedEmbeddings = os.path.join(mainPath, 'pizzaDataNewSeed',
                                          'cache',
                                          'outputontology.embeddings')
"""The path to the embeddings for the new seed"""

pizzaOntologyEmbeddings = os.path.join(mainPath, 'pizzaOntology', 'cache',
                                       'outputontology.embeddings')
"""The path to the embeddings to just the ontology"""


def main(word_pairs: list) -> list:
    """Here we look at 5 different entities and compare them

    Parameters
    ----------
    word_pairs: list
        Here we pass in a list of tuple pairs of words

    Returns
    -------
    list
        of strings to print out"""
    # load models
    pizzaDataModel = KeyedVectors.load(pizzaDataEmbeddings, mmap='r')
    pizzaDataNSModel = KeyedVectors.load(pizzaDataNewSeedEmbeddings, mmap='r')
    pizzaOntologyModel = KeyedVectors.load(pizzaOntologyEmbeddings, mmap='r')

    ret = []

    for word1, word2 in word_pairs:
        # pizza versus tef:margherita
        pizzaDataScore = pizzaDataModel.wv.similarity(word1, word2)
        pizzaDataNSScore = pizzaDataNSModel.wv.similarity(word1, word2)
        pizzaOntologyScore = pizzaOntologyModel.wv.similarity(word1, word2)
        out = f'{word1} vs {word2}: ' + str(pizzaDataScore) + ', ' \
              + str(pizzaDataNSScore) + ', ' + str(pizzaOntologyScore)
        ret.append(out)
    return ret


if __name__ == '__main__':
    url = 'http://link477.com/ds/pizza#'
    my_word_pairs = [
        ('pizza', url + 'margherita'),
        ('margherita', url + 'margherita'),
        ('pizza', url + 'pizza'),
        ('american', url + 'american'),
        ('pizzaiola', url + 'pizzaiola')
    ]
    for s in main(my_word_pairs):
        print(s)
