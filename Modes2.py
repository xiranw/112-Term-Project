# starting, editing, playing, and ending screen logic

import pygame
pygame.font.init()

import Shapes
import UserLevels
import time
import random

black = (0, 5, 45)
white = (243, 247, 241)
yellow = (240, 236, 87)
green = (103, 229, 191)
red = (255, 0, 0)

titleFont = pygame.font.SysFont("comicsansms", 100)
medFont = pygame.font.SysFont("comicsansms", 70)
smallFont = pygame.font.SysFont("comicsansms", 65)

# CITATION - anchoring text:
# https://stackoverflow.com/questions/23982907/python-library-pygame-centering-text
def drawButton(self, message, font, start, textColor, backColor, dimen):
    text = font.render(message, True, textColor, backColor)
    if start == "topleft":
        textButton = text.get_rect(topleft = dimen)
    elif start == "center":
        textButton = text.get_rect(center = dimen)
    self.frameSurface.blit(text, textButton)
    return textButton.size

def buttonClicked(self, button):
    if button == "playButton":
        x1, y1 = self.screenWidth/4, 400
        deltaX, deltaY = self.playButtonSize
    elif button == "editorButton":
        x1, y1 = self.screenWidth/4, 700
        deltaX, deltaY = self.editorButtonSize
    elif button == "saveButton":
        x1, y1 = 330, 50
        deltaX, deltaY = self.saveButtonSize
    elif button == "backButton":
        x1, y1 = 1300, 50
        deltaX, deltaY = self.backButtonSize
    elif button == "yesBomb":
        x1, y1 = 1500, 350
        deltaX, deltaY = self.yesButtonSize
    elif button == "noBomb":
        x1, y1 = 1680, 350
        deltaX, deltaY = self.noButtonSize
    elif button == "slow":
        pass
    elif button == "med":
        pass
    elif button == "fast":
        pass
    leftHandX, leftHandY = self.leftHandPos
    return x1 < leftHandX < x1 + deltaX and y1 < leftHandY < y1 + deltaY

### Start Screen ###

def runStartScreen(self):
    onStartScreen = True
    while onStartScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                onStartScreen = False
                self.exit = True

        self.drawKinectFrame()
        drawStartText(self)
        
        self.getJointPos()
        if playClicked(self):
            onStartScreen = False
            self.play = True
        elif editorClicked(self):
            onStartScreen = False
            self.editor = True
        
        self.adjustKinectFrame()
        pygame.display.update()
        self.clock.tick(60)

def drawStartText(self):
    title = titleFont.render("Shape Matching Game", True, black)
    titleRect = title.get_rect(center=(self.screenWidth, 100))
    self.frameSurface.blit(title, titleRect)
    
    self.playButtonSize = drawButton(self, "PLAY", titleFont, "topleft",
                                     white, black, (self.screenWidth/4, 400))
    
    self.editorButtonSize = drawButton(self, "EDITOR", titleFont, "topleft",
                                     white, black, (self.screenWidth/4, 700))

### Navigation to play or Level Editor

def playClicked(self):
    return buttonClicked(self, "playButton")

def editorClicked(self):
    return buttonClicked(self, "editorButton")

### Play Game Screen ###

def runPlayScreen(self):
    t0 = time.time()
    while not self.gameOver:
        self.timeLeft -= self.clock.tick()/1000 #displays time in seconds
        t1 = time.time()
        levelTime = t1 - t0
        if self.timeLeft <= 0:
            self.gameOver = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameOver = True
                self.exit = True
        
        self.drawKinectFrame()
        drawPlayText(self)

        #we have a body frame, so can get skeletons
        self.getJointPos()
        
        #generates targets and increments score
        if self.targetCircles == []: #game begins
            resetVariables(self)
            Shapes.generateTargets(self)
        elif Shapes.isShapeComplete(self):
            if self.newBomb != None:
                self.score += 100
            else: 
                self.score += 10 * len(self.targetCircles)
            resetVariables(self)
            Shapes.generateTargets(self)
            t0 = t1 #reset level timer
        
        #skip logic
        elif self.canSkip and self.isJump() and self.skipsLeft > 0:
            resetVariables(self)
            Shapes.generateTargets(self)
            t0 = t1
            self.skipsLeft -= 1
            self.canSkip = False
            self.hintShown = True
            self.showHint = False
        elif not self.isJump():
            self.canSkip = True
        
        if levelTime > 10 and self.hintShown == False:
            self.showHint = True
        elif levelTime < 10:
            if self.showHint == True:
                self.showHint = False
                self.hintShown = True
        
        #bomb logic
        if not self.choiceMade:
            self.makeBomb = random.choice((True, False, False))
            self.choiceMade = True
        Shapes.checkBomb(self)
        if self.newBomb != None and self.newBomb.blow:
            self.score -= 50
            resetVariables(self)
            Shapes.generateTargets(self)
            t0 = t1
        
        Shapes.updateTargets(self)
        Shapes.generateBodyCircles(self)
        Shapes.checkCollisions(self)
        Shapes.drawPlayShapes(self)
        
        self.adjustKinectFrame()
        pygame.display.update()

