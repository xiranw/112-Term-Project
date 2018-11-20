# displays starting screen
    # run logic inspired by: https://www.youtube.com/watch?v=rLrMPg-GCqo

import pygame

def run(self):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                self.done = True
        
        self.drawKinectFrame()
        titleFont = pygame.font.SysFont("Arial", 80)
        text = titleFont.render("Make a Y shape to start!", False, (0, 0, 0))
        self.frameSurface.blit(text, (600, 100))
        self.getJointPos()
        if matchY(self):
            waiting = False
        
        self.adjustKinectFrame()
        
        pygame.display.update()
        self.clock.tick(60)

def matchY(self):
    rightElbowX, rightElbowY = self.rightElbowPos
    rightHandX, rightHandY = self.rightHandPos
    headX, headY = self.headPos
    if rightHandX > rightElbowX and rightHandY < rightElbowY and \
        rightHandY < headY: # only checks right arm for now
        return True
    return False