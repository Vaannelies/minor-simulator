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
# import xlsxwriter as xw
import struct as struct
import numpy as np
from threading import Thread
from random import randrange

class LidarPilotBase:


    def __init__ (self):
        self.driveEnabled = False
        self.steeringAngle = 0
        self.timer = tr.Timer ()
        if not os.path.isdir('./data'): os.mkdir('./data')
        self.samplefile = open('.\data\samples_2.dat', 'w')
        # self.workbook = xw.Workbook('./data/data{}.xlsx'.format(randrange(10)))
        # self.worksheet = self.workbook.add_worksheet()

        self.row = 0
        self.col = 0


        # pc = pid_controller.py . PidController is the classname.
        # An instance was created of class PidController.
        # p = 1.05
        # i = 0.05
        # d = 0.03
        # These values are needed to calculate the value in the method 'getY()'
        
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
        
    def getObstacleDistances(self, lidarDistanceSections):
        # If len(self.lidarDistances) == 120, lidarDistanceSections should be something like 6, 12, 24 etc.

        # create empty result array (filled with zeroes)
        result = [0 for i in range(lidarDistanceSections)]
        sectionSize = len(self.lidarDistances)/lidarDistanceSections

        for (index, lidarDistance) in enumerate(self.lidarDistances):
            if index%sectionSize  == 0:
                if lidarDistance > result[round((index - index%sectionSize) / sectionSize)]:
                    result[round((index - index%sectionSize) / sectionSize)] = lidarDistance
                    
        return result       

    def sweep (self):   # Control algorithm to be tested
        obstacleDistancesAmount = 24
        obstacleDistances = self.getObstacleDistances(obstacleDistancesAmount)

        if sp.driveManually == False:
            self.nearestObstacleDistance = self.finity
            self.nearestObstacleAngle = 0
            
            self.nextObstacleDistance = self.finity
            self.nextObstacleAngle = 0

            for lidarAngle in range (-self.lidarHalfApertureAngle, self.lidarHalfApertureAngle):
                lidarDistance = self.lidarDistances [lidarAngle]
                
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

            self.steeringAngle = self.steeringPidController.getY (self.timer.deltaTime, self.targetObstacleAngle, 0)
            self.targetVelocity = ((90 - abs (self.steeringAngle)) / 60) if self.driveEnabled else 0

            if self.samplefile.closed == False:
                for (index, obstacleDistance) in enumerate(obstacleDistances):
                    self.samplefile.write(f'{round(obstacleDistance, 4)},')

                self.samplefile.write(f'{round(self.steeringAngle, 4)}')
                self.samplefile.write('\n')


            # self.samplefile.write(self.row, obstacleDistancesAmount, self.steeringAngle)
            # self.samplefile.write()
            self.row += 1

            

    def output (self):  # Play nice in class hierarchy
        if sp.driveManually == False:
            pass
    