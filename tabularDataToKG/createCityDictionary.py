"""This is to create a dictionary of states to their codes"""
import os
import pandas as pd
from pickle import dump

def main():
    """Open the states csv file, build a dictionary and then save it"""
    df = pd.read_excel(os.path.join('tabularDataToKG', 'urlsPlain.xlsx'))

    city_dict = {item.city + '_' + item.province: item.CityURL for item in df.itertuples()}

    with open(os.path.join('tabularDataToKG', 'city.pkl'), 'wb') as f:
         dump(city_dict, f)
    print(city_dict)


if __name__ == '__main__':
    main()
