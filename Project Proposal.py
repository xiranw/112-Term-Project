### Project Description ###
# The project will be a Kinect-supported game called "Shape-Matching Game". 
# A shape formed by connecting multiple circles will be displayed on the screen,
# and the player gains points by touch all circles simultaneously with their 
# hands, feet, and/or head. The game will also support multi-player and
# include a level-editor.

### Competitive Analysis ###


### Structual Plan ###
# __main__.py
    # class Main()
    # function __init__
    # function drawKinectFrame; getJointPos
    # function runMain
    # end of file calls runStartScreen, then runMain

# startScreen.py
    # function drawStartScreen
    # function buttonTouched
    # function runStartScreen
        # exits if play button touched
        # calls runLevelEditor if make level button touched

# circleClass.py
    # object Circle
        # attribute position
        # function draw
        # function isHit
    
    # object targetCircle inherits from Circle
    
    # object bodyCircle inherits from Circle
    
    # function generateTargetCircles; generateBodyCircles
    # function checkCollisions; isShapeComplete
    
    # function drawAll

# levelEditor.py
    # function drawLevelEditor
    # function addShape

### ALgorithmic Plan ###
# for creating targets, checking overlap, and generating levels

# step 1: generate targets
    # randomly placed and from pre-made levels
    # single player:
        # random.choice 2, 3, or 4 targets
        # 1/4 of the time pre-made levels (weigh choice somehow?)
        # targets must be fully on screen and cannot overlap
        # 100 pixels < seperation < 1000 pixels
    # two-player:
        # 5 or more targets
        # 1/2 pre-made levels to avoid getting messy

# step 2: generate body circles
    # converts joint locations to color-frame locations
    # draws five dots at head, left/right hand, and left/right food
        # smaller than targets, different fill
    # maybe add elbows too for complexity
    
# step 3: check collisions
    # loop through each target and each bodyCircle
        # if they overlap
            # change bodyCircle color
            # change status of target to hit
    # if all targets hit, increment score + back to step 1

### Timeline Plan ###


###Version Control Plan###
# backup code using github: https://github.com/xiranw/112-Term-Project

###Module List###
# Kinect
# Pygame