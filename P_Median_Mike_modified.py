# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 11:04:01 2018

P-Median Python example
"""
#from pulp import LpProblem, LpVariable, LpInteger, LpMinimize, LpStatus, value, lpsum
from pulp import* 

# set up variables
location = ['Loc1','Loc2','Loc3','Loc4','Loc5','Loc6']
demand = ['dem1','dem2','dem3','dem4','dem5','dem6']
D = dict(zip(demand,[dict(zip(location, [0, 5.6, 17.4, 21.8, 19.4, 11.4])),
dict(zip(location, [5.6, 0, 11.6, 19.6, 21.7, 13])),
dict(zip(location, [17.4, 11.6, 0, 8, 18.3, 16.8])),
dict(zip(location, [21.8, 19.6, 8, 0, 16.9, 20.1])),
dict(zip(location, [19.4, 21.7, 18.3, 16.9, 0, 13.6])),
dict(zip(location, [11.4, 13, 16.8, 20.1, 13.6, 0]))]))
print D



p = 1  #  number of locations to optimize to

# decision variables
# This is same as X = LpVariable.dicts('X_%s_%s', (location), cat = 'Binary', lowBound = 0, upBound = 1)
# but shorter and a format speficier is not needed.
X = LpVariable.dicts('X',(location),0,1, LpInteger)

# this is same X = LpVariable.dicts('X_%s_%s', (location,location), cat = 'Binary', lowBound = 0, upBound = 1)
# but shorter and a format speficier is not needed.
# declare distance variables
Y = LpVariable.dicts('Y', (demand,location),0,1,LpInteger) 

print X

# create the LP object, set up as a MINIMIZATION problem
prob = LpProblem('P Median', LpMinimize)
prob += sum(sum(D[i][j] * Y[i][j] for j in location) for i in demand)

#  set up constraints
#  This is same as prob += sum([X[j] for j in location]) == p
prob += lpSum([X[j] for j in location]) == p

for i in demand: prob += sum(Y[i][j] for j in location) == 1
for i in demand:
    for j in location: 
        prob +=  Y[i][j] <= X[j]
       

prob.solve()

#  format output
print(' ')
print("Status:",LpStatus[prob.status])
print(' ')
print("Objective: ",value(prob.objective))
print(' ')

for v in prob.variables():
    subV = v.name.split('_')
    
    if subV[0] == "X" and v.varValue == 1: print('p-Median Node: ', subV[1])
        
print(' ')
for v in prob.variables():
    subV = v.name.split('_')
    if subV[0] == "Y" and v.varValue == 1: print(subV[1], ' is connected to', subV[2] )    
    

