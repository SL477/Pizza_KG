# %%
"""Here we look at getting clusters for the embeddings"""
import gensim.models.keyedvectors
from gensim.models import KeyedVectors
import os
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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


def get_model_graph(mdl: gensim.models.keyedvectors.Word2VecKeyedVectors,
                    file_name: str) -> None:
    """Here we use PCA to project out data to 2D, then use KMeans clustering
    to get its cluster

    Parameters
    ----------
    mdl: gensim.models.keyedvectors.Word2VecKeyedVectors
        The saved model

    file_name: str
        The name of the file to save to

    Returns
    -------
    None
        Saves to file in the parameter"""
    data = []
    url = 'http://link477.com/ds/pizza#'
    out_data = {
        'x': [],
        'y': [],
        'c': [],
        'w': []
    }
    for word in mdl.wv.vocab:
        if url in word:
            out_data['w'].append(word)
            data.append(mdl.wv[word])
    p = PCA(n_components=2).fit_transform(data)
    k = KMeans(n_clusters=8).fit_transform(data)
    for idx, w in enumerate(out_data['w']):
        d = p[idx].tolist()
        out_data['x'].append(d[0])
        out_data['y'].append(d[1])
    out_data['c'] = k.argmax(axis=1)

    plt.scatter(out_data['x'], out_data['y'], c=out_data['c'])
    plt.title('Pizza NS Clusters')
    plt.savefig(os.path.join('images', file_name + '.png'))


def main() -> None:
    """Here we look at getting clusters for the embeddings

    Returns
    -------
    None
        Saves to various files in the images folder"""
    # load models
    pizzaDataModel = KeyedVectors.load(pizzaDataEmbeddings, mmap='r')
    pizzaDataNSModel = KeyedVectors.load(pizzaDataNewSeedEmbeddings, mmap='r')
    pizzaOntologyModel = KeyedVectors.load(pizzaOntologyEmbeddings, mmap='r')

    get_model_graph(pizzaDataModel, 'pizzaDataModelClusters')
    get_model_graph(pizzaDataNSModel, 'pizzaDataNSModelClusters')
    get_model_graph(pizzaOntologyModel, 'pizzaOntologyModelClusters')


if __name__ == '__main__':
    main()
