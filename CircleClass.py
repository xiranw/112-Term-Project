blue = (65,105,225)
red = (255, 0, 0)
green = (0, 255, 0)
import pygame

class Circle():
    def __init__(self, position):
        self.pos = (int(position[0]), int(position[1]))
        self.r = 50
        
    def draw(self, frameSurface):
        pygame.draw.circle(frameSurface, self.color, self.pos, self.r)
    
    def isHit(self, other):
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
    rightHand = bodyCircle(self.rightHandPos)
    leftHand = bodyCircle(self.leftHandPos)
    self.bodyCircles = [rightHand, leftHand]

def generateTargets(self):
    '''numOfTargets = random.choice((2, 3, 4))
    result = []
    for i in range(numOfTargets):
        pass'''
    target1 = targetCircle((700, 500))
    target2 = targetCircle((1500, 300))
    self.targetCircles = [target1, target2]

def checkCollisions(self):
    for targetCircle in self.targetCircles:
        for bodyCircle in self.bodyCircles:
            if targetCircle.isHit(bodyCircle):
                bodyCircle.color = green
                
def drawAll(self):
    for circle in self.targetCircles:
        circle.draw(self.frameSurface)
    for circle in self.bodyCircles:
        circle.draw(self.frameSurface)
