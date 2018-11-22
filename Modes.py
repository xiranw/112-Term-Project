# starting and ending screen logic
# CITATION - switching screens logic inspired by: https://www.youtube.com/watch?v=rLrMPg-GCqo
# CITATION - draw text in rect: 

import pygame
pygame.font.init()

black = (0, 5, 45)
white = (243, 247, 241)

titleFont = pygame.font.SysFont("comicsansms", 100)
medFont = pygame.font.SysFont("comicsansms", 70)

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
        
        self.adjustKinectFrame()
        
        pygame.display.update()
        self.clock.tick(60)

def drawStartText(self):
    title = titleFont.render("Shape Matching Game", True, black)
    titleRect = title.get_rect(center=(self.screenWidth, 100))
    self.frameSurface.blit(title, titleRect)
    
    play = titleFont.render("PLAY", True, white, black)
    #CITATION - anchor learned from
    playButton = play.get_rect(topleft=(self.screenWidth/4, 400))
    self.playButtonSize = playButton.size
    self.frameSurface.blit(play, playButton)
    
    levelEditor = titleFont.render("EDITOR", True, white, black)
    editorButton = levelEditor.get_rect(topleft=(self.screenWidth/4, 700))
    self.editorButtonSize = editorButton.size
    self.frameSurface.blit(levelEditor, editorButton)

def playClicked(self):
    x1, y1 = self.screenWidth/4, 400
    deltaX, deltaY = self.playButtonSize
    leftHandX, leftHandY = self.leftHandPos
    return x1 < leftHandX < x1 + deltaX and y1 < leftHandY < y1 + deltaY

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
    
    exit = medFont.render("Or make an O shape to exit", True, white, black)
    exitRect = restart.get_rect(center=(self.screenWidth, 600))
    self.frameSurface.blit(exit, exitRect)
    
def matchY(self):
    rightElbowX, rightElbowY = self.rightElbowPos
    rightHandX, rightHandY = self.rightHandPos
    headX, headY = self.headPos
    return rightHandX > rightElbowX and rightHandY < rightElbowY and \
           rightHandY < headY #only checks right arm for now

def matchO(self):
    return False
