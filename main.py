# ================================= main.py ================================== #


from Face_Recognition_Functions import *
from OpenCV_Functions import *

# ============================ GLOBAL VARAIBLES ============================== #
defaultLocation = "./Gareth&Cristiano.jpg"
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

def lookForKnownPeople(verbose = False):
    """
    TODO
    Function Name:
        lookForKnownPeople
    Objective:
        Take a pic & look for known people.
    Input parameter(s):
        - verbose : boolean to print or not information
    Output parameter(s):
        * None
    """ 
    global defaultLocation
    facesMatches = []

    # 1) Take a new pic and save it in default location
    # takePic(pathToSavePic=defaultLocation)
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

    return facesMatches

"""
    TODO
    Function Name:
        lookForKnownPeople
    Objective:
        Take a pic & look for known people within 
    Input parameter(s):

    Output parameter(s):
"""

if __name__ == "__main__":
    loadKnownFaces("known_People.json") # This function is essential to load previously generated data
    
    lookForKnownPeople(True)

    saveNewFaces()