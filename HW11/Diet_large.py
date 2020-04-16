#
# Diet large Problem
#

# import pandas, operator
import pandas as pd
import operator

# Import PuLP
from pulp import *

#
# DATA SECTION
#
data = pd.read_excel(r'diet_large.xls')
print(data.columns)

# dropping Fats as they are embedded in the Cholesterol variable
data = data.drop(['Fatty acids, total trans', 'Fatty acids, total saturated'], axis=1)

# counting missing cases by column
data.isnull().sum()

# dropping columns with at least 30% of missing cases
data = data.drop(['Vitamin E (alpha-tocopherol)', 'Vitamin D', 'Vitamin K (phylloquinone)'], axis=1)

# assigning 0s to remaining missing cases
data = data.fillna(0)

# drop last four rows
data = data[:-4]

# Creating list of foods
Food = list(data['Long_Desc'])

# Create dictionaries
Cholesterol = dict(zip(Food, data['Cholesterol']))
Protein = dict(zip(Food, data['Protein']))
Carbohydrates = dict(zip(Food, data['Carbohydrate, by difference']))
Energy1 = dict(zip(Food, data['Energy1']))
Water = dict(zip(Food, data['Water']))
Energy2 = dict(zip(Food, data['Energy2']))
Calcium = dict(zip(Food, data['Calcium, Ca']))
Iron = dict(zip(Food, data['Iron, Fe']))
Magnesium = dict(zip(Food, data['Magnesium, Mg']))
Phosphorus = dict(zip(Food, data['Phosphorus, P']))
Potassium = dict(zip(Food, data['Potassium, K']))
Sodium = dict(zip(Food, data['Sodium, Na']))
Zinc = dict(zip(Food, data['Zinc, Zn']))
Copper = dict(zip(Food, data['Copper, Cu']))
Manganese = dict(zip(Food, data['Manganese, Mn']))
Selenium = dict(zip(Food, data['Selenium, Se']))
Vitamin_A = dict(zip(Food, data['Vitamin A, RAE']))
Vitamin_C = dict(zip(Food, data['Vitamin C, total ascorbic acid']))
Vitamin_B1 = dict(zip(Food, data['Thiamin']))
Vitamin_B2 = dict(zip(Food, data['Riboflavin']))
Vitamin_B3 = dict(zip(Food, data['Niacin']))
Vitamin_B5 = dict(zip(Food, data['Pantothenic acid']))
Vitamin_B6 = dict(zip(Food, data['Vitamin B-6']))
Vitamin_B9 = dict(zip(Food, data['Folate, total']))
Vitamin_B12 = dict(zip(Food, data['Vitamin B-12']))

#
# MODEL SECTION
#

# Creating the 'prob' object
prob = LpProblem("Diet", LpMinimize)

# Creating decision variables (embedding nonnegativity)
Food_Quantity = LpVariable.dicts("Quantity", Food, lowBound=0, cat='Continuous')

# Creating indicator variables if a food is chosen
Food_Chosen = LpVariable.dicts("Chosen", Food, 0, 1, cat='Binary')

# Objective function
prob += lpSum([Cholesterol[f] * Food_Quantity[f] for f in Food])

