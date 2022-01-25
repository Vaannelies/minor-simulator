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

'''

      z
      |
      o -- y
     /
    x

'''

import random as rd

import simpylc as sp

import parameters as pm
import math

normalFloorColor = (0, 0.003, 0)
collisionFloorColor = (1, 0, 0.3)
nrOfObstacles = 64

class Scanner:
    
    def __init__ (self, apertureAngle, middleApertureAngle, obstacles):
        self.apertureAngle = apertureAngle
        self.halfApertureAngle = self.apertureAngle // 2
        self.middleApertureAngle = middleApertureAngle
        self.halfMiddleApertureAngle = self.middleApertureAngle // 2
        self.obstacles = obstacles
        self.lidarDistances = [1_000_000_000 for angle in range (self.apertureAngle)]
        self.sonarDistances = [1_000_000_000 for angle in range (3)]

    def atan2 (object0, object1):
        return math.atan2 (evaluate (object0), evaluate (object1)) * degreesPerRadian
        
    def tNor (v):
        return sqrt (sum (entry * entry for entry in v))
    
    def tSub (v0, v1):
        return tuple (entry0 - entry1 for entry0, entry1 in zip (v0, v1))

    def scan (self, mountPosition, mountAngle):
        self.lidarDistances = [1_000_000_000 for angle in range (self.apertureAngle)]

        # Set every sonarDistance section to infinite
        self.sonarDistances[-1] = 1e+20
        self.sonarDistances[0] = 1e+20
        self.sonarDistances[1] = 1e+20


        for obstacle in self.obstacles:
            # For every roadCone, get the angle and distance relative to the car
            # and check whether it's in the left, middle or right sonar sector.
            # Assign the smallest distance to the sonarDistances[sectorIndex]

            relativePosition = self.tSub (obstacle.center, mountPosition) 
            distance = self.tNor (relativePosition)
            absoluteAngle = self.atan2 (relativePosition [1], relativePosition [0])
            relativeAngle = (round (absoluteAngle - mountAngle) + 180) % 360 - 180 
           
            if -self.halfApertureAngle <= relativeAngle < self.halfApertureAngle - 1:
                self.lidarDistances [relativeAngle] = round (min (distance, self.lidarDistances [relativeAngle]), 4)    # In case of coincidence, favor nearby obstacle
                if relativeAngle < -self.halfMiddleApertureAngle:
                    sectorIndex = -1
                elif relativeAngle < self.halfMiddleApertureAngle:
                    sectorIndex = 0
                else:
                    sectorIndex = 1
                self.sonarDistances [sectorIndex] = round (min (distance, self.sonarDistances [sectorIndex]), 4)

# class Line (sp.Cylinder):
#     def __init__ (self, **arguments):
#        super () .__init__ (size = (0.01, 0.01, 0), axis = (1, 0, 0), angle = 90, color = (0, 1, 1), **arguments)

# class BodyPart (sp.Beam):
#     def __init__ (self, **arguments):
#         super () .__init__ (color = (1, 0, 0), **arguments)

# class Wheel:
#     def __init__ (self, **arguments): 
#         self.suspension = sp.Cylinder (size = (0.01, 0.01, 0.001), axis = (1, 0, 0), angle = 90, pivot = (0, 0, 1), **arguments)
#         self.rim = sp.Beam (size = (0.08, 0.06, 0.02), pivot = (0, 1, 0), color = (0, 0, 0))
#         self.tire = sp.Cylinder (size = (pm.wheelDiameter, pm.wheelDiameter, 0.04), axis = (1, 0, 0), angle = 90, color = (1, 1, 0))
#         self.line = Line ()
        
#     def __call__ (self, wheelAngle, slipping, steeringAngle = 0):
#         return self.suspension (rotation = steeringAngle, parts = lambda:
#             self.rim (rotation = wheelAngle, parts = lambda:
#                 self.tire (color = (rd.random (), rd.random (), rd.random ()) if slipping else (1, 1, 0)) +
#                 self.line ()
#         )   )
        
# class Window (sp.Beam):
#     def __init__ (self, **arguments):
#         super () .__init__ (axis = (0, 1, 0), color = (0, 0, 1), **arguments)
        
# class Floor (sp.Beam):
#     side = 16
#     spacing = 0.2
#     halfSteps = round (0.5 * side / spacing)

#     class Stripe (sp.Beam):
#         def __init__ (self, **arguments):
#             super () .__init__ (size = (0.01, Floor.side, 0.001), **arguments)
            
