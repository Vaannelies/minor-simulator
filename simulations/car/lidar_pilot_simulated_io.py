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

import simpylc as sp
import lidar_pilot_base as lb
from pynput.keyboard import Controller

class LidarPilotSimulatedIo (lb.LidarPilotBase):
    def __init__ (self):
        print ('Use up arrow to start, down arrow to stop')
        self.finity = sp.finity
        self.keyboard = Controller()
        super () .__init__ ()
        
    def input (self):   # Input from simulator
        super () .input ()
        key = sp.getKey ()
        if sp.driveManually == False:                
            if key == 'KEY_UP':
                self.driveEnabled = True
            elif key == 'KEY_DOWN':
                self.driveEnabled = False
            elif key == '\x1b':
                self.workbook.close()
            elif key == 'h': #press h for Helicopter view
                sp.world.visualisation.camera (position = sp.tEva ((0.0000001, 0, 20)),focus = sp.tEva ((0, 0, 0)))
            elif key == 'f': #press f for First person view 
                sp.world.visualisation.camera (position = sp.tEva ((sp.world.physics.positionX, sp.world.physics.positionY, 1)), 
                focus = sp.tEva ((sp.world.physics.focusX, sp.world.physics.focusY, 0)))
                self.keyboard.press(key)
            elif key == 's': #press s for Soccer match view
                sp.world.visualisation.camera (position = sp.tEva ((sp.world.physics.positionX + 2, sp.world.physics.positionY, 2)), 
                focus = sp.tEva ((sp.world.physics.positionX + 0.001, sp.world.physics.positionY, 0)))
                self.keyboard.press(key)
                
        self.lidarDistances = sp.world.visualisation.lidar.distances
        self.lidarHalfApertureAngle = sp.world.visualisation.lidar.halfApertureAngle
        
    def output (self):  # Output to simulator
        super () .output ()
        if sp.driveManually == False:
            sp.world.physics.steeringAngle.set (self.steeringAngle)
            sp.world.physics.targetVelocity.set (self.targetVelocity)
        
