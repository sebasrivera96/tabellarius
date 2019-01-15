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
from PIL import Image, ImageDraw
import json
import sys
import os
import time
# ============================================================================ #

# =========================== GLOBAL VARIABLES =============================== #
knownPeople = {} # Dictionary: {key = Name, value = encoding}
JSONPath = "/home/sebasrivera96/Documents/Dev/tabellarius/known_People.json"
facesLoaded = 0 # int determines if knownPeople was modified (add/delete elems)
defaultLocation = "/home/sebasrivera96/Pictures/Renombradas/Aaron_Hernandez_RESIZED.jpg"
config = {  "apiKey": "AIzaSyB0jgw-XexiMlBeyFVwUQKUSaRAd5WbDvg",
            "authDomain": "thefirstapp-80dcc.firebaseapp.com",
            "databaseURL": "https://thefirstapp-80dcc.firebaseio.com",
            "projectId": "thefirstapp-80dcc",
            "storageBucket": "thefirstapp-80dcc.appspot.com",
            "messagingSenderId": "601653648941"}
# ============================================================================ #

# ========================= FACE RECOGNITION FUNCTIONS ======================== #
def facesOnImg(imgObj):
    """
        Function Name:
            facesOnImg
        Objective:
            Return a list the of faces on the given image object.
        Input parameter(s):
            - imgPath: A path to the image file.
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

    # for tName, tEncoding in knownPeople.items():
    for tObject in theDB.getValues():

        # Extract information from the TabellariusPerson obj
        tName = tObject.getName()
        tEncoding = tObject.getEncodings()

        if areTheySameFace(unknownEncoding, tEncoding):
            return tName

    # Return None if no match was found
    return None

def isNameRegistered(nameToTest):
    global theDB
    return nameToTest in theDB.registeredPeople.keys()

def isThereASingleFace(faceLocations):
    return len(faceLocations) == 1

def getEncSingleFace(imgObj, facesLocation):
    encodingOfFace = face_recognition.face_encodings(imgObj, facesLocation)[0]
    return encodingOfFace

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
    
    # -> If nameOfPerson already exists, exit func. returning 0
    if isNameRegistered(nameOfPerson):
        return 1

    # -> Create imgObj with face_recognition module
    imgObj = face_recognition.load_image_file(imgPath)

    # -> Find faces on the image
    faceLocation = facesOnImg(imgObj)

    # -> If just one face found, keep going
    if isThereASingleFace(faceLocation):
        # -> Store the new encoding (value) related to nameOfPerson (key)
        newEncodingAsNumpyArray = getEncSingleFace(imgObj, faceLocation)

        # -> Convert numpy.ndarray ==> list
        newEncodingAsList = newEncodingAsNumpyArray.tolist()
        theDB.createPerson(nameOfPerson, newEncodingAsList)

        # -> Return success state
        return 0

    else:
        # -> Return failure state
        return -1

def convertToNpArray(tEncoding):
    # -> Convert from type list to np.array, IF necessary
    if type(tEncoding) != np.ndarray:
        return np.array(tEncoding)
    else:
        return tEncoding

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
            - tolerance is a key parameter for success
        Output parameter(s):
            - Boolean 'True' if there is a match; else 'False'.
    """
    # -> Ensure the data type of the encodings
    encodingOne = convertToNpArray(encodingOne)
    encodingTwo = convertToNpArray(encodingTwo)

    # -> 1st param. must be a list of np.array and 2nd param must be a single np.array
    boolSameFace = face_recognition.compare_faces([encodingOne], encodingTwo, tolerance=0.525)
    
    # 3) boolSameFace is a one-element list, thus return element 0
    return(boolSameFace[0])

def getPathOfImgToLookOn(takeNewPic, pathOfImage):
    if takeNewPic:
        takePic(pathToSavePic=pathOfImage)
        
        # Modify pathOfImg to the new captured image
        pathOfImage = "./temp.jpg"

    else:
        # Don't modify the pathOfImage
        return pathOfImage

