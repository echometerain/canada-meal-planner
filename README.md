<h1 align="center">
  <img src="https://github.com/echometerain/canada-meal-planner/assets/70437021/0d27df36-baee-4798-810e-b24ae241fd10" width=200px height=200px/>
</h1>
<h1 align="center">
  Canada Meal Planner
</h1>

Our submission to Recess Hacks 3.0 is this open-source meal-planning app established around the dietary guidelines provided by Health Canada. Canada Meal Planner stands at the **forefront** of your health journey, helping you become a better version of yourself. 

We strive to make **stress-free**, **accessible** healthy eating available to **everyone**, through our **user-friendly** interface and **intuitive** features. Users can enter their meals into a daily notebook, after which they receive a full macronutrient & vitamin breakdown that details how much fat, protein, carbohydrates, and other vitamins they are consuming. 

Users can find inspiration through our leaderboard system, where they can engage in **friendly competitions** with their friends regarding their eating habits, and through our achievement system, which recognizes users for their remarkable efforts.

Users can also search through thousands of healthy recipes in the catalog, which provides the full recipe, along with the full macronutrient & vitamin breakdown that details how much fat, protein, carbohydrates, and other vitamins they are consuming. 

This project pulls from the 2015 release of the [Canadian Nutrient File](https://www.canada.ca/en/health-canada/services/food-nutrition/healthy-eating/nutrient-data/canadian-nutrient-file-2015-download-files.html) (csv) and data scraped from Health Canada's [Dietary reference intakes tables](https://www.canada.ca/en/health-canada/services/food-nutrition/healthy-eating/dietary-reference-intakes/tables.html). This data was processed and cleaned using Libreoffice Calc, Kate (KDE text editor), Jupyter Notebooks, Numpy, and Pandas. The (currently unfinished) frontend was built with [Figma](https://www.figma.com/file/RwlNNQGx7ZAKdBrzsuS47g/Recess-Hacks---Canada-Meal-Planner?type=design&node-id=0%3A1&mode=design&t=ieK8M0aAKilz1f2M-1), CustomTkInter, TkInter, Pillow, and Rich. The (finished, documented) backend and CLI was built with Numpy, Pandas, TheFuzz, Typer, and Rich. The CLI support fuzzy searching and French.

View CLI features and docs with: `python ./back_end.py --help`

Must be installed with python 3.11

Install dependencies: `pip install -r requirements.txt`