def drawPlayText(self):
    #draw score
    score = smallFont.render("SCORE: " + str(self.score), True, white, black)
    scoreRect = score.get_rect(topleft = (100, 200))
    self.frameSurface.blit(score, scoreRect)
    
    #draw timeLeft
    timeLeft = smallFont.render("Time: %0.2f" %self.timeLeft, True, white, black)
    timeRect = timeLeft.get_rect(topleft = (100, 50))
    self.frameSurface.blit(timeLeft, timeRect)
    
    #draw stuck hint
    if self.showHint == True:
        #blinking hint!
        colorNum = self.timeLeft % 2
        if 0 < colorNum < 0.5 or 1 < colorNum < 1.5: 
            color = green
        else: 
            color = yellow
        hint = medFont.render("Stuck? JUMP to skip!", True, color, black)
        hintRect = hint.get_rect(center=(self.screenWidth, 90))
        self.frameSurface.blit(hint, hintRect)
    elif self.hintShown == True:
        skips = smallFont.render("Skips Left: " + str(self.skipsLeft), True, white, black)
        skipsRect = score.get_rect(topleft = (1400, 50))
        self.frameSurface.blit(skips, skipsRect)
        
    #bomb instruction
    if self.newBomb != None and self.newBomb.blow != True:
        caution = medFont.render("Complete level before bomb hits floor!", True, red, black)
        cautionRect = caution.get_rect(center=(self.screenWidth, 1000))
        self.frameSurface.blit(caution, cautionRect)
    
def resetVariables(self):
    self.newBomb = None
    self.makeBomb = False
    self.choiceMade = False

### Level Editor Screen ###

def runEditorScreen(self):
    onEditorScreen = True
    while onEditorScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                onEditorScreen = False
                self.exit = True
    
        self.drawKinectFrame()
        drawEditorText(self)
        
        self.getJointPos()
        
        # save and back buttons
        if saveClicked(self) and len(self.userLevel) != 0:
            if self.userBomb == False:
                level = [self.userLevel, self.userBomb, 0]
            else:
                level = [self.userLevel, self.userBomb, self.newBomb.speed]
            UserLevels.editedLevels.append(level)
            UserLevels.levelsToPlay.append(level)
            self.userBomb, self.makeBomb = False, False
            self.userLevel = []
        elif backClicked(self):
            self.userBomb, self.makeBomb = False, False
            onEditorScreen = False
        
        # bomb buttons
        if yesBombClicked(self) and self.userBomb == False:
            self.userBomb = True
            self.makeBomb = True
        elif noBombClicked(self) and self.userBomb == True:
            self.userBomb = False
            self.newBomb = None
        
        Shapes.checkBomb(self)
        
        if self.userBomb == True:
            if slowClicked(self) and self.newBomb.speed != 0.7:
                self.makeBomb = True
                self.newBomb.speed = 0.7
            elif medClicked(self) and self.newBomb.speed != 0.9:
                self.makeBomb = True
                self.newBomb.speed = 0.9
            elif fastClicked(self) and self.newBomb.speed != 1.2:
                self.makeBomb = True
                self.newBomb.speed = 1.2
        
        # adding and deleting targets
        if self.canEdit and self.leftHandState == 3: #closed fist
            Shapes.addTarget(self)
            self.canEdit = False
        else:
            if self.leftHandState != 3:
                self.canEdit = True
            if self.leftHandState == 4: # lasso
                Shapes.deleteTarget(self)
        Shapes.getHandCircle(self)
        Shapes.drawEditorShapes(self)
        
        self.adjustKinectFrame()
        pygame.display.update()
        self.clock.tick(60)