def getAllEncodingsAndLocationsOnImg(imgPath, verbose=False):
    mapLocation2EncodingOfFaces = {}
    imgObj = face_recognition.load_image_file(imgPath)

    # -> Find face locations on the imgObj
    locationsOfFacesInImg = face_recognition.face_locations(imgObj)

    # -> Find the encodings of  found on the image
    for singleLocation in locationsOfFacesInImg:
        singleLocationAsList = [singleLocation]
        mapLocation2EncodingOfFaces[singleLocation] = face_recognition.face_encodings(imgObj,known_face_locations=singleLocationAsList)[0]
        
        if verbose:
            print("Location {} : Checksum of encodings {}".format(singleLocation, len(mapLocation2EncodingOfFaces[singleLocation])))

    return mapLocation2EncodingOfFaces

def printMatchingFacesAndShowImg(facesMatched, imagePIL, pathOfImage):
    if len(facesMatched) == 0:
        print("No known faces found on this image.\n")
    else:
        for i in facesMatched:
            print("--> Face of {} found!\n".format(i))
        imagePIL.show(title=pathOfImage)

def createDrawAndImageObjects(pathToImg):
    originalImage = face_recognition.load_image_file(pathToImg)

    # Convert image to a PIL-format image so that we can draw on top of it
    imagePIL = Image.fromarray(originalImage)

    # Create Pillow ImageDraw Draw instance to draw with it
    drawPIL = ImageDraw.Draw(imagePIL)

    return imagePIL, drawPIL

def drawBoundingBoxAndNameonImg(name, drawPIL, location):
    top, right, bottom, left = location

    # Draw a box around the face using the Pillow module
    drawPIL.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    # Draw a label with a name below the face
    text_width, text_height = drawPIL.textsize(name)
    drawPIL.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
    drawPIL.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

def lookForKnownPeopleInImg(takeNewPic = True, pathOfImage = "", verbose = False):
    """
        Function Name:
            lookForKnownPeople
        Objective:
            Take a pic & look for known people.
        Input parameter(s):
            - verbose : boolean to print or not information
            - takeNewPic : boolean to take or no a new picture
        Output parameter(s):
            * None
    """ 
    facesMatched = []

    # -> Take a new pic and save it in default location
    pathOfImage = getPathOfImgToLookOn(takeNewPic, pathOfImage)

    # -> Create Pil & Draw objects to mark the rectangles
    imagePIL, drawPIL = createDrawAndImageObjects(pathOfImage)

    # -> Get map location:enconding of each face on the image
    mapLocation2EncodingOfFaces = getAllEncodingsAndLocationsOnImg(pathOfImage)

    # -> Iterate over map and look for mathces
    for tLocation, tEncoding in mapLocation2EncodingOfFaces.items():
        matchingName = isUnknownAKnownFace(tEncoding)

        # -> If match found, append it to the list of matches
        if matchingName != None:
            facesMatched.append(matchingName)
            
            # -> Draw a bounding box on the image
            drawBoundingBoxAndNameonImg(matchingName, drawPIL, tLocation)
    
    # -> Print the matching names
    if verbose:
        printMatchingFacesAndShowImg(facesMatched, imagePIL, pathOfImage)

    # -> Remove the drawing library from memory as per the Pillow docs
    del drawPIL

    return facesMatched

def lookForKnownPeopleInFiles(listOfFiles, directoryPath, verbose=False):
    foundImages = 0

    for currentFile in listOfFiles:
        # If file is an image, look for knownPeople
        if isFileAnImg(currentFile):
            foundImages += 1

            path2Img = createPathToAFile(directoryPath,currentFile)
            path2resizedImg = createPathToAFile(directoryPath, buildResizeImgName(originalFilename=currentFile))

            if verbose:
                print("\n==============================================")
                print("Looking for known faces in ==> " + str(currentFile) + "...")

            facesMatched = lookForKnownPeopleInImg(takeNewPic=False, pathOfImage=path2resizedImg, verbose=True)
            theDB.updateRuntimePaths(facesMatched, path=path2Img)

            # Clear the list after analisis on a picture
            facesMatched.clear()

    return foundImages

