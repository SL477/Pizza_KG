"""This is to clean the menu items data"""
import pandas as pd
import pprint
import os
from pizza_kg.data import get_org_data, OrgDataFiles
import re


def find_pizza(org: str, pizza_dict: dict) -> str:
    """This looks for the pizza in the dictionary

    Parameters
    ----------
    org: str
        The original string

    pizza_dict: dict
        The dictionary to look in

    Returns
    -------
    str
        The matching value in the dictionary"""
    if org.lower() == 'pizza':
        return 'pizza'
    for key, value in pizza_dict.items():
        if key.lower() in org.lower():
            return value
    return 'pizza'


def main() -> pd.DataFrame:
    """This is to get the cleaned menu items

    Returns
    -------
    pd.DataFrame
        The cleaned menu items columns:
        - menusAmountMax
        - menusAmountMin
        - menusDateSeen
        - menusDescription
        - menusName
        - menusCurrency"""
    ret_df: pd.DataFrame = get_org_data(OrgDataFiles.MAIN)
    menu_item_cols = [
        'menus.amountMax',
        'menus.amountMin',
        'menus.dateSeen',
        'menus.description',
        'menus.name',
        'menus.currency',
        'id'
    ]
    ret_df = ret_df[menu_item_cols].copy()
    ret_df.rename(columns={
        'menus.amountMax': 'menusAmountMax',
        'menus.amountMin': 'menusAmountMin',
        'menus.dateSeen': 'menusDateSeen',
        'menus.description': 'menusDescription',
        'menus.name': 'menusName',
        'menus.currency': 'menusCurrency'
    }, inplace=True)

    # replace items
    replace_list = [
        ('ampcomma', ','),
        (' and ', ', '),
        ('ampquot', '"'),
        ('ampamp', '&')
    ]
    for org_str, replace_str in replace_list:
        ret_df['menusDescription'] = ret_df['menusDescription']\
            .str.replace(org_str, replace_str)
        ret_df['menusName'] = ret_df['menusName']\
            .str.replace(org_str, replace_str)

    # load the map of pizzas
    pizzaMap = os.path.join('tabularDataToKG', 'pizzaMapping.xlsx')
    pizza_df = pd.read_excel(pizzaMap, sheet_name='Sheet1', index_col='org')
    # print(pizza_df)
    pizza_dict = pizza_df.to_dict()['MapTo']
    # print(pizza_dict)
    ret_df['menuItem'] = ret_df['menusName'].apply(find_pizza,
                                                   args=(pizza_dict,))

    ret_df['pizzaSize'] = ret_df['menusName'].str.extract(
        r'((\d+)"|(\d+) inch)',
        expand=False,
        flags=re.IGNORECASE)[0]
    ret_df['pizzaSize'] = ret_df['pizzaSize'].str.strip('"').str.lower()\
        .str.strip(' inch')
    return ret_df


if __name__ == '__main__':
    df: pd.DataFrame = main()
    pprint.pprint(df)
    df.to_excel(
        os.path.join('tabularDataToKG', 'clean_menu_items.xlsx'),
        index=False)
