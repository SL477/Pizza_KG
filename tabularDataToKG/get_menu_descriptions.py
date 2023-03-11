"""This is to get the descriptions of the menu items to relate to ingredients
in the Knowledge graph"""
import pandas as pd
import os
import urllib.parse
from pizza_kg.data import get_org_data, OrgDataFiles


def find_ingredient(org: str, ingredient_dict: dict) -> str:
    """This is to find the ingredient from the KG if it exists

    Parameters
    ----------
    org: str
        The original string

    ingredient_dict: dict
        The map of strings to ingredients

    Returns
    -------
    str
        The matching value in the dictionary"""
    for key, value in ingredient_dict.items():
        if key in org.lower():
            return value
    return ''


def main() -> pd.DataFrame:
    """This splits up the ingredients column into multiple rows and maps them
    to the ingredients in the Knowledge graph

    Returns
    -------
    pd.DataFrame
        With the columns:
            - id
            - description
            - ingredient"""
    ret_df: pd.DataFrame = get_org_data(OrgDataFiles.MAIN)
    ret_df.rename(columns={'menus.description': 'menusDescription',
                           'menus.name': 'menusName'},
                  inplace=True)
    ret_df = ret_df[['id', 'menusDescription', 'menusName']]
    replace_list = [
        ('ampcomma', ','),
        (' ampamp ', ', '),
        (' & ', ', '),
        (' and ', ', ')
    ]
    for org, replace in replace_list:
        ret_df['menusDescription'] = ret_df.menusDescription.str.replace(
            org, replace)

    # load the map of ingredients
    ingredientMap = os.path.join('tabularDataToKG',
                                 'ingredientsMapping.xlsx')
    ingredient_df = pd.read_excel(ingredientMap, sheet_name='Sheet1',
                                  index_col='org')
    ingredient_dict = ingredient_df.to_dict()['MapTo']

    descs = []
    ids = []
    for tup in ret_df.itertuples():
        item_id = tup.id + urllib.parse.quote_plus(tup.menusName)
        if not pd.isna(tup.menusDescription):
            for desc in str(tup.menusDescription).split(', '):
                descs.append(desc)
                ids.append(item_id)
    ret_df = pd.DataFrame.from_dict({'id': ids, 'description': descs})
    ret_df['ingredient'] = ret_df.description.apply(find_ingredient,
                                                    args=(ingredient_dict,))
    return ret_df


if __name__ == '__main__':
    df = main()
    print(df)
    df.to_excel(os.path.join('tabularDataToKG', 'menu_descriptions.xlsx'),
                index=False)