def lookForKnownPeopleInDir(verbose = False):
    """
        Function Name:
            lookForKnownPeopleInDir
        Objective:
            Look in various images inside a specified directory (path) for known people.
        Input parameter(s):
            - path : string that contains the path which contains the imgs to analyze
        Output parameter(s):
            * None
    """

    # -> Ask for a path
    directoryPath = askForDirPath()

    # -> Retrieve elements in directoryPath as a list
    filesInPath = getFilesFromDir(directoryPath)

    # -> TODO Implement try/catch to delete the duplicates if there is an error
    # -> Resize the images to a reasonable WIDTH x HEIGHT
    resizeImgsInDir(filesInPath)

    if verbose:
        print("***** Images in ==> {} *****\n".format(directoryPath))
    
    # -> Look for known people in the images of the current directoryPath
    foundImages = lookForKnownPeopleInFiles(filesInPath, directoryPath, verbose=True)

    if verbose:
        print("\n***** " + str(foundImages) + " IMAGES were analyzed. *****\n")
        print("\n==== The path {} was analyzed successfuly =====\n".format(directoryPath))

    # -> Delete resized images, because they are duplicates
    deleteResizedImages(directoryPath)

# ============================================================================ #

# ========================== PYREBASE & DB FUNCTIONS ========================= #
# TODO Clean this function
def registerNewPerson(newName, takeNewPic = 'Y'):
    """
        Function Name:
            registerNewPerson
        Objective:
            Register a new person on the DB (known_People.json) with its corresponding face encoding.
        Input parameter(s):
            - newName : name of person to register
        Output parameter(s):

    """
    global defaultLocation

    # 0) Print starting of the function
    print(" ===== Registering a new person ... ===== \n")

    # 1) Take a picture and store it in locally ("./temp.jpg")
    if takeNewPic == 'Y':
        takePic(showImage=False)
        pathToImg = "./temp.jpg"
    else:
        pathToImg = input("\nEnter the path to the image with the new face... \n")


    # 2) Call learn on new face to store {newName : faceEncoding} 
    successStatus = learnOnNewFace(pathToImg, newName)

    # 3) Print output status
    if successStatus == 0:
        print("\n ====={} was successfuly added to the DB ===== \n".format(newName))
    elif successStatus == -1:
        print("\n ==== {} WAS NOT added. Zero or multiple faces found on img. ==== \n".format(newName))
    elif successStatus == 1:
        print("\n ===== Face from {} already registered! ===== \n".format(newName))

