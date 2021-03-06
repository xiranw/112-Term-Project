#three major classes for this game: Circle, Bomb, and Polygon

import pygame
pygame.font.init()
import random
import time
import math
import Globals

red = (234, 152, 143)
outlineRed= (255, 0, 0)
yellow = (240, 236, 87)
green = (103, 229, 191)
purple = (199, 130, 255)
black = (0, 5, 45)
white = (243, 247, 241)

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
        if self.color == red:
            pygame.draw.circle(frameSurface, outlineRed, self.pos, self.r + 5, 5)

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

class movingTarget(targetCircle):
    def __init__(self, position, direction):
        super().__init__(position)
        self.color = red
        self.direction = direction
        self.speed = 1
        self.moving = False
    
    def move(self):
        if self.moving == True:
            newX = self.pos[0] + (self.speed)*(self.direction[0])
            newY = self.pos[1] + (self.speed)*(self.direction[1])
            self.pos = (newX, newY)
    
    def draw(self, frameSurface):
        pygame.draw.circle(frameSurface, red, self.pos, self.r)
        pygame.draw.circle(frameSurface, outlineRed, self.pos, self.r + 5, 5)
        margin = 35
        centerX, centerY = self.pos
        if self.direction == (-1, 0):
            pointList = [(centerX-margin, centerY),
                         (centerX, centerY+margin), (centerX, centerY-margin)]
        elif self.direction == (1, 0):
            pointList = [(centerX+margin, centerY),
                         (centerX, centerY+margin), (centerX, centerY-margin)]
        elif self.direction == (0, -1):
            pointList = [(centerX-margin, centerY), (centerX+margin, centerY),
                         (centerX, centerY-margin)]
        elif self.direction == (0, 1):
            pointList = [(centerX-margin, centerY), (centerX+margin, centerY),
                         (centerX, centerY+margin)]
        pygame.draw.polygon(frameSurface, white, pointList)
            
class bodyCircle(Circle):
    def __init__(self, position, color):
        super().__init__(position)
        self.color = color
        self.r = 30


class Bomb():
    def __init__(self, speed=0.7):
        self.pos = (100, 0)
        self.speed = speed
        self.blow = False
        
        bombImage = pygame.image.load("bomb.png").convert_alpha()
        self.bombImage = pygame.transform.scale(bombImage, (200, 260))
        blowImage = pygame.image.load("blow.png").convert_alpha()
        self.blowImage = pygame.transform.scale(blowImage, (300, 200))
        
    def fall(self):
        if self.blow == False:
            self.pos = (self.pos[0], self.pos[1]+self.speed)
            if self.pos[1] > 700:
                self.blow = True
            
    def draw(self, frameSurface):
        if self.blow == False:
            frameSurface.blit(self.bombImage, self.pos)
        else:
            frameSurface.blit(self.blowImage, self.pos)

def checkBomb(self, speed=0.7):
    if self.makeBomb == True:
        self.newBomb = Bomb(speed)
        self.makeBomb = False
    try:
        self.newBomb.fall()
        self.newBomb.draw(self.frameSurface)
    except:
        pass


class Polygon():
    def __init__(self, circleList):
        self.pointList = []
        for circle in circleList:
            self.pointList.append(circle.pos)
    
    def draw(self, frameSurface):
        if len(self.pointList) == 2:
            pygame.draw.line(frameSurface, outlineRed, self.pointList[0], self.pointList[1], 10)
        elif len(self.pointList) > 2:
            pygame.draw.polygon(frameSurface, outlineRed, self.pointList, 10)

### For Start Screen ###

def getHandCircle(self):
    leftHands = []
    player = 0
    for body in self.bodyDict:
        allJoints = self.bodyDict[body][0]
        if allJoints == []:
            continue
        
        player += 1
        if player % 2 == 1:
            color = yellow
        else:
            color = purple
        
        leftHandPos = allJoints[1]
        leftHand = bodyCircle(leftHandPos, color)
        leftHands.append(leftHand)
    
    self.editorHand = leftHands