def drawEditorText(self):
    fist = medFont.render("Fist: draw", True, black)
    fistRect = fist.get_rect(topleft=(150, 300))
    self.frameSurface.blit(fist, fistRect)
    
    lasso = medFont.render("Lasso: delete", True, black)
    lassoRect = fist.get_rect(topleft=(150, 400))
    self.frameSurface.blit(lasso, lassoRect)
    
    self.saveButtonSize = drawButton(self, "SAVE", titleFont, "topleft",
                                     white, black, (330, 50))
    
    self.backButtonSize = drawButton(self, "BACK", titleFont, "topleft",
                                     white, black, (1300, 50))
    
    if self.userBomb == False:
        yesColor, noColor = black, green
    else:
        yesColor, noColor = green, black
        drawSpeedButtons(self)
    
    self.yesButtonSize = drawButton(self, "Yes!", medFont, "topleft", white, yesColor, (1500, 350))
    self.noButtonSize = drawButton(self, "No!", medFont, "topleft", white, noColor, (1680, 350))
    
def drawSpeedButtons(self):
    speed = self.newBomb.speed
    if speed == 0.7:
        slowColor = green
        medColor, fastColor = black, black
    elif speed == 0.9:
        medColor = green
        slowColor, fastColor = black, black
    elif speed == 1.2:
        fastColor = green
        slowColor, medColor = black, black
    slowButtonSize = drawButton("Slow", smallFont, "topleft", white, slowColor, (1500, 440))
    medButtonSize = drawButton("Med", smallFont, "topleft", white, medColor, (1500, 485))
    fastButtonSize = drawButton("Fast", smallFont, "topleft", white, fastColor, (1500, 530))
        
def saveClicked(self):
    return buttonClicked(self, "saveButton")

def backClicked(self):
    return buttonClicked(self, "backButton")

def yesBombClicked(self):
    return buttonClicked(self, "yesBomb")

def noBombClicked(self):
    return buttonClicked(self, "noBomb")

def slowClicked(self):
    return buttonClicked(self, "slow")

def medClicked(self):
    return buttonClicked(self, "med")

def fastClicked(self):
    return buttonClicked(self, "fast")
    
### End Screen ###

def runEndScreen(self):
    onEndScreen = True
    while onEndScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                onEndScreen = False
                self.exit = True
        
        self.drawKinectFrame()
        drawEndText(self)
        
        self.getJointPos()
        if matchY(self):
            self.restart = True
            onEndScreen = False
        elif dabbing(self):
            onEndScreen = False
            self.exit = True
            
        self.adjustKinectFrame()
        pygame.display.update()
        self.clock.tick(60)

def drawEndText(self):
    over = titleFont.render("Game Over! Your score is " + str(self.score), True, black)
    overRect = over.get_rect(center=(self.screenWidth, 100))
    self.frameSurface.blit(over, overRect)
    
    restart = medFont.render("Make a Y shape to restart", True, white, black)
    restartRect = restart.get_rect(center=(self.screenWidth, 400))
    self.frameSurface.blit(restart, restartRect)
    
    exit = medFont.render("Or dab to exit! Yes, dab.", True, white, black)
    exitRect = restart.get_rect(center=(self.screenWidth, 600))
    self.frameSurface.blit(exit, exitRect)
    
def matchY(self):
    leftElbowX, leftElbowY = self.leftElbowPos
    rightElbowX, rightElbowY = self.rightElbowPos
    leftHandX, leftHandY = self.leftHandPos
    rightHandX, rightHandY = self.rightHandPos
    headX, headY = self.headPos
    leftState = leftHandX < leftElbowX and leftHandY < leftElbowY and \
                leftHandY < headY
    rightState = rightHandX > rightElbowX and rightHandY < rightElbowY and \
                 rightHandY < headY
    return leftState and rightState

def dabbing(self):
    leftElbowX, leftElbowY = self.leftElbowPos
    rightElbowX, rightElbowY = self.rightElbowPos
    leftHandX, leftHandY = self.leftHandPos
    rightHandX, rightHandY = self.rightHandPos
    dab = abs(leftHandY - rightElbowY) < 30 
    leftState = leftHandX > leftElbowX and leftHandY < leftElbowY
    rightState = rightHandX > rightElbowX and rightHandY < rightElbowY
    return dab and leftState and rightState