# TODO Clean this function
def registerPeopleFromDir():
    """
        Function Name:
            registerPeopleFromDir
        Objective:
            Ask the user for a directory with images named after the format
            FirstName_LastName.jpg and register them to the Firebase DB. The
            file that is going to be analyzed is the RESIZED one.
        Input parameter(s):
            * None
        Output parameter(s):
            * None

    """
    directoryPath = askForDirPath()

    filesInDirectoryPath = getFilesFromDir(directoryPath)
    
    resizeImgsInDir(filesInDirectoryPath)

    for currentFile in filesInDirectoryPath:
        if isFileAnImg(currentFile):
            # 1) Get the name of the person from the file name, e.g. FirstName_LastName.jpg
            newName = getNameOfPerson(currentFile)

            # 2) Call learnOnNewFace function on RESIZED image to store face encodings in DB
            currentFileResized = buildResizeImgName(originalFilename=currentFile)
            pathToImg = os.path.join(directoryPath, currentFileResized)
            successStatus = learnOnNewFace(pathToImg, newName)

            # 3) Print output status
            if successStatus == 0:
                print("{} was successfuly added to the DB \n".format(newName))
            elif successStatus != 0:
                print("{} WAS NOT added due to an error :( \n".format(newName))

    # --> Delete resized duplicates    
    deleteResizedImages(directoryPath)

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

    def setPaths(self, newListOfPaths):
        self.pathsToImgs = newListOfPaths

    def addPath(self, newPath):
        # Make sure that newPath hasn't been added previously
        if newPath not in self.pathsToImgs:
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
        data = {"encodings" : faceEncodings}
        self.dbHandle.child("People").child(name).set(data)
        
    def printRegisteredPeople(self):
        for k, v in self.registeredPeople.items():
            print("{} ==> {}...".format(k,v.getEncodings()[0:3]))

            thePaths = v.getPaths()
            for tPath in thePaths:
                print("\t- {}".format(tPath))

            print("\n")

    def getReferenceToPerson(self, tName):
        return self.dbHandle.child("People").child(tName)

    def updatePaths(self):
        update = input("\n ===== Update the paths in Firebase Database? [Y/n] ==== \n")

        if update == "Y" or update == "y":
            for name, tObj in self.registeredPeople.items():

                personToUpdatePaths = self.getReferenceToPerson(name)
                personToUpdatePaths.update({"pathsToImgs" : tObj.getPaths()})

    def updateRuntimePaths(self, facesMatched, path):
        for nameOfFace in facesMatched:
            self.registeredPeople[nameOfFace].addPath(path)

    def clearAllPathsToImgs(self):
        for name, tObj in self.registeredPeople.items():
            emptyList = []
            tObj.setPaths(emptyList)

            # personToUpdatePaths = self.getReferenceToPerson(name)

            # personToUpdatePaths.update({"pathsToImgs" : []})

    def updateEncoding(self, name, encoding):
        self.dbHandle.child("People").child(name).update({"other" : encoding})

    def getValues(self):
        return self.registeredPeople.values()

    def getKeys(self):
        return self.registeredPeople.keys()

    def removePerson(self, nameToRemove):
        # Remove from firebase
        self.dbHandle.child("People").child(nameToRemove).remove()
        # Remove from Runtime DB
        try:
            self.registeredPeople.pop(nameToRemove)
            print("\n{} was succesfully removed.\n".format(nameToRemove))
        except:
            print("\n{} wasn't previously registered. No action performed.\n".format(nameToRemove))

    def removeAllPeople(self):
        # Get all names
        allNames = self.getKeys()

        # Convert form dict_keys to a normal python list
        allNamesAsList = [name for name in allNames]

        # Loop over this list and call removePerson func for each element
        for name in allNamesAsList:
            self.removePerson(name)


# TODO Try/Catch this initialization
# ===== Initialization of the RuntimeDB, ONLY when called as a secondary script ... ===== #
if __name__ != "__main__":
    theDB = RuntimeDB(config)
    theDB.loadData()
# ============================================================================ #

# ============================= OPENCV FUNCTIONS ============================= #
def takePic(pathToSavePic = "./temp.jpg", showImage = False, deviceNum = 0):
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
    
    try:
        cap = cv2.VideoCapture(deviceNum)
       
        time.sleep(0.5) # Prevents the image to be dark
        _, frame = cap.read()
        cv2.imwrite(pathToSavePic, frame)

        if showImage:
            cv2.imshow("New Picture", frame)
            cv2.waitKey(0)
        
        cap.release()
        cv2.destroyAllWindows()
    except:
        pass

def computeNewDimensions(imgCV2Obj, stdWidth, stdHeight):
    # Get imgCV2Obj Width and Height
    origWidth, origHeight = imgCV2Obj.shape[:2]

    # Divide the original dimensions by the standard ones to get the scales
    widthScale = origWidth / stdWidth
    heightScale = origHeight / stdHeight

    # Return the new SCALED dimensions
    newWidht = int(origWidth / widthScale)
    newHeight = int(origHeight / heightScale)
    return newWidht, newHeight

def resizePic(originalImageName = "temp.jpg", stdWidth = 720, stdHeight = 480, verbose=False):
    """
        TODO
        Function Name:
        Objective:
        Input parameter(s):
        Output parameter(s):

    """
    originalImage = cv2.imread(originalImageName)

    # -> Compute newWidth and newHeight using the parameters stdWidth and stdHeight
    newWidth, newHeight = computeNewDimensions(originalImage, stdWidth, stdHeight)

    # -> Resize img, create resized name and save it 
    resizedImage = cv2.resize(originalImage,(newWidth, newHeight), interpolation = cv2.INTER_CUBIC)
    resizedImageName = buildResizeImgName(originalImageName)
    cv2.imwrite(resizedImageName, resizedImage)

    if verbose:
        print("\n==========")
        print("Creating {} ...".format(resizedImageName))
        print("==========\n")

