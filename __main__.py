# main run function

# 11/20: added score, timer, constraints on generation of targets, fixed overflow error

from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import pygame
import ctypes
import CircleClass
import Modes

class Main():
    def __init__(self):
        #game run logic
        pygame.init()
        self.gameOver = False
        self.exit = False
        self.restart = False
        self.clock = pygame.time.Clock()
        self.timeLeft = 60
        
        self.bodies = None
        self.targetCircles = []
        
        #joint positions
        self.headPos = (-50, -50)
        self.leftHandPos, self.rightHandPos = (-50, -50), (-50, -50)
        self.leftElbowPos, self.rightElbowPos = (-50, -50), (-50,-50)
        self.leftFootPos, self.rightFootPos = (-50, -50), (-50, -50)
        
        #screen calibration
        self.screenWidth = 960
        self.screenHeight = 540
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        self.frameSurface = pygame.Surface((self.kinect.color_frame_desc.Width, self.kinect.color_frame_desc.Height), 0, 32)
        
        self.score = -1 #increments 1 when game starts
        self.canSkip = True
        self.skipsLeft = 3
    
    # CITATION - Kinect draw, getJoints framwork, and coordinate conversion:
    # https://github.com/Kinect/PyKinect2/blob/master/examples/PyKinectBodyGame.pymbcs

    def drawColorFrame(self, frame, targetSurface):
        targetSurface.lock()
        address = self.kinect.surface_as_array(targetSurface.get_buffer())
        #replacing old frame with new one
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        targetSurface.unlock()
    
    def drawKinectFrame(self):
        if self.kinect.has_new_color_frame():
            frame = self.kinect.get_last_color_frame()
            self.drawColorFrame(frame, self.frameSurface)
            frame = None
    
    def adjustKinectFrame(self):
        hToW = float(self.frameSurface.get_height()) / self.frameSurface.get_width()
        targetHeight = int(hToW * self.screen.get_width())
        surfaceToDraw = pygame.transform.scale(self.frameSurface, (self.screen.get_width(), targetHeight));
        self.screen.blit(surfaceToDraw, (0,0))
        surrgefaceToDraw = None
    
    def getJointPos(self):
        if self.kinect.has_new_body_frame(): 
            self.bodies = self.kinect.get_last_body_frame()
    
            if self.bodies is not None: 
            #if there are tracked people on screen
                for i in range(0, self.kinect.max_body_count):
                    body = self.bodies.bodies[i]
                    if not body.is_tracked: 
                        continue   
                    
                    joints = body.joints
                    #important! Converts joint coordinates to canvas coordinates
                    jointPoints = self.kinect.body_joints_to_color_space(joints)
                    
                    Head = PyKinectV2.JointType_Head
                    HandLeft = PyKinectV2.JointType_HandLeft
                    HandRight = PyKinectV2.JointType_HandRight
                    ElbowLeft = PyKinectV2.JointType_ElbowLeft
                    ElbowRight = PyKinectV2.JointType_ElbowRight
                    FootLeft = PyKinectV2.JointType_FootLeft
                    FootRight = PyKinectV2.JointType_FootRight
                    
                    #change joint positions if they are tracked
                    if joints[Head].TrackingState != PyKinectV2.TrackingState_NotTracked:
                        self.headPos = (jointPoints[Head].x, jointPoints[Head].y)
                    if joints[HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                        self.leftHandPos = (jointPoints[HandLeft].x, jointPoints[HandLeft].y)
                    if joints[HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                        self.rightHandPos = (jointPoints[HandRight].x, jointPoints[HandRight].y)
                    if joints[ElbowLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                        self.leftElbowPos = (jointPoints[ElbowLeft].x, jointPoints[ElbowLeft].y)
                    if joints[ElbowRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                        self.rightElbowPos = (jointPoints[ElbowRight].x, jointPoints[ElbowRight].y)
                    if joints[FootLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                        self.leftFootPos = (jointPoints[FootLeft].x, jointPoints[FootLeft].y)
                    if joints[FootRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                        self.rightFootPos = (jointPoints[FootRight].x, jointPoints[FootRight].y)
                        
    def startScreen(self):
        return Modes.runStartScreen(self)
    
    def endScreen(self):
        return Modes.runEndScreen(self)
    
    def isJump(self):
        leftFootY, rightFootY = self.leftFootPos[1], self.rightFootPos[1]
        return leftFootY < 750 and rightFootY < 750

    def run(self):
        while not self.gameOver:
            self.timeLeft -= self.clock.tick()/1000 #displays time in seconds
            if self.timeLeft <= 0:
                self.gameOver = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameOver = True
                    self.exit = True
            
            self.drawKinectFrame()

            #we have a body frame, so can get skeletons
            self.getJointPos()
            
            if self.targetCircles == [] or CircleClass.isShapeComplete(self):
                #make new targets at start of game and when a shape is done
                CircleClass.generateTargets(self)
                self.score += 1
            elif self.canSkip and self.isJump():
                CircleClass.generateTargets(self)
                self.skipsLeft -= 1
                self.canSkip = False
            elif not self.isJump():
                self.canSkip = True
            CircleClass.updateTargets(self)
            CircleClass.generateBodyCircles(self)
            CircleClass.checkCollisions(self)
            CircleClass.drawAll(self)
            
            self.adjustKinectFrame()
            pygame.display.update()
        
        while self.gameOver == True and self.exit == False:
            self.endScreen()
            if self.restart == True:
                self.__init__()
                self.run()

game = Main()
game.startScreen()
while not game.exit:
    game.run()
#close the window and quit
game.kinect.close()
pygame.quit()