#     def __init__ (self, **arguments):
#         super () .__init__ (size = (self.side, self.side, 0.0005), color = normalFloorColor)
#         self.xStripes = [self.Stripe (center = (0, nr * self.spacing, 0.0001), angle = 90, color = (1, 1, 1)) for nr in range (-self.halfSteps, self.halfSteps)]
#         self.yStripes = [self.Stripe (center = (nr * self.spacing, 0, 0), color = (0, 0, 0)) for nr in range (-self.halfSteps, self.halfSteps)]
        
#     def __call__ (self, parts):
#         return super () .__call__ (color = collisionFloorColor if self.scene.collided else  normalFloorColor, parts = lambda:
#             parts () +
#             sum (xStripe () for xStripe in self.xStripes) +
#             sum (yStripe () for yStripe in self.yStripes)
#         )



      
class Scene:
    _dmCheck, _dmUpdate, _dmRender, _dmAsync = range (4)

    def __init__ (self, name = None, width = 600, height = 400):
        self.name = name if name else self.__class__.__name__.lower ()
        self.width = width
        self.height = height
        # self.camera = Camera (tracking = False)
        # self._displayMode = Scene._dmCheck
        self._async = False
        self.collided = False
        
    # def _registerWithCamera (self):
        # self.camera.scene = self
        
    def _registerWithThings (self):                
        for thing in Thing.instances:
            thing.scene = self
         
        # if self._displayMode == Scene._dmCheck:
        #     self.display ()
        #     if self._async:
        #         self._displayMode = Scene._dmAsync
        #     else:
        #         self._displayMode = Scene._dmUpdate
        # else:
        #     abortInvalidDisplayMode (currentframe ())
        
    def _createWindow (self):
        glutInitWindowSize (self.width, self.height)
        self.window = glutCreateWindow (getTitle (self.name) .encode ('ascii'))
        
        glClearColor (0, 0, 0, 0)
        
        glEnable (GL_LINE_SMOOTH)
        glEnable(GL_BLEND);
        glEnable (GL_MULTISAMPLE)
        glEnable (GL_DEPTH_TEST)
        
        glShadeModel (GL_SMOOTH)
        glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth (1.5)
        
        glEnable (GL_LIGHTING)
        glColorMaterial (GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glEnable (GL_COLOR_MATERIAL)

        glLight (GL_LIGHT0, GL_POSITION, (5, 5, 0, 0))
        glLight (GL_LIGHT0, GL_DIFFUSE, (0.2, 0.2, 0.2))
        glEnable (GL_LIGHT0)
        
        glLight (GL_LIGHT1, GL_POSITION, (5, -5, 0, 0))
        glLight (GL_LIGHT1, GL_DIFFUSE, (0, 0, 0.6))
        glEnable (GL_LIGHT1)
        
        glLight (GL_LIGHT3, GL_POSITION, (0, 0, 5, 0))
        glLight (GL_LIGHT3, GL_DIFFUSE, (0.1, 0.1, 0.5))
        glEnable (GL_LIGHT3)
        
        glLight (GL_LIGHT4, GL_POSITION, (0, 0, -1, 0))
        glLight (GL_LIGHT4, GL_DIFFUSE, (0.05, 0, 0))
        glEnable (GL_LIGHT4)
        
        # glutDisplayFunc (self._display)
        glutReshapeFunc (self._reshape)
        
    # def _display (self):
    #     # [object coords] -> (model view matrix) -> [eye coords] (projection matrix) -> [clip coords]
        
    #     # Operations related to projection matrix: gluPerspective, gluLookat
    #     # They will work on the camera

    #     # Operations related to model view matrix: glTranslate, glRotate, glScale.
    #     # They will work on the objects
                    
    #     if self._displayMode in {Scene._dmRender, Scene._dmAsync}:        
    #         # self.camera._transform (False)   # Expensive so only if tracking, not forced
                    
    #         glLoadIdentity ()
    #         glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
            
    #         glPushMatrix ()
    #         self.display () # Since we'll render in GL_MODELVIEW mode, operations in self.display () will move the objects
    #         self._collide ()
    #         glPopMatrix ()

    #         glFlush ()
    #         glutSwapBuffers ()
            
    #         if self._displayMode == Scene._dmRender:
    #             self._displayMode = Scene._dmUpdate
            
    def _reshape (self, width, height):
        self.width = width
        self.height = height
        glViewport (0, 0, self.width, self.height)
        # self.camera ()
        # self.camera._transform (True)        
        
    # def update (self):
    #     # if self._displayMode == Scene._dmUpdate:
    #     #     self.display ()
    #     #     self._displayMode = Scene._dmRender
            
    def _collide (self):
        self.collided = False
        for colliderGroup in Thing.groups.values ():
            for thing in colliderGroup:
                thing.computeCollisionFields ()
            for collideeGroup in Thing.groups.values ():
                if colliderGroup == collideeGroup:
                    break
                for collider in colliderGroup:
                    for collidee in collideeGroup:
                        if collision (collider, collidee):
                            self.collided = True
                            return
                            
class Visualisation (sp.Scene):
    # class Visualisation (sp.Scene):
    def __init__ (self):
        super () .__init__ ()
        
        # self.camera = sp.Camera ()
        
        # self.floor = Floor (scene = self)
        
        # self.fuselage = BodyPart (size = (0.70, 0.16, 0.08), center = (0, 0, 0.07), pivot = (0, 0, 1), group = 0)
        # self.fuselageLine = Line ()
        # self.cabin = BodyPart (size = (0.20, 0.16, 0.06), center = (-0.06, 0, 0.07))
        
        # self.wheelFrontLeft = Wheel (center = (pm.wheelShift, 0.08, -0.02))
        # self.wheelFrontRight = Wheel (center = (pm.wheelShift, -0.08, -0.02))
        
        # self.wheelRearLeft = Wheel (center = (-pm.wheelShift, 0.08, -0.02))
        # self.wheelRearRight = Wheel (center = (-pm.wheelShift, -0.08, -0.02))
        
        # self.windowFront = Window (size = (0.05, 0.14, 0.14), center = (0.14, 0, -0.025), angle = -60)    
        # self.windowRear = Window (size = (0.05, 0.14, 0.18), center = (-0.18, 0, -0.025),angle = 72) 

        self.letter = 's'
        self.roadCones = []
        track = open ('sonar.track')
        
        for rowIndex, row in enumerate (track):
            for columnIndex, column in enumerate (row):
                # if column == '*':
                #     # self.roadCones.append (sp.Cone (
                #     #     size = (0.07, 0.07, 0.15),
                #     #     center = (columnIndex / 4 - 8, rowIndex / 2 - 8, 0.15),
                #     #     color = (1, 0.3, 0),
                #     #     group = 1
                #     # ))
                # elif column == "@":
                self.startX = columnIndex / 4 - 8
                self.startY = rowIndex / 2 - 8
                self.init = True
                
        # track.close ()
        
        self.lidar = Scanner (160, 45, self.roadCones)
        # print (self.lidar)
        
    def display (self):
        if self.init:
            self.init = False
            # sp.world.physics.positionX.set (self.startX) 
            # sp.world.physics.positionY.set (self.startY)
        
        # if self.letter == 'f':
        #     self.camera (   # First person
        #         position = sp.tEva ((sp.world.physics.positionX, sp.world.physics.positionY, 1)),
        #         focus = sp.tEva ((sp.world.physics.focusX, sp.world.physics.focusY, 0))
        #     )
        # elif self.letter == 's':
        #     self.camera (   # Soccer match
        #         position = sp.tEva ((sp.world.physics.positionX + 2, sp.world.physics.positionY, 2)),
        #         focus = sp.tEva ((sp.world.physics.positionX + 0.001, sp.world.physics.positionY, 0))
        #     )
        # elif self.letter == 'h':
        #     self.camera (   # Helicopter
        #         position = sp.tEva ((0.0000001, 0, 20)),
        #         focus = sp.tEva ((0, 0, 0))
        #     )
        
        # self.floor (parts = lambda:
        #     self.fuselage (position = (sp.world.physics.positionX, sp.world.physics.positionY, 0), rotation = sp.world.physics.attitudeAngle, parts = lambda:
        #         self.cabin (parts = lambda:
        #             self.windowFront () +
        #             self.windowRear ()
        #         ) +
                
        #         self.wheelFrontLeft (
        #             wheelAngle = sp.world.physics.midWheelAngle,
        #             slipping = sp.world.physics.slipping,
        #             steeringAngle = sp.world.physics.steeringAngle
        #         ) +
        #         self.wheelFrontRight (
        #             wheelAngle = sp.world.physics.midWheelAngle,
        #             slipping = sp.world.physics.slipping,
        #             steeringAngle = sp.world.physics.steeringAngle
        #         ) +
                
        #         self.wheelRearLeft (
        #             wheelAngle = sp.world.physics.midWheelAngle,
        #             slipping = sp.world.physics.slipping
        #         ) +
        #         self.wheelRearRight (
        #             wheelAngle = sp.world.physics.midWheelAngle,
        #             slipping = sp.world.physics.slipping
        #         ) +
                
        #         self.fuselageLine ()
        #     ) +
            
        #     sum (roadCone () for roadCone in self.roadCones)
        # )
                
        try:
            self.lidar.scan (self.fuselage.position, self.fuselage.rotation)
        except Exception as exception: # Initial check
            pass
            # print ('Visualisation.display:', exception)

    # def setLetter(self, letter):
    #     self.letter = letter
