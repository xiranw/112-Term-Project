# starting, editing, playing, and ending screen logic

import pygame
pygame.font.init()

import CircleClass
import UserLevels
import time

black = (0, 5, 45)
white = (243, 247, 241)
yellow = (240, 236, 87)
green = (103, 229, 191)

titleFont = pygame.font.SysFont("comicsansms", 100)
medFont = pygame.font.SysFont("comicsansms", 70)
smallFont = pygame.font.SysFont("comicsansms", 65)

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
    
    play = titleFont.render("PLAY", True, white, black)
    #CITATION - anchor learned from blah
    playButton = play.get_rect(topleft=(self.screenWidth/4, 400))
    self.playButtonSize = playButton.size
    self.frameSurface.blit(play, playButton)
    
    levelEditor = titleFont.render("EDITOR", True, white, black)
    editorButton = levelEditor.get_rect(topleft=(self.screenWidth/4, 700))
    self.editorButtonSize = editorButton.size
    self.frameSurface.blit(levelEditor, editorButton)

### Navigation to play or Level Editor

def playClicked(self):
    return buttonClicked(self, "playButton")

def editorClicked(self):
    return buttonClicked(self, "editorButton")

# CITATION - getting size of button: 
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
    leftHandX, leftHandY = self.leftHandPos
    return x1 < leftHandX < x1 + deltaX and y1 < leftHandY < y1 + deltaY

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
        
        if self.targetCircles == []: #game begins
            CircleClass.generateTargets(self)
        elif CircleClass.isShapeComplete(self):
            self.score += 10 * len(self.targetCircles)
            CircleClass.generateTargets(self)
            t1 = t0 #reset level timer
        
        elif self.canSkip and self.isJump() and self.skipsLeft > 0:
            CircleClass.generateTargets(self)
            t1 = t0
            self.skipsLeft -= 1
            self.canSkip = False
            self.hintShown = True
            self.showHint = False
        elif not self.isJump():
            self.canSkip = True
        
        if levelTime > 10 and self.hintShown == False:
            self.showHint = True
            
        CircleClass.updateTargets(self)
        CircleClass.generateBodyCircles(self)
        CircleClass.checkCollisions(self)
        CircleClass.playDrawAll(self)
        
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
        if saveClicked(self) and self.canSave == True:
            UserLevels.editedLevels.append(self.userLevel)
            UserLevels.levelsToPlay.append(self.userLevel)
            self.canSave = False
            self.userLevel = []
        elif not saveClicked(self):
            self.canSave = True
            if backClicked(self):
                onEditorScreen = False
        
        if self.canEdit and self.leftHandState == 3: #closed fist
            CircleClass.addTarget(self)
            self.canEdit = False
        else:
            if self.leftHandState != 3:
                self.canEdit = True
            if self.leftHandState == 4: # lasso
                CircleClass.deleteTarget(self)
        CircleClass.getHandCircle(self)
        CircleClass.editorDrawAll(self)
        
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
    
    save = titleFont.render("SAVE", True, white, black)
    #CITATION - anchor learned from blah
    saveButton = save.get_rect(topleft=(330, 50))
    self.saveButtonSize = saveButton.size
    self.frameSurface.blit(save, saveButton)
    
    back = titleFont.render("BACK", True, white, black)
    #CITATION - anchor learned from blah
    backButton = back.get_rect(topleft=(1300, 50))
    self.backButtonSize = backButton.size
    self.frameSurface.blit(back, backButton)

def saveClicked(self):
    return buttonClicked(self, "saveButton")

def backClicked(self):
    return buttonClicked(self, "backButton")

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
        elif matchO(self):
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

def matchO(self):
    leftElbowX, leftElbowY = self.leftElbowPos
    rightElbowX, rightElbowY = self.rightElbowPos
    leftHandX, leftHandY = self.leftHandPos
    rightHandX, rightHandY = self.rightHandPos
    dab = abs(leftHandY - rightElbowY) < 30 
    leftState = leftHandX > leftElbowX and leftHandY < leftElbowY
    rightState = rightHandX > rightElbowX and rightHandY < rightElbowY
    return dab and leftState and rightState
