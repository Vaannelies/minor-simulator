'''
====== Legal notices

Copyright (C) 2013 - 2021 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicense for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html

__________________________________________________________________________


 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your license.
'''

import os
import sys as ss

ss.path.append (os.path.abspath ('../../..')) # If you want to store your simulations somewhere else, put SimPyLC in your PYTHONPATH environment variable

import simpylc as sp

import lidar_pilot_simulated_io as ls
import lidar_pilot_real_io as lr
import physics as ps
import visualisation as vs
import zzz_alternatives.control as c
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import numpy as np


df = pd.read_excel('D:\Annelies\Documenten\HR\JAAR 4\Minor\minor-simulator\simulations\car\data\data1.xlsx');
# print(df);
data = df.to_numpy()
print('data', data)
# data = np.loadtxt('D:\Annelies\Documenten\HR\JAAR 4\Minor\minor-simulator\simulations\data\data.csv', delimiter=";")
# data = np.loadtxt('D:\Annelies\Documenten\HR\JAAR 4\Minor\minor-simulator\simulations\car\data\data1.xlsx', delimiter=";")
# data[:1]

# print('data', data)


# print("\n")
# for row in data:
#     result = ''
#     for column in row:
#         result += str(column) + "\t"
#     print(result)
#     print("\n")

# print("\n")

yColumn = [0 for item in data]      # output node values
for index, row in enumerate(data): 
    yColumn[index] += row[len(row)-1]
# print('yColumn', yColumn)

xColumns = []           # input nodes values
for index, row in enumerate(data):
    xColumns.append([])
    items = []
    for index, column in enumerate(row):
        if index < len(row)-1:
            items.append(column)
    xColumns[len(xColumns)-1] = items


x = xColumns
y = yColumn 
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = 1)
regr = MLPRegressor(
    hidden_layer_sizes=(64,64,64),
    # activation="relu",
    random_state = 1, 
    max_iter = 500, 
    ).fit(x_train, y_train)
# regr.add(layers.Dense(10, activation='relu'))









# print('xtest', x_test)
# print('ytest', y_test)

print()                     # wat betekent dit 
print('predict', regr.predict(x_test)) # <-----
print('score', regr.score(x_test, y_test))


# print('The \'score\' is the coefficient of determination of the prediction. A.k.a. de \'determinatiecoëfficiënt\'.')
# print('De determinatiecoëfficiënt is een heel ingewikkeld iets op wikipedia.')

# X = np.array(df)
# print('X =', X)

# neural_net = MLPRegressor().fit(X[:, :-1], X[:,-1])
# res = neural_net.predict([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
# print('result =', res)

# sp.World (
#     lr.LidarPilotRealIo,
#     ls.LidarPilotSimulatedIo,
#     ps.Physics,
#     c.Control,
#     vs.Visualisation
# )
