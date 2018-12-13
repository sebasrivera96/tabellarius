import pyrebase

config = {
    "apiKey": "AIzaSyB0jgw-XexiMlBeyFVwUQKUSaRAd5WbDvg",
    "authDomain": "thefirstapp-80dcc.firebaseapp.com",
    "databaseURL": "https://thefirstapp-80dcc.firebaseio.com",
    "projectId": "thefirstapp-80dcc",
    "storageBucket": "thefirstapp-80dcc.appspot.com",
    "messagingSenderId": "601653648941"
}

firebase = pyrebase.initialize_app(config)

# DATABASE FUNCTIONS
db = firebase.database()
registeredPeople = db.child("People").get()

for person in registeredPeople.each():
    print(person.key())
    print(person.val()["pathsToImgs"])

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
    registeredPeople = {}

    # ===== METHODS ===== #
    def __init__(self):
        loadData()
    
    def addPerson(self, name, faceEncodings=[], paths=[]):
        raise NotImplementedError