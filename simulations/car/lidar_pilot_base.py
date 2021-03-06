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
import time as tm
import traceback as tb
import math as mt
import simpylc as sp
import timer as tr
import pid_controller as pc
import xlsxwriter as xw
import joblib
import glob as gl
from threading import Thread
from random import randrange
from datetime import datetime
from time import sleep
import struct as struct
import numpy as np

class LidarPilotBase:

    def __init__ (self):
        self.driveEnabled = False
        self.steeringAngle = 0
        self.timer = tr.Timer ()
        if not os.path.isdir('.\data'): os.mkdir('.\data')
        self.samplefile = open('.\data\samples.dat', 'w')

        self.row = 0
        self.col = 0
        
        self.trained_network = joblib.load(self.getHighestNeuralNetwork())
        
        self.steeringPidController = pc.PidController (1.05, 0.05, 0.03)

        while True:
            self.timer.tick ()
            self.input ()
            self.sweep ()
            self.output ()
            tm.sleep (0.02)

    def input (self):   # Play nice in class hierarchy
        if sp.driveManually == False:
            pass  

    def getHighestNeuralNetwork(self):
        scores = []
        files = gl.glob(r'.\data\trained_network_0.*')

        for file in files:
            head, tail = os.path.split(file)
            scores.append(tail.split('_')[2].split('.sav')[0])

        highestScore = max(scores)
        highest_trained_network = r'.\data\trained_network_{}.sav'.format(highestScore)

        return highest_trained_network

    def sweep (self):   # Control algorithm to be tested
        obstacleDistances = self.sonarDistances
        trained_network_steeringAngle = self.trained_network.predict([obstacleDistances])

        if sp.driveManually == False:
            self.nearestObstacleDistance = self.finity
            self.nearestObstacleAngle = 0
            
            self.nextObstacleDistance = self.finity
            self.nextObstacleAngle = 0

            for lidarAngle in range (3):
                lidarDistance = self.sonarDistances [lidarAngle]
                
                if lidarDistance < self.nearestObstacleDistance:
                    self.nextObstacleDistance =  self.nearestObstacleDistance
                    self.nextObstacleAngle = self.nearestObstacleAngle
                    
                    self.nearestObstacleDistance = lidarDistance 
                    self.nearestObstacleAngle = lidarAngle

                elif lidarDistance < self.nextObstacleDistance:
                    self.nextObstacleDistance = lidarDistance
                    self.nextObstacleAngle = lidarAngle
            
            self.targetObstacleDistance = (self.nearestObstacleDistance + self.nextObstacleDistance) / 2
            self.targetObstacleAngle = (self.nearestObstacleAngle + self.nextObstacleAngle) / 2

            # self.steeringAngle = self.steeringPidController.getY (self.timer.deltaTime, self.targetObstacleAngle, 0)
            self.steeringAngle = trained_network_steeringAngle[0]
            self.targetVelocity = ((90 - abs (self.steeringAngle)) / 60) if self.driveEnabled else 0

            if self.samplefile.closed == False:
                for (index, obstacleDistance) in enumerate(obstacleDistances):
                    self.samplefile.write(f'{round(obstacleDistance, 4)},')

                self.samplefile.write(f'{round(self.steeringAngle, 4)}')
                self.samplefile.write('\n')

            self.row += 1

    def output (self):  # Play nice in class hierarchy
        if sp.driveManually == False:
            pass
    