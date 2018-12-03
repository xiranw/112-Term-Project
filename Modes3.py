# starting, editing, playing, and ending screen logic

import pygame
pygame.font.init()

import Shapes
import Globals
import time
import random

red = (255, 0, 0)
outlineRed= (255, 0, 0)
yellow = (232, 220, 62)
green = (103, 229, 191)
purple = (155, 62, 233)
black = (0, 5, 45)
white = (243, 247, 241)

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
        x1, y1 = 1500, 460
        deltaX, deltaY = self.slowButtonSize
    elif button == "med":
        x1, y1 = 1500, 560
        deltaX, deltaY = self.medButtonSize
    elif button == "fast":
        x1, y1 = 1500, 660
        deltaX, deltaY = self.fastButtonSize
    
    booleanList = []
    for body in self.bodyDict:
        allJoints = self.bodyDict[body][0]
        if allJoints == []:
            continue
        leftHandX, leftHandY = allJoints[1]
        clicked = x1 < leftHandX < x1 + deltaX and y1 < leftHandY < y1 + deltaY
        booleanList.append(clicked)
    return checkBooleanOr(booleanList)

def checkBooleanOr(booleanList):
    # only needs one player performing the action
    for boolean in booleanList:
        if boolean == True:
            return True
    return False
    
def checkBooleanAnd(booleanList):
    #needs all players performing the action
    for boolean in booleanList:
        if boolean == False:
            return False
    return True
    
def drawDepthWarning(self):
    player = 0
    booleanList = []
    for body in self.bodyDict:
        allJoints = self.bodyDict[body][0]
        if allJoints == []:
            continue
        
        player += 1
        if player % 2 == 1:
            color = yellow
        else:
            color = purple
        
        depth = self.bodyDict[body][2][0]
        xCoordinate = allJoints[0][0]
        if depth < 150:
            instruction = medFont.render("Move Back!", True, color)
            instructionRect = instruction.get_rect(center=(xCoordinate, 240))
            self.frameSurface.blit(instruction, instructionRect)
            booleanList.append(True)
        elif depth > 190:
            instruction = medFont.render("Move forward!", True, color)
            instructionRect = instruction.get_rect(center=(xCoordinate, 240))
            self.frameSurface.blit(instruction, instructionRect)
            booleanList.append(True)
    
    return len(booleanList) > 0
    
### Start Screen ###

def runStartScreen(self):
    onStartScreen = True
    while onStartScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                onStartScreen = False
                self.exit = True

        self.drawKinectFrame()
        self.getJointPos()
        
        drawStartText(self)
        
        if not drawDepthWarning(self) and playClicked(self):
            onStartScreen = False
            self.play = True
        elif editorClicked(self):
            onStartScreen = False
            self.editor = True
       
        Shapes.getHandCircle(self)
        Shapes.drawStartShapes(self)
        
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
    self.score = 0
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

        #we have body frames, so can get skeletons
        self.getJointPos()
        
        #generates targets and increments score
        if self.targetCircles == []: #game begins
            resetVariables(self)
            Shapes.generateTargets(self)
        elif Shapes.isShapeComplete(self):
            if self.level == "static":    
                incrementScore(self)
                resetVariables(self)
                Shapes.generateTargets(self)
                t0 = t1 #reset level timer
            elif self.level == "moving":
                if self.alreadyMoving == False:
                    incrementScore(self)
                    self.newBomb = None
                    for circle in self.targetCircles:
                        if isinstance(circle, Shapes.movingTarget):
                            circle.moving = True
                    self.alreadyMoving = True
                    t3 = time.time()
                elif self.alreadyMoving == True:
                    self.score += 1
        
        if self.alreadyMoving == True:
            t4 = time.time()
            movingTime = t4 - t3
            if movingTime > 2.5:
                resetVariables(self)
                Shapes.generateTargets(self)
                t0 = t1
            
        for circle in self.targetCircles:
            if isinstance(circle, Shapes.movingTarget):
                circle.move()
    
        #skip logic
        if self.canSkip and isJump(self) and self.skipsLeft > 0:
            resetVariables(self)
            Shapes.generateTargets(self)
            t0 = t1
            self.skipsLeft -= 1
            self.canSkip = False
            self.hintShown = True
            self.showHint = False
        elif not isJump(self):
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
            if self.score > 50: #score can't be negative (cuz that's just sad)
                self.score -= 50
            resetVariables(self)
            Shapes.generateTargets(self)
            t0 = t1
        
        #depth
        if drawDepthWarning(self) and self.score > 0.2:
            self.score -= 0.2
            
        Shapes.updateTargets(self)
        Shapes.generateBodyCircles(self)
        Shapes.checkCollisions(self)
        Shapes.drawPlayShapes(self)
        
        drawPlayText(self)
        
        self.adjustKinectFrame()
        pygame.display.update()
    
    self.score = int(self.score)
    if self.score > Globals.highScore:
        Globals.highScore = self.score

def incrementScore(self):
    if self.newBomb != None:
        self.score += 100
    else: 
        self.score += 10 * len(self.targetCircles)
        
def drawPlayText(self):
    #draw score
    score = smallFont.render("SCORE: " + str(int(self.score)), True, white, black)
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

