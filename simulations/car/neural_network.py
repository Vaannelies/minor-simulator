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


with open('.\data\samples_2.dat') as sampleFile:
    data = np.array([[float (word) for word in line.split(',')] for line in sampleFile.readlines()])


# Shuffle the dataset
# https://scikit-learn.org/stable/modules/generated/sklearn.utils.shuffle.html
# data = shuffle(data)
# data = shuffle(df.to_numpy())
print('data', data)

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

x_train = np.array(x_train)
y_train = np.array(y_train).reshape(-1,1)
x_test = np.array(x_test)
y_test = np.array(y_test).reshape(-1,1)
print('x_train', x_train.shape)
print('y_train', y_train.shape)


# Use MinMaxScaler on x_train and x_test
scalerX = MinMaxScaler(feature_range = (-1, 1), copy = True, clip = False)
scalerX.fit(x_train)
scaled_x_train = scalerX.transform(x_train)
scaled_x_test = scalerX.transform(x_test)

scalerY = MinMaxScaler(feature_range = (-1, 1), copy = True, clip = False)
scalerY.fit(y_train)
scaled_y_train = scalerY.transform(y_train)
scaled_y_test = scalerY.transform(y_test)

# predictedY = predict(test_x)
# predictedY = scalerY.inverse_transform(predictedY)
# Voordat je predict gaat gebruiken moet je die input data dus ook elke keer op dezelfde manier scalen. Anders krijgt ie bij predict()
# hele andere input mee dan hij gewend is bij het trainen (waarbij je het wel gescaled hebt).

regr = MLPRegressor(
    hidden_layer_sizes=(64,64,64),
    activation="logistic",
    random_state = 1, 
    max_iter = 2048, 
    ).fit(x_train, y_train.reshape(-1,))
    # ).fit(scaled_x_train, scaled_y_train.reshape(-1,)) // with scale

right_answers = 0
test_answers = regr.predict(x_test).reshape(-1,1)
# test_answers = regr.predict(scaled_x_test).reshape(-1,1) // with scale
print('test_answers', test_answers.shape)
# test_answers = scalerY.inverse_transform(test_answers) // with scale

for i in range(len(x_test)):
    print('input nodes', x_test[i], 'predicted answer (output node)', list(map('{:.2f}'.format,test_answers[i])), 'real answer', y_test[i])
    if(y_test[i] - test_answers[i]) < 1 and (y_test[i] - test_answers[i]) > -2:
        print('Right!')
        print('Difference:', y_test[i] - test_answers[i])
    print('\n')

    if(y_test[i] - test_answers[i]) < 1 and (y_test[i] - test_answers[i]) > -2:
        right_answers += 1

print()                         
print('Score', regr.score(x_test, y_test))
# print('Score', regr.score(scaled_x_test, scaled_y_test)) // with scale
print('Total test data:', len(x_test), '\t',  'Right answers (difference less than 2):', right_answers)

# Deze line uitcommenten als je de getrained model wilt opslaan in een aparte file
joblib.dump(regr, './data/trained_network_{}.sav'.format(round(regr.score(x_test, y_test),2))) 
