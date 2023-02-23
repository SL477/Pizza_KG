"""This is to create a dictionary of states to their codes"""
import os
import pandas as pd
from pickle import dump

def main():
    """Open the states csv file, build a dictionary and then save it"""
    df = pd.read_csv(os.path.join('tabularDataToKG', 'states.csv'))

    state_dict = {item.codes: item.states for item in df.itertuples()}

    with open(os.path.join('tabularDataToKG', 'state.pkl'), 'wb') as f:
        dump(state_dict, f)
    print(state_dict)


if __name__ == '__main__':
    main()