# initializes user levels in a global variable
# CITATION - using global variables across files: 
# https://stackoverflow.com/questions/13034496/using-global-variables-between-files

def __init__():
    global editedLevels
    editedLevels = []
    global levelsToPlay
    levelsToPlay = []
    global highScore
    highScore = 0
