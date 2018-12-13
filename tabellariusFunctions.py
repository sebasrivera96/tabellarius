# ====================== tabellariusFunctions.py ======================= #
"""
- Author: Sebastian Rivera Gonzalez
- Official Github from Pyrebase:
    https://github.com/thisbejim/Pyrebase
- Documentation of the library face_recognition:
    https://face-recognition.readthedocs.io/en/latest/face_recognition.html
"""

# =============================== LIBRARIES ================================== #
import face_recognition
import cv2
import pyrebase
import numpy as np
from PIL import Image
import json
import sys
import os
import time
# ============================================================================ #

# =========================== GLOBAL VARIABLES =============================== #
knownPeople = {} # Dictionary: {key = Name, value = encoding}
JSONPath = "/home/sebasrivera96/Documents/Dev/tabellarius/known_People.json"
facesLoaded = 0 # int determines if knownPeople was modified (add/delete elems)
config = {  "apiKey": "AIzaSyB0jgw-XexiMlBeyFVwUQKUSaRAd5WbDvg",
            "authDomain": "thefirstapp-80dcc.firebaseapp.com",
            "databaseURL": "https://thefirstapp-80dcc.firebaseio.com",
            "projectId": "thefirstapp-80dcc",
            "storageBucket": "thefirstapp-80dcc.appspot.com",
            "messagingSenderId": "601653648941"}
# ============================================================================ #

