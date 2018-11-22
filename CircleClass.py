#respawn and draw circles; check collisions

import pygame
pygame.font.init()
import random
import math

yellow = (240, 236, 87)
red = (234, 152, 143)
green = (103, 229, 191)
black = (0, 5, 45)
white = (243, 247, 241)

smallFont = pygame.font.SysFont("comicsansms", 65)

class Circle():
    def __init__(self, position):
        #overflow error when body is too close, use try/except to catch
        try:
            self.pos = (int(position[0]), int(position[1]))
        except:
            self.pos = (-50, -50)
        self.r = 50
        
    def draw(self, frameSurface):
        pygame.draw.circle(frameSurface, self.color, self.pos, self.r)

    def isHit(self, other):
        #circles hit if center of other is within self
        targetX, targetY = self.pos
        targetR = self.r
        bodyX, bodyY = other.pos
        return targetX - targetR < bodyX < targetX + targetR and \
               targetY - targetR < bodyY < targetY + targetR
        
class targetCircle(Circle):
    def __init__(self, position):
        super().__init__(position)
        self.color = red
        self.hit = False

class bodyCircle(Circle):
    def __init__(self, position):
        super().__init__(position)
        self.color = yellow
        self.r = 30
        
def generateBodyCircles(self):
    #generate circles at 5 joint positions
    head = bodyCircle(self.headPos)
    leftHand = bodyCircle(self.leftHandPos)
    rightHand = bodyCircle(self.rightHandPos)
    leftFoot = bodyCircle(self.leftFootPos)
    rightFoot = bodyCircle(self.rightFootPos)
    
    self.bodyCircles = [rightHand, leftHand, head, rightFoot, leftFoot]

def generateTargets(self, numOfTargets = None):
    #optional parameter ensures more complex shapes will be generated
    if numOfTargets == None:
        numOfTargets = random.choice((2, 3, 4))
    newTargets = []
    for i in range(numOfTargets):
        targetX = random.randint(500, 1500)
        targetY = random.randint(200, 900)
        newTargets.append(targetCircle((targetX, targetY)))
    if redoTargets(newTargets):
        newTargets = generateTargets(self, numOfTargets)
    self.targetCircles = newTargets
    return self.targetCircles

def redoTargets(newTargets):
    circlesSeen = []
    minDist, maxDist = 250, 850
    for target in newTargets:
        targetX, targetY = target.pos
        for prev in circlesSeen:
            prevX, prevY = prev
            if checkDistance(targetX, targetY, prevX, prevY) < minDist or\
               checkDistance(targetX, targetY, prevX, prevY) > maxDist:
                   print("redo " + str(len(newTargets)))
                   return True
        circlesSeen.append(target.pos)
    return False

def checkDistance(x1, y1, x2, y2):
    distance = math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
    return distance
    
def updateTargets(self):
    for targetCircle in self.targetCircles:
        targetCircle.hit = False
    
def checkCollisions(self):
    for targetCircle in self.targetCircles:
        for bodyCircle in self.bodyCircles:
            if targetCircle.isHit(bodyCircle):
                bodyCircle.color = green
                targetCircle.hit = True

def isShapeComplete(self):
    for targetCircle in self.targetCircles:
        if targetCircle.hit == False:
            return False
    return True
    
def drawAll(self):
    for circle in self.targetCircles:
        circle.draw(self.frameSurface)
    for circle in self.bodyCircles:
        circle.draw(self.frameSurface)
    #draw score
    score = smallFont.render("SCORE: " + str(self.score), True, white, black)
    scoreRect = score.get_rect(topleft = (1500, 50))
    self.frameSurface.blit(score, scoreRect)
    #draw timeLeft
    timeLeft = smallFont.render("Time remaining: %0.2f" %self.timeLeft, True, white, black)
    timeRect = timeLeft.get_rect(topleft = (100, 50))
    self.frameSurface.blit(timeLeft, timeRect)
