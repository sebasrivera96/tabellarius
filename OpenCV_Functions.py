import numpy as np
import cv2
import time

"""
    TODO
    Function Name:
        takePic
    Objective:
        Take a picture an store it on the local directory ==> "./temp.jpg"
    Input parameter(s):
        - pathToSavePic : relative path to save the pic that will be captured. 
            * Default value = "./temp.jpg"
        - showImage : boolean val that determines if the img will be shown or not.
            * Default value = False
    Output parameter(s):

"""
def takePic(pathToSavePic = "./temp.jpg", showImage = False):

    cap = cv2.VideoCapture(0)
    time.sleep(0.1) # Prevents the image to be dark
    _, frame = cap.read()
    cv2.imwrite(pathToSavePic, frame)

    if showImage:
        cv2.imshow("New Picture", frame)
        cv2.waitKey(0)
    
    cap.release()

"""
    TODO
    Function Name:
        
    Objective:

    Input parameter(s):

    Output parameter(s):
"""
