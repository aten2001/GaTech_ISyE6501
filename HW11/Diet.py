#
# Diet Problem
#

# import pandas, operator
import pandas as pd
import operator

# Import PuLP
from pulp import *

#
# DATA
#
data = pd.read_excel(r'diet.xls')
print(data.columns)

# Getting constraints for nutrients
Mins = data.iloc[-2:-1, 3:].values.tolist()[0]
Maxes = data.iloc[-1:, 3:].values.tolist()[0]

# Getting list of foods and nutrients
data = data.iloc[:-3,:]
Food = data.iloc[:,0].values.tolist()
Nutrient = data.columns[3:].values.tolist()

# Creating dictionaries to 1) match nutrients with constraints; 2) match foods with price
Min_dict = dict(zip(Nutrient, Mins))
Max_dict = dict(zip(Nutrient, Maxes))
Price_dict = dict(zip(data['Foods'], data['Price/ Serving']))

# Creating dict that matches each nutrient n to their own dict that has: the name of each 
# food and amount of nutrient n in it
Nutrient_dict = {n: dict(zip(data['Foods'], data[n])) for n in Nutrient}

#
# MODEL
#

# Creating the 'prob' object
prob = LpProblem("Diet", LpMinimize)

# Creating decision variables (embedding nonnegativity)
Food_Quantity = LpVariable.dicts("Quantity", Food, lowBound=0, cat='Continuous')

# Creating indicator variables if a food is chosen
Food_Chosen = LpVariable.dicts("Chosen", Food, 0, 1, cat='Binary')

# Objective function
prob += lpSum([Price_dict[f] * Food_Quantity[f] for f in Food])

# Creating min/max constraints:
for n in Nutrient:
    prob += lpSum([Nutrient_dict[n][f] * Food_Quantity[f] for f in Food]) >= Min_dict[n]
    prob += lpSum([Nutrient_dict[n][f] * Food_Quantity[f] for f in Food]) <= Max_dict[n]

# Creating min serving size constraint for chosen foods
for f in Food:
    prob += Food_Quantity[f] >= 0.1 * Food_Chosen[f]

# Creating celery or broccoli constraint
prob += Food_Chosen['Celery, Raw'] + Food_Chosen['Frozen Broccoli'] <= 1

# 
prob += Food_Chosen['Tofu'] + Food_Chosen['Roasted Chicken'] + \
        Food_Chosen['Poached Eggs'] + Food_Chosen['Scrambled Eggs'] + \
        Food_Chosen['Bologna,Turkey'] + Food_Chosen['Frankfurter, Beef'] + \
        Food_Chosen['Ham,Sliced,Extralean'] + Food_Chosen['Kielbasa,Prk'] + \
        Food_Chosen['Hamburger W/Toppings'] + Food_Chosen['Hotdog, Plain'] + \
        Food_Chosen['Pork'] + Food_Chosen['Sardines in Oil'] + \
        Food_Chosen['White Tuna in Water'] + Food_Chosen['Neweng Clamchwd'] + \
        Food_Chosen['New E Clamchwd,W/Mlk'] + Food_Chosen['Beanbacn Soup,W/Watr'] >= 3

#
# SOLUTION
#

# solving the LP using the default
prob.solve()

# printing diet
for var in prob.variables():
    if var.varValue > 0:
        print(var.name, "=", var.varValue)

# printing optimal expenditures
cost = value(prob.objective)
print("The total cost of the diet is: ${}".format(round(cost,2)))
