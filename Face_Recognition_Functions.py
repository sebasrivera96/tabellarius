import face_recognition
from PIL import Image
import sys
import os

# ============================= MAIN FUNTIONS ==================================
"""
Function Name:
    facesOnImg
Objective:
    Load an image with the face_recognition library and return a list the of 
    human faces on the given image.
Input parameter(s):
    - imgPath: A relative path to the image. Preferably consider to have 
        a local director to the repository to store the images.
Return value(s):
    - numOfFaces :
        * faceLocations: A list of tuples of found face locations in 
            css (top, right, bottom, left) order.
"""
def facesOnImg(imgPath):
    numOfFaces = 0
    imgObj = face_recognition.load_image_file(imgPath)

    # Use a built-in function from the library to detect faces
    faceLocations = face_recognition.face_locations(imgObj)
    return faceLocations

"""
Function Name:
    identifyKnownPeople
Objective:
    Load an image with the face_recognition library and search for a known 
    person using the encodings that were previously generated and stored.
Input parameter(s):
    - imgPath : A relative path to the image. Preferably consider to have 
        a local director to the repository to store the images.
    - facesEncodings : TODO define wher this encodings will be stored, e.g.
        on a txt file, on a directory created during the runtime.
Return value(s):
    - recognizedPeople : A list containig the names of the recognized people.
"""
def identifyKnownPeople(imgPath, facesEncodings):
    imgObj = face_recognition.load_image_file(imgPath)
    recognizedPeople = []

    # 1) Find the faces on the image

    # 2) Compare the found faces with the past encodings

    # 3) Store the known people, if there is a match

    # 4) Return the list with the names
    return recognizedPeople

"""
Function Name:
    learnOnNewFace
Objective:
    An image with a single face will be received to learn on a new face. If the
    number of detected faces on the img is not 1, an error will be returned.
Input parameter(s):
    - imgPath : A relative path to the image.
    - nameOfPerson : A string that represents the name of the new person.
    - facesDict : Dictionary with key NAME : value FACE_ENCODING.
Return value(s): 
    - successState : Integer value communicating success or failure
        * 0 : The face was correctly learned
        * -1 : There was a problem and the new face WASN'T learned, e.g. the 
        number of faces detected on the image were 0 or more than 1
"""
def learnOnNewFace(imgPath):
    # imgObj = face_recognition.load_image_file(imgPath)
    numOfFaces = facesOnImg(imgPath)

    # 1) Find faces on the image

    # 2) If not 1, return -1 : else, keep going

    # 3) Store the new encoding (value) related to nameOfPerson (key)

    # 4) Return a success state
    return 0


"""
Function Name:
    loadKnownFaces
Objective:
    Load the dictonary that contains the information about the information 
    from the already learned faces.
Input parameter(s):
    - jsonPath : A string of the relative path to the JSON file.
Return value(s):
    - facesDict : Dictionary with key NAME : value FACE_ENCODING.
"""
def loadKnownFaces(jsonPath):


"""
Function Name:
    saveNewFaces
Objective:

Input parameter(s):

Output parameter(s):

"""
def saveNewFaces(facesDict)
