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

class LidarPilotBase:
    def __init__ (self):
        self.driveEnabled = False
        self.steeringAngle = 0
        self.timer = tr.Timer ()
        if not os.path.isdir('.\data'): os.mkdir('.\data')
        self.samplefile = open('.\data\samples_0.04.dat', 'w')


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
            
            self.steeringAngle = self.steeringPidController.getY (self.timer.deltaTime, self.targetObstacleAngle, 0)
            self.targetVelocity = ((90 - abs (self.steeringAngle)) / 60) if self.driveEnabled else 0

    def output (self):  # Play nice in class hierarchy
        if sp.driveManually == False:
            pass
