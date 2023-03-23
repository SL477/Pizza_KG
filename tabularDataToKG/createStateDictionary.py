"""This is to create a dictionary of states to their codes"""
import os
import pandas as pd
from pickle import dump


def main() -> None:
    """Open the states csv file, builds a dictionary and then saves it
    to state.pkl. The dictionary has the the state code as the key and the
    DBPedia URL as the value

    Returns
    -------
    None
        Saves to state.pkl"""
    df = pd.read_csv(os.path.join('tabularDataToKG', 'states.csv'))

    state_dict = {item.codes: item.states for item in df.itertuples()}

    with open(os.path.join('tabularDataToKG', 'state.pkl'), 'wb') as f:
        dump(state_dict, f)
    print(state_dict)


if __name__ == '__main__':
    main()