# Creating max/min constraints
prob += lpSum([Protein[f] * Food_Quantity[f] for f in Food]) >= 56.0
prob += lpSum([Protein[f] * Food_Quantity[f] for f in Food]) <= 1000000.0
prob += lpSum([Carbohydrates[f] * Food_Quantity[f] for f in Food]) >= 130.0
prob += lpSum([Carbohydrates[f] * Food_Quantity[f] for f in Food]) <= 1000000.0
prob += lpSum([Energy1[f] * Food_Quantity[f] for f in Food]) >= 2400.0
prob += lpSum([Energy1[f] * Food_Quantity[f] for f in Food]) <= 1000000.0
prob += lpSum([Water[f] * Food_Quantity[f] for f in Food]) >= 3700.0
prob += lpSum([Water[f] * Food_Quantity[f] for f in Food]) <= 1000000.0
prob += lpSum([Energy2[f] * Food_Quantity[f] for f in Food]) >= 2400.0
prob += lpSum([Energy2[f] * Food_Quantity[f] for f in Food]) <= 1000000.0
prob += lpSum([Calcium[f] * Food_Quantity[f] for f in Food]) >= 1000.0
prob += lpSum([Calcium[f] * Food_Quantity[f] for f in Food]) <= 2500.0
prob += lpSum([Iron[f] * Food_Quantity[f] for f in Food]) >= 8.0
prob += lpSum([Iron[f] * Food_Quantity[f] for f in Food]) <= 45.0
prob += lpSum([Magnesium[f] * Food_Quantity[f] for f in Food]) >= 270.0
prob += lpSum([Magnesium[f] * Food_Quantity[f] for f in Food]) <= 400.0
prob += lpSum([Phosphorus[f] * Food_Quantity[f] for f in Food]) >= 700.0
prob += lpSum([Phosphorus[f] * Food_Quantity[f] for f in Food]) <= 4000.0
prob += lpSum([Potassium[f] * Food_Quantity[f] for f in Food]) >= 4700.0
prob += lpSum([Potassium[f] * Food_Quantity[f] for f in Food]) <= 1000000.0
prob += lpSum([Sodium[f] * Food_Quantity[f] for f in Food]) >= 1500.0
prob += lpSum([Sodium[f] * Food_Quantity[f] for f in Food]) <= 2300.0
prob += lpSum([Zinc[f] * Food_Quantity[f] for f in Food]) >= 11.0
prob += lpSum([Zinc[f] * Food_Quantity[f] for f in Food]) <= 40.0
prob += lpSum([Copper[f] * Food_Quantity[f] for f in Food]) >= 0.9
prob += lpSum([Copper[f] * Food_Quantity[f] for f in Food]) <= 10.0
prob += lpSum([Manganese[f] * Food_Quantity[f] for f in Food]) >= 2.3
prob += lpSum([Manganese[f] * Food_Quantity[f] for f in Food]) <= 11
prob += lpSum([Selenium[f] * Food_Quantity[f] for f in Food]) >= 55
prob += lpSum([Selenium[f] * Food_Quantity[f] for f in Food]) <= 400.0
prob += lpSum([Vitamin_A[f] * Food_Quantity[f] for f in Food]) >= 900.0
prob += lpSum([Vitamin_A[f] * Food_Quantity[f] for f in Food]) <= 3000.0
prob += lpSum([Vitamin_C[f] * Food_Quantity[f] for f in Food]) <= 90.0
prob += lpSum([Vitamin_C[f] * Food_Quantity[f] for f in Food]) <= 2000.0
prob += lpSum([Vitamin_B1[f] * Food_Quantity[f] for f in Food]) <= 0.0012
prob += lpSum([Vitamin_B1[f] * Food_Quantity[f] for f in Food]) <= 1000000.0
prob += lpSum([Vitamin_B2[f] * Food_Quantity[f] for f in Food]) <= 1.3
prob += lpSum([Vitamin_B2[f] * Food_Quantity[f] for f in Food]) <= 1000000
prob += lpSum([Vitamin_B3[f] * Food_Quantity[f] for f in Food]) <= 16.0
prob += lpSum([Vitamin_B3[f] * Food_Quantity[f] for f in Food]) <= 35.0
prob += lpSum([Vitamin_B5[f] * Food_Quantity[f] for f in Food]) <= 5.0
prob += lpSum([Vitamin_B5[f] * Food_Quantity[f] for f in Food]) <= 1000000.0
prob += lpSum([Vitamin_B6[f] * Food_Quantity[f] for f in Food]) <= 1.3
prob += lpSum([Vitamin_B6[f] * Food_Quantity[f] for f in Food]) <= 100
prob += lpSum([Vitamin_B9[f] * Food_Quantity[f] for f in Food]) <= 400.0
prob += lpSum([Vitamin_B9[f] * Food_Quantity[f] for f in Food]) <= 1000.0
prob += lpSum([Vitamin_B12[f] * Food_Quantity[f] for f in Food]) <= 2.4
prob += lpSum([Vitamin_B12[f] * Food_Quantity[f] for f in Food]) <= 1000000.0

#
# SOLUTION SECTION
#

# solving the LP using the default
prob.solve()

# printing diet
for var in prob.variables():
    if var.varValue > 0:
        print(var.name, "=", var.varValue)

# printing optimal expenditures
cost = value(prob.objective)
print("The total cholesterol of the diet is: {}".format(round(cost,2)))
