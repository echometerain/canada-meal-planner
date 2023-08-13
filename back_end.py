import pandas as pd
import numpy as np
from thefuzz import process
from typing import List

merged = pd.read_csv("./csv/merged.csv").set_index("FoodDescription")
nu_names = pd.read_csv("./csv/nu_name.csv").set_index("NutrientID")
nu_amounts = pd.read_csv("./csv/nu_amount.csv")
percent_e = pd.read_csv("./csv/percent_e.csv").set_index("Components")
daily = pd.read_csv("./csv/daily.csv")


def fuzzy_match(st: str) -> List[str]:
    """
    Args:
        st (str): partial string you want to complete

    Returns:
        List[str]: top ten completions, sorted descending based on likelihood
    """
    return [x[0] for x in process.extract(st, merged.index, limit=10)]


def check_daily(nu_dict: dict) -> dict:
    """
    Args:
        nu_dict (dict): output of get_nutrients()

    Returns:
        dict: {nutrient name: (amount - min, amount - good, amount - max)}
        values without data will return NaN
    """
    True


def convert_units(from_unit: str, to_unit: str, amount: float, kcal_type: str) -> float:  # for check_daily only
    if to_unit == "kCal":
        if kcal_type == "Protein" or kcal_type == "carbs":
            return amount*4
        elif kcal_type == "Fat":
            return amount


def get_nutrients(plan: dict) -> dict:
    """
    Args:
        plan (dict): day plan {food name: amount in grams}

    Returns:
        dict: {nutrient en name: (fr name, amount, unit)}
    """
    output = {}
    for k, v in plan.items():
        rows = nu_amounts.loc[nu_amounts.FoodID == merged.at[k, "FoodID"]]
        for i in range(rows.shape[0]):
            nu_name = nu_names.at[rows.iloc[i]["NutrientID"], "NutrientName"]
            nu_name_fr = nu_names.at[rows.iloc[i]
                                     ["NutrientID"], "NutrientNameF"]
            amount = v * rows.iloc[i]["NutrientValue"] * \
                merged.at[k, "ConversionFactorValue"]/100
            unit = nu_names.at[rows.iloc[i]["NutrientID"], "NutrientUnit"]
            if nu_name in output.values():
                output[nu_name][2] += amount
            else:
                output[nu_name] = (nu_name_fr, amount, unit)

    return output
