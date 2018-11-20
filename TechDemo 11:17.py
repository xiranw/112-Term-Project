#https://github.com/Kinect/PyKinect2/blob/master/examples/PyKinectBodyGame.pymbcs
from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import pygame
import ctypes
import CircleClass

class TechDemo():
    def __init__(self):
        pygame.init()
        self.gameOver = False
        self.done = False
        
        self.screenWidth = 1000
        self.screenHeight = 1000
        self.bodies = None
        
        self.rightHandPos = (-50, -50)
        self.leftHandPos = (-50, -50)
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 1000))
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        self.frameSurface = pygame.Surface((self.kinect.color_frame_desc.Width, self.kinect.color_frame_desc.Height), 0, 32)
    
    def drawColorFrame(self, frame, targetSurface):
        targetSurface.lock()
        address = self.kinect.surface_as_array(targetSurface.get_buffer())
        # replacing old frame with new one
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        targetSurface.unlock()
    
    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            
            if self.kinect.has_new_color_frame():
                frame = self.kinect.get_last_color_frame()
                self.drawColorFrame(frame, self.frameSurface)
                frame = None

            # We have a body frame, so can get skeletons
            if self.kinect.has_new_body_frame(): 
                self.bodies = self.kinect.get_last_body_frame()

                if self.bodies is not None: 
                    for i in range(0, self.kinect.max_body_count):
                        body = self.bodies.bodies[i]
                        if not body.is_tracked: 
                            continue         
                        
                        joints = body.joints
                        #important! Converts joint coordinates to canvas coordinates
                        jointPoints = self.kinect.body_joints_to_color_space(joints)
                        # save the hand positions
                        
                        HandRight = PyKinectV2.JointType_HandRight
                        HandLeft = PyKinectV2.JointType_HandLeft
                        Head = PyKinectV2.JointType_Head
                        if joints[HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.rightHandPos = (jointPoints[HandRight].x, jointPoints[HandRight].y)
                        if joints[HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.leftHandPos = (jointPoints[HandLeft].x, jointPoints[HandLeft].y)
                        if joints[Head].TrackingState != PyKinectV2.TrackingState.NotTracked:
                            self.headPos = (jointPoints[Head].x, jointPoints[Head].y)
            
            if self.targetCircles == [] or CircleClass.isShapeComplete(self):
                CircleClass.generateTargets(self)
                self.score += 1
            CircleClass.generateBodyCircles(self)
            CircleClass.checkCollisions(self)
            CircleClass.drawAll(self)
            
            hToW = float(self.frameSurface.get_height()) / self.frameSurface.get_width()
            targetHeight = int(hToW * self.screen.get_width())
            surfaceToDraw = pygame.transform.scale(self.frameSurface, (self.screen.get_width(), targetHeight));
            self.screen.blit(surfaceToDraw, (0,0))
            surfaceToDraw = None
            pygame.display.update()

            # --- Limit to 60 frames per second
            self.clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self.kinect.close()
        pygame.quit()

game = TechDemo()
game.run()
#
