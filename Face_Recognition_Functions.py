# ====================== Face_Recognition_Functions.py ======================= #
"""
Documentation of the library face_recognition:
    https://face-recognition.readthedocs.io/en/latest/face_recognition.html
"""

# =============================== LIBRARIES ================================== #
import face_recognition
import cv2
import numpy as np
from PIL import Image
import json
import sys
import os
# ============================================================================ #

# =========================== GLOBAL VARIABLES =============================== #
knownPeople = {} # Dictionary: {key = Name, value = encoding}
JSONPath = "known_People.json"
facesLoaded = 0 # int determines if knownPeople was modified (add/delete elems)
# ============================================================================ #

# ============================= MAIN FUNTIONS ================================ #
def facesOnImg(imgObj):
    """
        Function Name:
            facesOnImg
        Objective:
            Return a list the of faces on the given image object.
        Input parameter(s):
            - imgObj: An image object loaded from with the face_recognition.load_image_file function
        Return value(s):
            - faceLocations: A list of tuples of found face locations in css (top, right, bottom, left) order.
    """
    # Use a built-in function from the library to detect faces
    faceLocations = face_recognition.face_locations(imgObj)
    return faceLocations

def isUnknownAKnownFace(unknownEncoding):
    """
        TODO
        Function Name:
            isUnknownAKnownFace
        Objective:
            Compare a new encoding with the ones stored in knownPeople dictionary
        Input parameter(s):
            - imgPath : unknownEndoing of data type <class numpy.ndarray>
        Return value(s):
            - String containing the name of the matching encoding, if any
    """
    matchingName = ""

    for tName, tEncoding in knownPeople.items():
        if areTheySameFace(unknownEncoding, tEncoding):
            matchingName = tName
            break

    return matchingName

def learnOnNewFace(imgPath, nameOfPerson):
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
                * 0 : The face was correctly learned OR nameOfPerson is already registered
                * -1 : There was a problem and the new face WASN'T learned, e.g. the 
                number of faces detected on the image were 0 or more than 1
    """
    global knownPeople
    # 0) If nameOfPerson already exists, exit func. returning 0
    if nameOfPerson in knownPeople.keys():
        print("\n ===== Face already registered! ===== \n")
        return 0

    # 1) Find faces on the image
    imgObj = face_recognition.load_image_file(imgPath)
    faceLocation = facesOnImg(imgObj)

    # 2) If not 1, return -1 : else, keep going
    if len(faceLocation) != 1:
        return -1 # Error because when learning a new face there must be exactly one to prevent ambiguity

    # 3) Store the new encoding (value) related to nameOfPerson (key)
    newEncoding = face_recognition.face_encodings(imgObj, faceLocation)[0]

    # 4) Convert numpy.ndarray ==> list
    knownPeople[nameOfPerson] = newEncoding.tolist()

    # 4) Return a success state
    return 0

def areTheySameFace(encodingOne, encodingTwo):
    """
        Function Name:
            areTheySameFace
        Objective:
            Compare two face's encodings and return a boolean determining if they are 
            the same person.
        Input parameter(s): Both lists, which must be processed before comparing
            - encodingOne 
            - encodingTwo
        Output parameter(s):
            - Boolean 'True' if there is a match; else 'False'.
    """
    # 1) Convert from type list to np.array, if necessary
    if type(encodingOne) != np.ndarray:
        encodingOne = np.array(encodingOne)
    if type(encodingTwo) != np.ndarray:
        encodingTwo = np.array(encodingTwo)

    # 2) First parameter must be a list of np.array and second parameter must
    # be a single np.array
    returnValue = face_recognition.compare_faces([encodingOne], encodingTwo)
    
    # 3) returnValue is a one-element list, thus return element 0
    return(returnValue[0])

def loadKnownFaces(jsonPath):
    """
        Function Name:
            loadKnownFaces
        Objective:
            Load the dictonary that contains the information about the information from the already learned faces.
        Input parameter(s):
            - jsonPath : A string of the relative path to the JSON file.
        Return value(s):
            * None because the data is loaded in a global dictionary called knownPeople
    """
    global knownPeople
    global facesLoaded
    print("\n===== Loading data from {} ... =====\n".format(jsonPath))

    with open("known_People.json", 'r') as read_file:
        knownPeople = json.load(read_file)  
    facesLoaded = len(knownPeople)

    print("\n===== Loaded from {} successful =====\n".format(jsonPath))

def saveNewFaces():
    """
        Function Name:
            saveNewFaces
        Objective:

        Input parameter(s):
            * None
        Output parameter(s):
            * None
    """
    global knownPeople
    global facesLoaded

    # Check if elements were added/deleted during runtime
    if facesLoaded != len(knownPeople):
        with open("known_People.json", 'w') as write_file:
            json.dump(knownPeople, write_file)

        print("\n===== Saved knownPeople in JSON file correctly =====\n")

def printKnownPeople():
    """
        Function Name:
            printKnownPeople
        Objective:
            Print data stored on global dictionary 'knownPeople'.
        Input parameter(s):
            * None
        Output parameter(s):
            * None
    """
    global knownPeople
    print("\n")
    for k,v in knownPeople.items():
        print("-------------------------------------------")
        print(k, "==>", v[0:2], " ... ", v[-2:])
    print("-------------------------------------------\n")

# def whoAreThey(foundFaces):
    """
        TODO
        Function Name:
            whoAreThey
        Objective:
            Take a picture using OpenCV and check for known people on the image. The
            algorithm will be a brut force comparison between the encodings from the
            found faces and the encodings on people stored in 'knownPeople' dict.
        Input parameter(s):
            - foundFaces : A list of tuples of found face locations in css (top, right, bottom, left) order.
        Output parameter(s):
            - matches : list of names (strings) of the people found on the image
    """

"""
    TODO
    Function Name:
        
    Objective:

    Input parameter(s):

    Output parameter(s):
"""

if __name__ == "__main__":
    loadKnownFaces("known_People.json")

    imgs = ["Leo_Messi/1.jpg", "Cristiano_Ronaldo/2.jpg", "Gareth_Bale/3.jpg","Leo_Messi/2.jpg"]

    takePicRegistration("Sebastian Rivera")

    # print("Register Messi: ", learnOnNewFace(imgPath, "Leonel Messi"))
    # print("Register Cristiano: ", learnOnNewFace(imgPath_CR7, "Cristiano Ronaldo"))
    # print("Register Gareth: ", learnOnNewFace(imgPath_GB, "Gareth Bale"))
    
    # for imgPath in imgs:
    #     imgObject = face_recognition.load_image_file(imgPath)
    #     faceEncoding = face_recognition.face_encodings(imgObject)
    #     # newFaceEncoding = faceEncoding[0].tolist()
    #     newFaceEncoding = faceEncoding[0]
    #     print(imgPath)
    #     for k, v in knownPeople.items():
    #         if areTheySameFace(newFaceEncoding, v):
    #             print(k)

    # printKnownPeople()
    saveNewFaces()