# ========================= FACE RECOGNITION FUNTIONS ======================== #
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
        Function Name:
            isUnknownAKnownFace
        Objective:
            Compare a new encoding with the ones stored in knownPeople dictionary
        Input parameter(s):
            - imgPath : unknownEndoing of data type <class numpy.ndarray>
        Return value(s):
            - String containing the name of the matching encoding, if any. Empty str returned when no match.
    """
    global theDB
    matchingName = ""

    # for tName, tEncoding in knownPeople.items():
    for tObject in theDB.getValues():
        # Extract information from the TabellariusPerson obj
        tName = tObject.getName()
        tEncoding = tObject.getEncodings()

        if areTheySameFace(unknownEncoding, tEncoding):
            matchingName = tName
            break

    return matchingName

def isNameRegistered(nameToTest):
    # global knownPeople
    # return nameToTest in knownPeople.keys() 
    global theDB
    return nameToTest in theDB.registeredPeople.keys()

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
    global theDB
    
    # 0) If nameOfPerson already exists, exit func. returning 0
    if isNameRegistered(nameOfPerson):
        print("\n ===== Face already registered! ===== \n")
        return 0

    # 1) Find faces on the image
    imgObj = face_recognition.load_image_file(imgPath)
    faceLocation = facesOnImg(imgObj)

    # 2) If not 1, return -1 : else, keep going
    if len(faceLocation) != 1:
        # Error because when learning a new face there must be exactly one to prevent ambiguity
        return -1 

    # 3) Store the new encoding (value) related to nameOfPerson (key)
    newEncoding = face_recognition.face_encodings(imgObj, faceLocation)[0]

    # 4) Convert numpy.ndarray ==> list
    # knownPeople[nameOfPerson] = newEncoding.tolist()
    theDB.createPerson(nameOfPerson, newEncoding.tolist())

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

    with open(JSONPath, 'r') as read_file:
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
        with open(JSONPath, 'w') as write_file:
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

def eraseFace(eraseName):
    """
        TODO
        Function Name:
            eraseFace
        Objective:
            Erase an element from knownPeople dictionary
        Input parameter(s):
            - eraseName : string to erase a specific value.
        Output parameter(s):
            - Failure status -1, in case key value is not found
    """
    return knownPeople.pop(eraseName, -1)

    """
        TODO
        Function Name:
            
        Objective:

        Input parameter(s):

        Output parameter(s):
    """

# ============================================================================ #

# ============================ PYREBASE FUNCTIONS ============================ #
class TabellariusPerson:

    # ===== ATTRIBUTES ===== #
    name = ""
    faceEncodings = []
    pathsToImgs = []

    # ===== METHODS ===== #
    def __init__(self, tName = "", tFaceEncodings = [], tPathsToimgs = []):
        self.name = tName
        self.faceEncodings = tFaceEncodings
        self.pathsToImgs = tPathsToimgs

    def getName(self):
        return self.name

    def setName(self, tName):
        self.name = tName
    
    def getEncodings(self):
        return self.faceEncodings

    def setEncodings(self, tFaceEncodings):
        self.faceEncodings = tFaceEncodings

    def getPaths(self):
        return self.pathsToImgs        

    def addPath(self, newPath):
        self.pathsToImgs.append(newPath)

    def orderPaths(self):
        raise NotImplementedError

class RuntimeDB:

    # ===== ATTRIBUTES ===== #
    firebaseHandle = ""
    dbHandle = ""
    registeredPeople = {}

    # ===== METHODS ===== #
    def __init__(self, config):
        self.firebaseHandle = pyrebase.initialize_app(config)
        self.dbHandle = self.firebaseHandle.database()
    
    def loadData(self):
        firebasePeople = self.dbHandle.child("People").get()

        for firebasePerson in firebasePeople.each():

            name = firebasePerson.key()
            encodings = firebasePerson.val()["encodings"]
            try:
                paths = firebasePerson.val()["pathsToImgs"]
            except:
                paths = []

            self.addPerson(name, encodings, paths)

    def addPerson(self, name, faceEncodings=[], paths=[]):
        """

        """
        newPerson = TabellariusPerson(name, faceEncodings, paths)
        self.registeredPeople[name] = newPerson

    def createPerson(self, name, faceEncodings, paths = []):
        """
        This person is completly new and must be added to the firebaseDB
        """
        self.addPerson(name, faceEncodings, paths)
        print(faceEncodings)
        data = {"encodings" : faceEncodings}
        self.dbHandle.child("People").child(name).set(data)
        
    def printRegisteredPeople(self):
        for k, v in self.registeredPeople.items():
            print("{} ==> {}..., {}".format(k,v.getEncodings()[0:3], v.getPaths()))

    def updatePaths(self):
        for name, tObj in self.registeredPeople.items():
            self.dbHandle.child("People").child(name).update({"pathsToImgs" : tObj.getPaths()})

    def updateRuntimePaths(self, facesMatched, path):
        """
        TODO
        Function Name:
            
        Objective:

        Input parameter(s):

        Output parameter(s):
        """
        for nameOfFace in facesMatched:
            self.registeredPeople[nameOfFace].addPath(path)

    def updateEncoding(self, name, encoding):
        self.dbHandle.child("People").child(name).update({"other" : encoding})

    def getValues(self):
        return self.registeredPeople.values()

    def getKeys(self):
        return self.registeredPeople.keys()

# ===== Initialization of the RuntimeDB ... ===== #
theDB = RuntimeDB(config)
theDB.loadData()
# ============================================================================ #

# ============================= OPENCV FUNCTIONS ============================= #
def takePic(pathToSavePic = "./temp.jpg", showImage = False):
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
    # TODO try/catch when opening the camera
    cap = cv2.VideoCapture(0)
    time.sleep(1) # Prevents the image to be dark
    _, frame = cap.read()
    cv2.imwrite(pathToSavePic, frame)

    if showImage:
        cv2.imshow("New Picture", frame)
        cv2.waitKey(0)
    
    cap.release()
    cv2.destroyAllWindows()

# ============================================================================ #

# ======================== DIRECTORY & FILES FUNCTIONS ======================= #
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

# ============================================================================ #

    """
    TODO
    Function Name:
        
    Objective:

    Input parameter(s):

    Output parameter(s):
    """

if __name__ == "__main__":

    # Test for loading data from Firebase DB
    theDB = RuntimeDB(config)
    theDB.loadData()
    # theDB.printRegisteredPeople()
    theDB.updateEncoding("Leonel Messi", "koko")    