def drawStartShapes(self):
    for circle in self.editorHand:
        circle.draw(self.frameSurface)
    
### For Play Mode ###

def generateBodyCircles(self):
    #generate circles at 5 joint positions
    bodies = []
    player = 0
    for body in self.bodyDict:
        allJoints = self.bodyDict[body][0]
        if allJoints == []:
            continue
        
        player += 1
        if player % 2 == 1:
            color = yellow
        else:
            color = purple
        
        headPos, leftHandPos, rightHandPos, leftElbowPos, rightElbowPos, \
        leftFootPos, rightFootPos = allJoints
        head = bodyCircle(headPos, color)
        leftHand = bodyCircle(leftHandPos, color)
        rightHand = bodyCircle(rightHandPos, color)
        leftFoot = bodyCircle(leftFootPos, color)
        rightFoot = bodyCircle(rightFootPos, color)
        
        bodies.extend((head, leftHand, rightHand, leftFoot, rightFoot))
        
    self.bodyCircles = bodies

#optional parameter ensures more complex shapes will be generated
def generateTargets(self, numOfTargets = None):
    self.level = "static"
    numPlayers = self.checkBodyCount()
    if len(Globals.levelsToPlay) != 0:
        return playUserLevel(self)
    if numOfTargets == None:
        if numPlayers < 2:
            numOfTargets = random.choice((2, 3, 4))
        elif numPlayers == 2:
            numOfTargets = random.choice((4, 5))
    
    newTargets = []
    maxMoving = numOfTargets//2
    numMoving = 0
    for i in range(numOfTargets):
        targetX = random.randint(500, 1500)
        targetY = random.randint(200, 900)
        if self.score <= 100:
            newTargets.append(targetCircle((targetX, targetY)))
        else:
            if numMoving >= maxMoving:
                newTargets.append(targetCircle((targetX, targetY)))
                continue
            type = random.choice((targetCircle, movingTarget))
            if type == targetCircle:
                newTargets.append(targetCircle((targetX, targetY)))
            elif type == movingTarget:
                direction = random.choice(((-1,0), (1,0), (0,-1), (0,1)))
                newTargets.append(movingTarget((targetX, targetY), direction))
                numMoving += 1
                self.level = "moving"
    
    if redoTargets(newTargets):
        newTargets = generateTargets(self, numOfTargets)
    self.targetCircles = newTargets
    return self.targetCircles

def redoTargets(newTargets):
    #for creating feasible targets
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
    
def drawPlayShapes(self):
    shape = Polygon(self.targetCircles)
    shape.draw(self.frameSurface)
    for circle in self.targetCircles:
        circle.draw(self.frameSurface)
    for circle in self.bodyCircles:
        circle.draw(self.frameSurface)
    
### For Level Editor ###

def addTarget(self, leftHandPos):
    newTarget = targetCircle(leftHandPos)
    self.userLevel.append(newTarget)

def deleteTarget(self, leftHandPos):
    newTargets = []
    targetRemoved = False
    for circle in reversed(self.userLevel):
        leftHand = targetCircle(leftHandPos)
        if circle.isHit(leftHand) and targetRemoved == False:
            targetRemoved = True
        else:
            newTargets.append(circle)
    newTargets.reverse()
    self.userLevel = newTargets

def drawEditorShapes(self):
    if len(self.userLevel) > 2:
        shape = Polygon(self.userLevel)
        shape.draw(self.frameSurface)
    for circle in self.userLevel:
        circle.draw(self.frameSurface)
    for circle in self.editorHand:
        circle.draw(self.frameSurface)

def playUserLevel(self):
    #level: [[circlesPos], is there bomb, bomb speed]
    currLevel = Globals.levelsToPlay.pop(0)
    self.targetCircles = currLevel[0]
    self.choiceMade = True
    if currLevel[1] == True:
        speed = currLevel[2]
        self.newBomb = Bomb(speed)
    return self.targetCircles
