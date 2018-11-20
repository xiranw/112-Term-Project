#respawn and draw circles; check collisions

blue = (65,105,225)
red = (255, 0, 0)
green = (0, 255, 0)
import pygame
import random

class Circle():
    def __init__(self, position):
        #Overflow error when body is too close, use try/except to catch
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
        self.color = blue
        self.hit = False
        
class bodyCircle(Circle):
    def __init__(self, position):
        super().__init__(position)
        self.color = red
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
        numOfTargets = random.choice((3, 4))
    newTargets = []
    for i in range(numOfTargets):
        targetX = random.randint(300, 1800)
        targetY = random.randint(200, 1000)
        newTargets.append(targetCircle((targetX, targetY)))
    if redoTargets(newTargets):
        newTargets = generateTargets(self, numOfTargets)
    self.targetCircles = newTargets
    return self.targetCircles

def redoTargets(newTargets):
    #redo targets if they are too close or too far from each other
    circleX = []
    circleY = []
    minXDist, minYDist = 80, 200
    maxXDist, maxYDist = 800, 800
    for target in newTargets:
        targetX, targetY = target.pos[0], target.pos[1]
        for element in circleX:
            if abs(targetX - element) < minXDist or \
               abs(targetX - element) > maxXDist:
                print("redo " + str(len(newTargets)))
                return True
        circleX.append(targetX)
        for element in circleY:
            if abs(targetY - element) < minYDist or \
               abs(targetY - element) > maxYDist:
                print("redo " + str(len(newTargets)))
                return True
        circleY.append(targetY)
    return False

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
    Font = pygame.font.SysFont("Arial", 50)
    score = Font.render("Score: " + str(self.score), 0, (0, 0, 0))
    self.frameSurface.blit(score, (1700, 50))
    #draw timeLeft
    timeLeft = Font.render("Time remaining: %0.2f" %self.timeLeft, 0, (0, 0, 0))
    self.frameSurface.blit(timeLeft, (100, 50))
