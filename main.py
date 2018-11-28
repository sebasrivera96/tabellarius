# ================================= main.py ================================== #


from Face_Recognition_Functions import *
from OpenCV_Functions import *
from Directory_and_File_Functions import *
import sys


# ============================ GLOBAL VARAIBLES ============================== #
defaultLocation = "/home/sebasrivera96/Documents/Dev/tabellarius/temp.jpg"
facesFilePath = "/home/sebasrivera96/Documents/Dev/tabellarius/namesFaces.txt"
# ============================================================================ #

def registerNewPerson(newName):
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
    takePic(showImage=False)

    # 2) Call learn on new face to store {newName : faceEncoding} 
    successStatus = learnOnNewFace(defaultLocation, newName)

    # 3) Print output status
    if successStatus == 0:
        print("{} was successfuly added to the DB \n".format(newName))
    elif successStatus != 0:
        print("{} WAS NOT added due to an error :( \n".format(newName))

def lookForKnownPeople(verbose = False, takeNewPic = True):
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
    global defaultLocation
    facesMatches = []

    # 1) Take a new pic and save it in default location
    if takeNewPic:
        takePic(pathToSavePic=defaultLocation)
    imgObj = face_recognition.load_image_file(defaultLocation)

    # 2) Find the encoding(s) of the faces found on the image
    listOfEncodings = face_recognition.face_encodings(imgObj)

    # 3) Iterate over listOfEncodings and look for mathces
    for encoding in listOfEncodings:
        tMatch = isUnknownAKnownFace(encoding)
        if tMatch != "":
            facesMatches.append(tMatch)
    
    # 4) Print the matching names
    if verbose:
        for i in facesMatches:
            print("Face of {} found on this image {}.\n".format(i, defaultLocation[2:]))
        if facesMatches == 0:
            print("No known faces found on this image {}.\n".format(defaultLocation[2:]))
    return facesMatches

def lookForKnownPeopleInDir(path):
    """
    TODO
    Function Name:
        lookForKnownPeopleInDir
    Objective:
        Look in various images inside a specified directory (path) for known people.
    Input parameter(s):
        - path : string that contains the path which contains the imgs to analyze
    Output parameter(s):
        * None
    """

    # 1) Change directory to 'path', if valid
    successStatus = isPathValid(path)

    # 2) Print success status
    if successStatus:
        print("\n==== The path {} was analyzed successfuly =====\n".format(path))
    else:
        print("\n==== The path {} is not valid! =====\n".format(path))


def interactiveMenu():
    """
        Function Name:
            interactiveMenu
        Objective:
            As the name suggests, this function will display a menu for the user 
            to interact with the functionalities of tabellarius.
        Input parameter(s):
            * None
        Output parameter(s):
            * None
    """
    option = ''
    while option != 'e':
        print("Please type a CHARACTER to execute an action: \n")
        print("\t- [r] ==> Register a new person")
        print("\t- [p} ==> Print the registered people")
        print("\t- [l] ==> Take a picture and look for a known person")
        print("\t- [c] ==> Erase a person from the list of known people")        
        print("\t- [d] ==> Look for a known person in pictures inside a directory")        
        print("\t- [e] ==> Exit")

        option = input()

        if option == 'r':
            newName = input("Enter the name (First Last): ")
            registerNewPerson(newName)
        elif option == 'p':
            printKnownPeople()
        elif option == 'l':
            lookForKnownPeople(verbose=True, takeNewPic=True)
        elif option == 'c':
            eraseName = input("Enter the name to be erased: ")
            eraseFace(eraseName)
        elif option == 'd':
            directoryPath = input("Enter the directory where the pictures are located: ")
            lookForKnownPeopleInDir(directoryPath)
        elif option == 'e':
            print("Exiting ...")
        else:
            print("The character [" + option + "] is not a valid option in this menu.")

"""
    TODO
    Function Name:
        
    Objective:

    Input parameter(s):

    Output parameter(s):

"""

if __name__ == "__main__":
    loadKnownFaces(JSONPath) # This function is essential to load previously generated data
    
    # lookForKnownPeople(verbose=True, takeNewPic=True)
    if len(sys.argv) == 1:
        interactiveMenu()
    elif len(sys.argv) > 1:
        if sys.argv[1] == "learn":
            registerNewPerson(sys.argv[2])
        elif sys.argv[1] == "recognize":
            foundFaces = lookForKnownPeople(verbose=True, takeNewPic=True)
            file = open(facesFilePath, "w")
            for face in foundFaces:
                file.write(face+"\n")

    saveNewFaces()