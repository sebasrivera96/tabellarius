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
theDB = 0
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
    for tObject in theDB.values():
        # Extract information from the TabellariusPerson obj
        tName = tObject.getName()
        tEncoding = tObject.getEncodings()

        if areTheySameFace(unknownEncoding, tEncoding):
            matchingName = tName
            break

    return matchingName

def isNameRegistered(nameToTest):
    global knownPeople
    return nameToTest in knownPeople.keys() or nameToTest in theDB.keys()

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
    if isNameRegistered(nameOfPerson):
        print("\n ===== Face already registered! ===== \n")
        return 0

    # 1) Find faces on the image
    imgObj = face_recognition.load_image_file(imgPath)
    faceLocation = facesOnImg(imgObj)

    # 2) If not 1, return -1 : else, keep going
    if len(faceLocation) != 1:
        # Error because when learning a new face there must be exactly one to 
        # prevent ambiguity
        return -1 

    # 3) Store the new encoding (value) related to nameOfPerson (key)
    newEncoding = face_recognition.face_encodings(imgObj, faceLocation)[0]

    # 4) Convert numpy.ndarray ==> list
    # knownPeople[nameOfPerson] = newEncoding.tolist()
    theDB.createPerson(nameOfPerson, newEncoding.tolist)

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
            paths = firebasePerson.val()["pathsToImgs"]

            self.addPerson(name, encodings, paths)

    def addPerson(self, name, faceEncodings=[], paths=[]):
        """

        """
        newPerson = TabellariusPerson(name, faceEncodings, paths)
        self.registeredPeople[name] = newPerson

    def createPerson(self, name, faceEncodings, paths=[""]):
        """
        This person is completly new and must be added to the firebaseDB
        """
        self.addPerson(name, faceEncodings, paths)
        data = {"encodings" : faceEncodings, "pathsToImgs" : paths}
        self.dbHandle.child("People").child(name).set(data)
        
    def printRegisteredPeople(self):
        for k, v in self.registeredPeople.items():
            print("{} ==> {}, {}".format(k,v.getEncodings(), v.getPaths()))

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
        self.dbHandle.child("People").child(name).update({"encodings" : encoding})
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
    # loadKnownFaces("known_People.json")

    # imgs = ["Leo_Messi/1.jpg", "Cristiano_Ronaldo/2.jpg", "Gareth_Bale/3.jpg","Leo_Messi/2.jpg"]

    # takePicRegistration("Sebastian Rivera")

    # saveNewFaces()
    enc = [-0.12451215088367462, 0.1324130743741989, 0.016436217352747917, -0.05885402113199234, -0.2077673375606537, 0.08744069933891296, -0.08062275499105453, -0.027331694960594177, 0.10549729317426682, -0.04180077463388443, 0.2250259667634964, -0.049243710935115814, -0.2720992863178253, -0.024380424991250038, -0.07537446916103363, 0.15143989026546478, -0.11014050245285034, -0.058159492909908295, -0.10049812495708466, -0.2121541053056717, -0.03928423672914505, 0.06940678507089615, -0.016132911667227745, 0.05956858769059181, -0.1668822169303894, -0.23768137395381927, -0.0031539034098386765, -0.16372984647750854, 0.09612885117530823, -0.15594062209129333, -0.03863710165023804, 0.06346476078033447, -0.11029714345932007, -0.033698659390211105, 0.03575294464826584, 0.0020417198538780212, -0.02842068485915661, -0.12709519267082214, 0.22558936476707458, -0.07350572198629379, -0.0549318790435791, 0.013971186242997646, 0.1341504454612732, 0.24512538313865662, 0.11907759308815002, -0.00849852617830038, 0.04727025702595711, -0.07700493186712265, 0.19799953699111938, -0.19360136985778809, 0.14015409350395203, 0.1467822790145874, 0.11901912093162537, 0.09623400866985321, 0.03703257441520691, -0.18007759749889374, -0.02905355766415596, 0.2195032835006714, -0.21728718280792236, 0.08397090435028076, 0.05658569186925888, 0.027492068707942963, -0.1362631767988205, -0.1524336040019989, 0.19807250797748566, 0.20429719984531403, -0.1131497472524643, -0.18027709424495697, 0.15253660082817078, -0.15343277156352997, -0.04591187462210655, 0.0405857190489769, -0.1306769698858261, -0.12891371548175812, -0.1927756518125534, 0.12198351323604584, 0.276944100856781, 0.23721054196357727, -0.162721186876297, -0.007861684076488018, -0.02092725969851017, -0.05864158272743225, 0.0021281444933265448, 0.024826254695653915, -0.12459409236907959, -0.12413810193538666, 0.030235398560762405, 0.019553247839212418, 0.17502322793006897, 0.009146051481366158, -0.008737161755561829, 0.20757119357585907, 0.0891205221414566, -0.06979658454656601, -0.001283283345401287, 0.024261631071567535, -0.18123780190944672, -0.06716939806938171, -0.054231829941272736, 0.0013412954285740852, 0.0023893509060144424, -0.1214044913649559, 0.029713772237300873, 0.07594374567270279, -0.19027775526046753, 0.1861744374036789, -0.031743697822093964, -0.0038180220872163773, -0.006893208250403404, 0.025142189115285873, -0.055949628353118896, -0.018132342025637627, 0.20743416249752045, -0.19672170281410217, 0.20113429427146912, 0.0728132575750351, 0.10999970138072968, 0.18571922183036804, 0.10877353698015213, 0.12610620260238647, 0.045428402721881866, -0.0010007377713918686, -0.10267752408981323, -0.12744958698749542, 0.10754186660051346, -0.10538624972105026, 0.03396880254149437, 0.061288654804229736]
    # Test for loading data from Firebase DB
    theDB = RuntimeDB(config)
    theDB.loadData()
    # theDB.printRegisteredPeople()
    theDB.updateEncoding("Leonel Messi", enc)    