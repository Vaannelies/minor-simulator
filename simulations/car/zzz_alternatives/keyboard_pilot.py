# ====== Legal notices
#
# Copyright (C) 2013 - 2020 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

import os
import time as tm
import xlsxwriter as xw
from random import randrange
from datetime import datetime
import simpylc as sp

class KeyboardPilot:
    def __init__ (self):
        print ('Use arrow keys to control speed and direction')
        self.steeringAngle = 0
        
        if not os.path.isdir('./data'): os.mkdir('./data')
        self.samplefile = open('.\data\samples_2.dat', 'w')

        self.row = 0
        self.col = 0

        while True:
            self.input ()
            self.sweep ()
            self.output ()
            tm.sleep (0.02)
            
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

    def input (self):
        if sp.driveManually == True:
            key = sp.getKey ()
            
            self.leftKey = key == 'KEY_LEFT'
            self.rightKey = key == 'KEY_RIGHT'
            self.upKey = key == 'KEY_UP'
            self.downKey = key == 'KEY_DOWN'

            if key == '\x1b': # Escape key
                if self.samplefile.closed == False:
                    self.samplefile.close()
                    print('Saved')
            elif key == 's':
	            sp.world.visualisation.setLetter(key)
            elif key == 'f':
                sp.world.visualisation.setLetter(key)
            elif key == 'h':
                sp.world.visualisation.setLetter(key)

        self.targetVelocityStep = sp.world.control.targetVelocityStep
        self.steeringAngleStep = sp.world.control.steeringAngleStep

    def sweep (self):
        self.lidarDistances = sp.world.visualisation.lidar.distances
        obstacleDistancesAmount = 24
        obstacleDistances = self.getObstacleDistances(obstacleDistancesAmount)

        if sp.driveManually == True:
            if self.leftKey:
                self.steeringAngleStep += 1
            elif self.rightKey:
                self.steeringAngleStep -= 1
            elif self.upKey:
                self.targetVelocityStep += 1
            elif self.downKey:
                self.targetVelocityStep -= 1
            
            if self.samplefile.closed == False:
                for (index, obstacleDistance) in enumerate(obstacleDistances):
                    self.samplefile.write(f'{round(obstacleDistance, 4)},')

                self.samplefile.write(f'{round(10 * self.steeringAngleStep, 4)}')
                self.samplefile.write('\n')

            self.row += 1
        
    def output (self):
        if sp.driveManually == True:
            sp.world.control.steeringAngleStep.set (self.steeringAngleStep)
            sp.world.control.targetVelocityStep.set (self.targetVelocityStep)
            
