# main run function

# things to do: research multi, generate black circles, change editor inheritance

from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import pygame
import time
import ctypes
import Shapes
import Modes
import Globals

class Main():
    def __init__(self):
        #game run logic
        pygame.init()
        self.gameOver = False #game ends
        self.exit = False #users clicks exit button
        self.play = False
        self.restart = False
        self.editor = False
        
        self.clock = pygame.time.Clock()
        self.timeLeft = 60
        
        self.bodies = None
        self.targetCircles = []
        
        #joint positions
        self.bodyDict = { "body0":[[],[]], "body1":[[],[]], "body2":[[], []],
                          "body3":[[],[]], "body4":[[],[]], "body5":[[], []]}
        #2 lists per body: joints and hand states
        self.headPos = (-50, -50)
        self.leftHandPos, self.rightHandPos = (-50, -50), (-50, -50)
        self.leftElbowPos, self.rightElbowPos = (-50, -50), (-50,-50)
        self.leftFootPos, self.rightFootPos = (-50, -50), (-50, -50)
        self.leftHandState = -1
        
        #screen calibration
        self.screenWidth = 960
        self.screenHeight = 540
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        self.frameSurface = pygame.Surface((self.kinect.color_frame_desc.Width, self.kinect.color_frame_desc.Height), 0, 32)
        
        self.score = 0
        
        #skip logic
        self.skipsLeft = 3
        self.canSkip = True
        self.showHint = False
        self.hintShown = False
        
        #editor logic
        self.canEdit = True
        self.userLevel = []
        
        #bomb!
        self.newBomb = None
        self.makeBomb = False
        self.choiceMade = False
        self.userBomb = False
        
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
                        self.bodyDict["body"+str(i)] = [[],[]]
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
                    
                    if joints[HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                        self.leftHandState = body.hand_left_state
                    allJoints = [self.headPos, self.leftHandPos, self.rightHandPos,
                                 self.leftElbowPos, self.rightElbowPos, self.leftFootPos, self.rightFootPos]
                    self.bodyDict["body"+str(i)][0] = allJoints
                    self.bodyDict["body"+str(i)][1] = [self.leftHandState]
    
    def startScreen(self):
        return Modes.runStartScreen(self)
    
    def editorScreen(self):
        return Modes.runEditorScreen(self)
    
    def playScreen(self):
        return Modes.runPlayScreen(self)
    
    def endScreen(self):
        return Modes.runEndScreen(self)
    
    def run(self):
        while not self.exit:
            self.startScreen()
            if self.editor == True:
                self.editorScreen()
                self.__init__()
                self.run()
            elif self.play == True:
                self.playScreen()
                self.endScreen()
                while self.gameOver == True and self.exit == False:
                    self.endScreen()
                    if self.restart == True:
                        self.__init__()
                        self.run()

game = Main()
Globals.__init__()
game.run()
#close the window and quit
game.kinect.close()
pygame.quit()
