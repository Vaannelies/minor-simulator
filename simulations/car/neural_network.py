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
import glob as gl
import re
import sys as ss

ss.path.append (os.path.abspath ('../../..')) # If you want to store your simulations somewhere else, put SimPyLC in your PYTHONPATH environment variable

import pandas as pd
import joblib
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle

# list_of_files = gl.glob(r'.\data\*.xlsx') # * means all if need specific format then *.csv
# latest_file = max(list_of_files, key=os.path.getmtime)
# df = pd.read_excel(latest_file)


with open('.\data\samples.dat') as sampleFile:
    data = np.array([[float (word) for word in line.split()] for line in sampleFile.readlines()])


# Shuffle the dataset
# https://scikit-learn.org/stable/modules/generated/sklearn.utils.shuffle.html
# data = shuffle(df.to_numpy())
print('data', data)

# Remove duplicates from data
# print('Original excel data length:', len(data))
# filteredData =np.unique(data,axis=0)
# print ('Filtered excel data length (without duplicates): ', len(filteredData))
# data = filteredData

yColumn = [0 for item in data]      # output node values
for index, row in enumerate(data): 
    yColumn[index] += row[len(row)-1]

xColumns = []           # input nodes values
for index, row in enumerate(data):
    xColumns.append([])
    items = []
    for index, column in enumerate(row):
        if index < len(row)-1:
            if column > 10000000:
                column = 20
            items.append(column)
    xColumns[len(xColumns)-1] = items

x = xColumns
y = yColumn 
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = 1)

# Use MinMaxScaler on x_train and x_test
# scaler = MinMaxScaler()
# scaler.fit(x_train,y_train)
# x_train = scaler.transform(x_train)
# x_test = scaler.transform(x_test)

regr = MLPRegressor(
    hidden_layer_sizes=(64,64,64),
    activation="logistic",
    random_state = 1, 
    max_iter = 2048, ).fit(x_train, y_train)
# regr.add(layers.Dense(10, activation='relu'))

right_answers = 0
test_answers = regr.predict(x_test)
for i in range(len(x_test)):
    print('input nodes', x_test[i], 'predicted answer (output node)', '{:f}'.format(test_answers[i]), 'real answer', y_test[i])
    if(y_test[i] - test_answers[i]) < 1 and (y_test[i] - test_answers[i]) > -2:
        print('Right!')
        print('Difference:', y_test[i] - test_answers[i])
    print('\n')

    if(y_test[i] - test_answers[i]) < 1 and (y_test[i] - test_answers[i]) > -2:
        right_answers += 1

print()                     # wat betekent dit 
            #                           v
# print('predict', regr.predict(x_test[:2])) # <-----
print('Score', regr.score(x_test, y_test))
print('Total test data:', len(x_test), '\t',  'Right answers (difference less than 2):', right_answers)

# print('The \'score\' is the coefficient of determination of the prediction. A.k.a. de \'determinatiecoëfficiënt\'.')
# print('De determinatiecoëfficiënt is een heel ingewikkeld iets op wikipedia.')

# X = np.array(df)
# print('X =', X)

# neural_net = MLPRegressor().fit(X[:, :-1], X[:,-1])
# res = neural_net.predict([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
# print('result =', res)

# Deze line uitcommenten als je de getrained model wilt opslaan in een aparte file
# joblib.dump(regr, './data/trained_network.sav') 
