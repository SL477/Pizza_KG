"""This is to recreate the date from the aligned ontology"""
from sparqlAndReasoning.inference import inference
from tabularDataToKG.main import main as tabularDataToKGMain
import os


def main():
    """This is to recreate the data from the aligned ontology"""
    aligned_ontology = os.path.join('ontologyAlignment',
                                    'mainAlignedOntology.ttl')
    tabularDataToKGMain(original_location=aligned_ontology,
                        original_format='ttl',
                        destination='dataPreReasoning.ttl',
                        destination_format='ttl')
    # inference(original_location='dataPreReasoning.ttl', original_format='ttl',
    #          destination='data.ttl', destination_format='ttl')


if __name__ == '__main__':
    main()