def isJump(self):
    booleanList = []
    for body in self.bodyDict:
        allJoints = self.bodyDict[body][0]
        if allJoints == []:
            continue
        leftFootY = allJoints[5][1]
        rightFootY = allJoints[6][1]
        if leftFootY == (-50, -50):
            return False
        jump = leftFootY < 750 and rightFootY < 750
        booleanList.append(jump)
    return checkBooleanAnd(booleanList)
        
def resetVariables(self):
    self.newBomb = None
    self.makeBomb = False
    self.choiceMade = False
    self.alreadyMoving = False

### Level Editor Screen ###

def runEditorScreen(self):
    onEditorScreen = True
    speed = 0.7
    while onEditorScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                onEditorScreen = False
                self.exit = True
    
        self.drawKinectFrame()
        self.getJointPos()
        
        drawEditorText(self)
        
        # save and back buttons
        if saveClicked(self) and len(self.userLevel) != 0:
            if self.userBomb == False:
                level = [self.userLevel, self.userBomb, 0]
            else:
                level = [self.userLevel, self.userBomb, self.newBomb.speed]
            Globals.editedLevels.append(level)
            Globals.levelsToPlay.append(level)
            self.userBomb, self.makeBomb = False, False
            self.newBomb = None
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
        
        Shapes.checkBomb(self, speed)
    
        if self.userBomb == True:
            try:
                if slowClicked(self) and self.newBomb.speed != 0.7:
                    self.makeBomb = True
                    speed = 0.7
                elif medClicked(self) and self.newBomb.speed != 0.9:
                    self.makeBomb = True
                    speed = 0.9
                elif fastClicked(self) and self.newBomb.speed != 1.2:
                    self.makeBomb = True
                    speed = 1.2
            except:
                pass
        
        # adding and deleting targets
        for body in self.bodyDict:
            allJoints = self.bodyDict[body][0]
            if allJoints == []:
                continue
            
            handState = self.bodyDict[body][1][0]
            leftHandPos = allJoints[1]
            canEdit = self.bodyDict[body][3]
            
            if canEdit and handState == 3: #closed fist
                Shapes.addTarget(self, leftHandPos)
                self.bodyDict[body][3] = False
            else:
                if handState != 3:
                    canEdit = True
                    self.bodyDict[body][3] = canEdit
                if handState == 4: # lasso
                    Shapes.deleteTarget(self, leftHandPos)
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
    
    question = medFont.render("Bomb?", True, black)
    questionRect = question.get_rect(topleft = (1550, 230))
    self.frameSurface.blit(question, questionRect)
    
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
    self.slowButtonSize = drawButton(self, "Slow", smallFont, "topleft", white, slowColor, (1500, 460))
    self.medButtonSize = drawButton(self, "Med", smallFont, "topleft", white, medColor, (1500, 560))
    self.fastButtonSize = drawButton(self, "Fast", smallFont, "topleft", white, fastColor, (1500, 660))
        
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
    
    highScore = medFont.render("High Score: " + str(Globals.highScore), True, black)
    highRect = highScore.get_rect(center=(self.screenWidth, 200))
    self.frameSurface.blit(highScore, highRect)
    
    restart = medFont.render("Make a Y shape to restart", True, white, black)
    restartRect = restart.get_rect(center=(self.screenWidth, 400))
    self.frameSurface.blit(restart, restartRect)
    
    exit = medFont.render("Or dab to exit! Yes, dab.", True, white, black)
    exitRect = restart.get_rect(center=(self.screenWidth, 600))
    self.frameSurface.blit(exit, exitRect)
    
    booleanList = []
    for body in self.bodyDict:
        allJoints = self.bodyDict[body][0]
        if allJoints == []:
            continue
        leftFootY = allJoints[5][1]
        rightFootY = allJoints[6][1]
        if leftFootY == (-50, -50):
            return False
        jump = leftFootY < 750 and rightFootY < 750
        booleanList.append(jump)
    return checkBooleanAnd(booleanList)
    
def matchY(self):
    booleanList = []
    for body in self.bodyDict:
        allJoints = self.bodyDict[body][0]
        if allJoints == []:
            continue
        headX, headY = allJoints[0]
        leftHandX, leftHandY = allJoints[1]
        rightHandX, rightHandY = allJoints[2]
        leftElbowX, leftElbowY = allJoints[3]
        rightElbowX, rightElbowY = allJoints[4]
        leftState = leftHandX < leftElbowX and leftHandY < leftElbowY and \
                    leftHandY < headY
        rightState = rightHandX > rightElbowX and rightHandY < rightElbowY and \
                     rightHandY < headY
        booleanList.append(leftState and rightState)
    return checkBooleanOr(booleanList)

def dabbing(self):
    booleanList = []
    for body in self.bodyDict:
        allJoints = self.bodyDict[body][0]
        if allJoints == []:
            continue
        leftHandX, leftHandY = allJoints[1]
        rightHandX, rightHandY = allJoints[2]
        leftElbowX, leftElbowY = allJoints[3]
        rightElbowX, rightElbowY = allJoints[4]
        
        dab = abs(leftHandY - rightElbowY) < 30 
        leftState = leftHandX > leftElbowX and leftHandY < leftElbowY
        rightState = rightHandX > rightElbowX and rightHandY < rightElbowY
        booleanList.append(dab and leftState and rightState)
    return checkBooleanOr(booleanList)