def resizeImgsInDir(filesInPath):
    """
        Function Name:
            resizeImgsInDir
        Objective:
            Resize all imgs on a given directory.
        Input parameter(s):
            - directoryPath : 
        Output parameter(s):
            * None
    """
    # -> Execute the resizePic function on each img file of the list filesInPath
    for currentFile in filesInPath:
        if isFileAnImg(currentFile):
            resizePic(originalImageName=currentFile, verbose=True)

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
    imageTypes = ('.jpg','.png','.jpeg','.JPG')
    for e in imageTypes:
        if fileName.endswith(e):
            return True
    return False

def getNameOfPerson(fileName):
    nameOfPerson = ""
    for char in fileName:
        if char == '.':
            return nameOfPerson
        elif char == '_':
            nameOfPerson += ' '
        elif isALetter(char):
            nameOfPerson += char

def askForDirPath():
    """
        Function Name:
        askForDirPath
        Objective:
        Input parameter(s):
        Output parameter(s):

    """
    directoryPath = ""
    while not os.path.exists(directoryPath):
        directoryPath = input("\nEnter the directory where the pictures are located: ")

    return directoryPath

def getFilesFromDir(dir):
    """
        Function Name:
            getFilesFromDir
        Objective:
            Get files from a given directory
        Input parameter(s):
            - dir : Path to a directory.
        Output parameter(s):
            - filesInDir : All files of the directory stored in a LIST.

    """
    # -> Change location to dir (cd dir)
    os.chdir(dir)
    
    # -> List all files from dir (ls ./)
    filesInDir = os.listdir()

    return filesInDir

def isALetter(c): 
    return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')

def deleteResizedImages(dir="."):
    os.chdir(dir)
    os.system("rm *_RESIZED*")

def buildResizeImgName(originalFilename, sufix="_RESIZED"):
    dotIndex = originalFilename.find('.')

    imageName = originalFilename[:dotIndex]
    typeOfImgFile = originalFilename[dotIndex:]

    resizeImgName = imageName + sufix + typeOfImgFile
    
    return resizeImgName

def createPathToAFile(basePath, fileName):
    return os.path.join(basePath, fileName)

# ============================================================================ #

    """
    TODO
    Function Name:
        
    Objective:

    Input parameter(s):

    Output parameter(s):
    """

if __name__ == "__main__":

    # ===== Test for loading data from Firebase DB =====
    # theDB = RuntimeDB(config)
    # theDB.loadData()
    # theDB.printRegisteredPeople()

    # ===== Other Tests =====
    # t = askForDirPath()
    # print(getFilesFromDir(t))

    # ===== Take Pic Test =====
    # takePic(showImage=True, deviceNum=0) 

    # ===== Resize Image Test =====
    resizePic(verbose=True)

    # ===== Resize ALL Images on a Directory, wait 3 seconds & delete the resized images =====
    # tFiles = getFilesFromDir(dir="/home/sebasrivera96/Desktop/FaceRevognitionTest_1")
    # resizeImgsInDir(tFiles)
    # time.sleep(3)
    # deleteResizedImages(dir="/home/sebasrivera96/Desktop/FaceRevognitionTest_1")

    # ===== Draw a bounding box and name on img =====
    # name = "Vicente Guerrero"

    # imgObj = face_recognition.load_image_file("temp.jpg")
    # pil_image, draw = createDrawAndImageObjects("temp.jpg")

    # location = face_recognition.face_locations(imgObj)[0]
    # drawBoundingBoxAndNameonImg(name, draw, location)
    # pil_image.show()

    # ===== Get all locations & encodings of faces on an img =====
    # getAllEncodingsAndLocationsOnImg("temp.jpg", verbose=True)

    pass