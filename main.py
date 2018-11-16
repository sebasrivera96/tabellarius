# ================================= main.py ================================== #


from Face_Recognition_Functions import *
from OpenCV_Functions import *

def registerNewPerson(newName):
    """
        TODO
        Function Name:
            registerNewPerson
        Objective:
            Register a new person on the DB (known_People.json) with its corresponding face encoding.
        Input parameter(s):
            - newName : name of person to register
        Output parameter(s):

    """
    defaultLocation = "./temp.jpg"

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

"""
    TODO
    Function Name:
        lookForKnownPeople
    Objective:

    Input parameter(s):

    Output parameter(s):
"""

if __name__ == "__main__":
    loadKnownFaces("known_People.json")
    printKnownPeople()
    registerNewPerson("Sebastian Rivera")
    printKnownPeople()
    saveNewFaces()