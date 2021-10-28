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

import time as tm
import traceback as tb
import math as mt
import simpylc as sp
import timer as tr
import pid_controller as pc
import xlsxwriter as xw
from threading import Thread

class LidarPilotBase:


    def __init__ (self):
        self.driveEnabled = False
        self.steeringAngle = 0
        self.timer = tr.Timer ()
        self.workbook = xw.Workbook('data.xlsx')
        self.worksheet = self.workbook.add_worksheet()

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
        
    def sweep (self):   # Control algorithm to be tested
        if(self.row == 0):
            self.worksheet.write(self.row, self.col, 'nearestObstacleDistance')
            self.worksheet.write(self.row, self.col + 1,'nearestObstacleAngle')
            self.worksheet.write(self.row, self.col + 2, 'nextObstacleDistance')
            self.worksheet.write(self.row, self.col + 3, 'nextObstacleAngle')
            self.worksheet.write(self.row, self.col + 4, 'targetObstacleDistance')
            self.worksheet.write(self.row, self.col + 5, 'targetObstacleAngle')
            self.row += 1

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

                    self.worksheet.write(self.row, self.col, self.nearestObstacleDistance)
                    self.worksheet.write(self.row, self.col + 1, self.nearestObstacleAngle)
                    self.worksheet.write(self.row, self.col + 2, self.nextObstacleDistance)
                    self.worksheet.write(self.row, self.col + 3, self.nextObstacleAngle)

                    self.row += 1

                elif lidarDistance < self.nextObstacleDistance:
                    self.nextObstacleDistance = lidarDistance
                    self.nextObstacleAngle = lidarAngle

                    self.worksheet.write(self.row, self.col, self.nearestObstacleDistance)
                    self.worksheet.write(self.row, self.col + 1, self.nearestObstacleAngle)
                    self.worksheet.write(self.row, self.col + 2, self.nextObstacleDistance)
                    self.worksheet.write(self.row, self.col + 3, self.nextObstacleAngle)

                    self.row += 1
            
            self.targetObstacleDistance = (self.nearestObstacleDistance + self.nextObstacleDistance) / 2
            self.targetObstacleAngle = (self.nearestObstacleAngle + self.nextObstacleAngle) / 2

            self.worksheet.write(self.row, self.col + 4, self.targetObstacleDistance)
            self.worksheet.write(self.row, self.col + 5, self.targetObstacleAngle)
            
            self.steeringAngle = self.steeringPidController.getY (self.timer.deltaTime, self.targetObstacleAngle, 0)
            self.targetVelocity = ((90 - abs (self.steeringAngle)) / 60) if self.driveEnabled else 0

            

    def output (self):  # Play nice in class hierarchy
        if sp.driveManually == False:
            pass
    