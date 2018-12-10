# ====================== Directory_and_File_Functions.py ===================== #

from Face_Recognition_Functions import *
import os

def isFileAnImg(fileName):
    """
    TODO
    Function Name:
        isFileAnImg
    Objective:
        Validate if fileName is an img file
    Input parameter(s):
        - fileName : str with the file's name
    Output parameter(s):
        - True (file is an img) : False (file not an img) 
    """
    imageTypes = ('.jpg','.png','.jpeg')
    for e in imageTypes:
        if fileName.endswith(e):
            return True
    return False

    """
    TODO
    Function Name:
        
    Objective:

    Input parameter(s):

    Output parameter(s):

    """

if __name__ == "__main__":
    pass