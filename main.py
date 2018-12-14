# ================================= main.py ================================== #

# ================================ LIBRARIES ================================= #
from tabellariusFunctions import *
# ============================================================================ #

# ============================ GLOBAL VARAIBLES ============================== #
defaultLocation = "./Mony&Sebas_1.jpeg"
facesFilePath = "/home/sebasrivera96/Documents/Dev/tabellarius/namesFaces.txt"
# ============================================================================ #

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
    pathToImg = defaultLocation

    # 1) Take a picture and store it in locally ("./temp.jpg")
    if takeNewPic == 'Y':
        takePic(showImage=False)
        pathToImg = "./temp.jpg"


    # 2) Call learn on new face to store {newName : faceEncoding} 
    successStatus = learnOnNewFace(pathToImg, newName)

    # 3) Print output status
    if successStatus == 0:
        print("{} was successfuly added to the DB \n".format(newName))
    elif successStatus != 0:
        print("{} WAS NOT added due to an error :( \n".format(newName))

def lookForKnownPeople(verbose = False, takeNewPic = True, pathOfImage = ""):
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
        pathOfImage = "./temp.jpg"
        takePic(pathToSavePic=pathOfImage)
    else:
        # Don't modify the pathOfImage
        pass

    imgObj = face_recognition.load_image_file(pathOfImage)

    # 2) Find the encoding(s) of the faces found on the image
    listOfEncodings = face_recognition.face_encodings(imgObj)

    # 3) Iterate over listOfEncodings and look for mathces
    for encoding in listOfEncodings:
        tMatch = isUnknownAKnownFace(encoding)
        if tMatch != "":
            facesMatches.append(tMatch)
    
    # 4) Print the matching names
    if verbose:
        if len(facesMatches) == 0:
            print("No known faces found on this image {}.\n".format(defaultLocation[2:]))
        else:
            for i in facesMatches:
                print("--> Face of {} found!\n".format(i))
    return facesMatches

def lookForKnownPeopleInDir():
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
    # --> Ask for a path. chdir to 'path', if valid
    directoryPath = ""
    while not os.path.exists(directoryPath):
        directoryPath = input("\nEnter the directory where the pictures are located: ")

    # -->
    os.chdir(directoryPath)
    filesInPath = os.listdir()
    foundImages = 0

    print("***** Images in ==> {} *****\n".format(directoryPath))
    for currentFile in filesInPath:
        # If file is an image, look for knownPeople
        if isFileAnImg(currentFile):
            foundImages += 1
            path2img = os.path.join(directoryPath,currentFile)
            print("\n==============================================")
            print("Looking for known faces in ==> " + str(currentFile) + "...")
            facesMatched = lookForKnownPeople(verbose=True, takeNewPic=False, pathOfImage=path2img)
            theDB.updateRuntimePaths(facesMatched, path=path2img)
    print("***** " + str(foundImages) + " IMAGES were analyzed. *****")

    # --> Print success status
    print("\n==== The path {} was analyzed successfuly =====\n".format(directoryPath))

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
    global theDB
    option = ''
    while option != 'e':
        print("Please type a CHARACTER to execute an action: \n")
        print("\t- [a] ==> Take a picture and display it")
        print("\t- [r] ==> Register a new person")
        print("\t- [p} ==> Print the registered people")
        print("\t- [l] ==> Take a picture and look for a known person")
        # print("\t- [c] ==> Erase a person from the list of known people")        
        print("\t- [d] ==> Look for known people in pictures of a given directory")        
        print("\t- [e] ==> Exit")

        option = input()

        if option == 'a':
            takePic(showImage=True)
        elif option == 'r':
            newName = input("Enter the complete name: ")
            
            newPic = ""
            while newPic != 'Y' and newPic != 'N':
                newPic = input("Take a new picture? [Y/N]? ")

            registerNewPerson(newName, takeNewPic=newPic)
        elif option == 'p':
            # printKnownPeople()
            theDB.printRegisteredPeople()
        elif option == 'l':
            newPic = ""
            while newPic != 'Y' and newPic != 'N':
                newPic = input("Take a new picture? [Y/N)]? ")
            if newPic == 'Y':
                lookForKnownPeople(verbose=True, takeNewPic=True)
            elif newPic == 'N':
                lookForKnownPeople(verbose=True, takeNewPic=False)
        # TODO update this function to the FirebaseDB
        # elif option == 'c':
        #     eraseName = input("Enter the name to be erased: ")
        #     eraseFace(eraseName)
        elif option == 'd':
            lookForKnownPeopleInDir()
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

    theDB.updatePaths()
