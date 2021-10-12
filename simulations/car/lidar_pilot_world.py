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

sp.World (
    lr.LidarPilotRealIo,
    ls.LidarPilotSimulatedIo,
    ps.Physics,
    c.Control,
    vs.Visualisation
)
