import pandas as pd
import numpy as np
import thefuzz as fw
from typing import List

merged = pd.read_csv("./csv/merged.csv").set_index("FoodDescription")
nu_names = pd.read_csv("./csv/nu_name.csv").set_index("NutrientID")
nu_amounts = pd.read_csv("./csv/nu_amount.csv")
daily = pd.read_csv("./csv/daily.csv")
units = {
    # Unit: micrograms amount
}


def fuzzy_match(st: str) -> List[int]:
    """
    Args:
        st (str): partial string you want to complete

    Returns:
        List[int]: completed strings, sorted descending based on likelihood
    """
    True


def check_daily(nu_dict: dict) -> dict:
    """
    Args:
        nu_dict (dict): output of get_nutrients()

    Returns:
        dict: {nutrient name: (amount - min, amount - good, amount - max)}
        values without data will return NaN
    """
    True


def convert_units(from_unit: str, to_unit: str, amount: float) -> float:
    True


def get_nutrients(plan: dict) -> dict:
    """
    Args:
        plan (dict): day plan {food name: (amount, units)}

    Returns:
        dict: {nutrient name: amount in micrograms}
    """
    output = {}
    for k, v in plan.items():
        for _, row in nu_amounts.loc[nu_amounts.FoodID == merged.at[k, "FoodID"]]:
            nu_name = nu_names.at[row["NutrientID"], "NutrientName"]
            unit = nu_names.at[row["NutrientID"], "NutrientUnit"]
            nu_amount = v[1]*convert_units()

    return output
