import pandas as pd
import numpy as np
from thefuzz import process
from typing import List

merged = pd.read_csv("./csv/merged.csv").set_index("FoodDescription")
nu_names = pd.read_csv("./csv/nu_name.csv").set_index("NutrientID")
nu_amounts = pd.read_csv("./csv/nu_amount.csv")
percent_e = pd.read_csv("./csv/percent_e.csv")
daily = pd.read_csv("./csv/daily.csv")
ages = [0, 0.5, 1, 4, 9, 14, 19, 31, 51, 70]
ages_pl = [0, 19, 31]
units = {  # in mg
    "g": 1000.0,
    "mg": 1.0,
    "μg": 0.001
}


def fuzzy_match(st: str) -> List[str]:
    """
    Args:
        st (str): partial string you want to completes

    Returns:
        List[str]: top ten completions, sorted descending based on likelihood
    """
    return [x[0] for x in process.extract(st, merged.index, limit=10)]


def check_daily(nu_dict: dict, age: float, female: bool, pregnant: bool, lactating: bool) -> dict:
    """
    Args:
        nu_dict (dict): output of get_nutrients()

        input sex not gender

    Returns:
        dict: {nutrient name: (amount - min, amount - good, amount - max, units)} general component daily intake

        dict: {nutrient name: (amount - min, amount - max)} component percent energy

        values without data will return NaN
    """
    comp_names = np.array(list(nu_dict.keys()))
    daily_n = np.intersect1d(comp_names, np.unique(daily["Components"]))
    percent_e_n = np.intersect1d(comp_names, percent_e["Components"])
    output = {}
    output_pe = {}
    ptype = ""
    age_i = 0
    if pregnant or lactating:
        for i in range(len(ages_pl)):
            if age > ages_pl[i]:
                age_i = i
            elif pregnant:
                ptype = f"{ages_pl[age_i]} p"
                break
            else:
                ptype = f"{ages_pl[age_i]} l"
                break
    else:
        for i in range(len(ages)):
            if age > ages[i]:
                age_i = i
            elif age > 4:
                ptype = str(ages[age_i]) + "f" if female else "m"
            else:
                ptype = str(ages[age_i])

    for e in daily_n:
        mgm = daily.loc[daily["Components"] == e]
        mgm = mgm.loc[mgm.Unit.isin(["g", "mg", "μg"])].set_index("Type")
        min_diff = np.nan
        good_diff = np.nan
        max_diff = np.nan
        if "Min" in mgm.index:
            min_diff = convert_units(
                nu_dict[e][2], mgm.at["Min", "Unit"], nu_dict[e][1]) - mgm.at["Min", ptype]
        if "Good" in mgm.index:
            good_diff = convert_units(
                nu_dict[e][2], mgm.at["Good", "Unit"], nu_dict[e][1]) - mgm.at["Good", ptype]
        if "Max" in mgm.index:
            max_diff = convert_units(
                nu_dict[e][2], mgm.at["Max", "Unit"], nu_dict[e][1]) - mgm.at["Max", ptype]
        output[e] = (min_diff, good_diff, max_diff)
    for e in percent_e_n:
        mm = percent_e.loc[percent_e["Components"] == e].set_index("Type")
        min_diff = get_e_percent(
            nu_dict["Energy"][1], nu_dict[e][1], e) - mm.at["Min", ptype]
        max_diff = get_e_percent(
            nu_dict["Energy"][1], nu_dict[e][1], e) - mm.at["Max", ptype]
        output_pe[e] = (min_diff, max_diff)

    return output, output_pe


def convert_units(from_unit: str, to_unit: str, amount: np.double) -> np.double:  # for check_daily only
    return amount * units[to_unit] / units[from_unit]


def get_e_percent(energy: np.double, amount: np.double, kcal_type: str) -> np.double:
    if kcal_type == "Total Protein" or kcal_type == "Total Carbohydrate":
        return amount*4/energy
    elif kcal_type == "Total Fat":
        return amount/energy


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


print(check_daily(get_nutrients(
    {fuzzy_match("fish")[0]: 5000}), 25, True, False, True))
