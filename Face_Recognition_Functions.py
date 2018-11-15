import face_recognition
from PIL import Image
import sys
import os

# =========================== GLOBAL VARIABLES =============================== #
knownPeople = {} # Dictionary: {key = Name, value = encoding}

# ============================= MAIN FUNTIONS ================================ #
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
def facesOnImg(imgObj):
    # Use a built-in function from the library to detect faces
    faceLocations = face_recognition.face_locations(imgObj)
    return faceLocations

"""
TODO
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
TODO
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
def learnOnNewFace(imgPath, nameOfPerson):
    global knownPeople
    imgObj = face_recognition.load_image_file(imgPath)

    # 1) Find faces on the image
    faceLocation = facesOnImg(imgObj)

    # 2) If not 1, return -1 : else, keep going
    if len(faceLocation) != 1:
        return -1 # Error because when learning a new face there must be exactly one to prevent ambiguity

    # 3) Store the new encoding (value) related to nameOfPerson (key)
    newEncoding = face_recognition.face_encodings(imgObj, faceLocation)[0]
    knownPeople[nameOfPerson] = newEncoding

    # 4) Return a success state
    return 0


"""
TODO
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
# def loadKnownFaces(jsonPath):


"""
TODO
Function Name:
    saveNewFaces
Objective:

Input parameter(s):

Output parameter(s):

"""
# def saveNewFaces(facesDict):

"""
TODO
Function Name:
    
Objective:

Input parameter(s):

Output parameter(s):

"""

if __name__ == "__main__":
    imgPath = "Leo_Messi/1.jpg"
    imgPath_CR7 = "Cristiano_Ronaldo/1.jpg"
    imgPath_GB = "Gareth_Bale/1.jpg"

    print("Register Messi: ", learnOnNewFace(imgPath, "Leonel Messi"))
    print("Register Cristiano: ", learnOnNewFace(imgPath_CR7, "Cristiano Ronaldo"))
    print("Register Gareth: ", learnOnNewFace(imgPath_GB, "Gareth Bale"))

    for key, value in knownPeople.items():
        print(key, value, type(value))

    # imgObject = face_recognition.load_image_file(imgPath)
    # imgObj_CR7 = face_recognition.load_image_file(imgPath_CR7)
    # imgObj_GB = face_recognition.load_image_file(imgPath_GB)


    # faceEncoding = face_recognition.face_encodings(imgObject)[0]
    # faceEncoding_CR7 = face_recognition.face_encodings(imgObj_CR7)[0]
    # faceEncoding_GB = face_recognition.face_encodings(imgObj_GB)[0]

    # print("Leo and Leo")
    # print(face_recognition.compare_faces([faceEncoding_CR7], faceEncoding))
    # print("Leo and Cristiano")
    # print(face_recognition.compare_faces([faceEncoding_CR7], faceEncoding_CR7))
    # print("Leo and Gareth")
    # print(face_recognition.compare_faces([faceEncoding_CR7], faceEncoding_GB))



