# ====================== Directory_and_File_Functions.py ===================== #

from Face_Recognition_Functions import *
import os


def isPathValid(pathToTest):
    """
    Function Name:
        isPathValid
    Objective:
        Check is the path is valid by looking for it.
    Input parameter(s):
        - pathToTest : String containing the path to a directory.
    Output parameter(s):
        - isValid : The path will be valid until the opposite is demonstrated.
    """
    isValid = True
    try:
        os.chdir(pathToTest)
    except:
        return not isValid


    # If path is valid, continue
    filesInPath = os.listdir()
    peopleInImgs = {} # Dictionary to store those images which contain known people

    print("Images in ==> {}\n".format(pathToTest))
    for currentFile in filesInPath:
        # If file is an image, look for knownPeople
        print("- " + currentFile)

    return isValid

    """
    TODO
    Function Name:
        
    Objective:

    Input parameter(s):

    Output parameter(s):

    """

if __name__ == "__main__":
    isPathValid("/home/sebasrivera96/Documents/Dev/tabellarius/")