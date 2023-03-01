"""This is to clean the menu items data"""
import pandas as pd
import pprint
import os
from pizza_kg.data import get_org_data, OrgDataFiles


def main() -> pd.DataFrame:
    """This is to get the cleaned menu items

    Returns
    -------
    pd.DataFrame
        The cleaned menu items"""
    ret_df: pd.DataFrame = get_org_data(OrgDataFiles.MAIN)
    menu_item_cols = [
        'menus.amountMax',
        'menus.amountMin',
        'menus.dateSeen',
        'menus.description',
        'menus.name'
    ]
    ret_df = ret_df[menu_item_cols].copy()
    ret_df.rename(columns={
        'menus.amountMax': 'menusAmountMax',
        'menus.amountMin': 'menusAmountMin',
        'menus.dateSeen': 'menusDateSeen',
        'menus.description': 'menusDescription',
        'menus.name': 'menusName'
    }, inplace=True)

    # replace items
    replace_list = [
        ('ampcomma', ','),
        (' and ', ', '),
        ('ampquot', '"')
    ]
    for org_str, replace_str in replace_list:
        ret_df['menusDescription'] = ret_df['menusDescription']\
            .str.replace(org_str, replace_str)
        ret_df['menusName'] = ret_df['menusName']\
            .str.replace(org_str, replace_str)
    return ret_df


if __name__ == '__main__':
    df: pd.DataFrame = main()
    pprint.pprint(df)
    df.to_excel(
        os.path.join('tabularDataToKG', 'clean_menu_items.xlsx'),
        index=False)
