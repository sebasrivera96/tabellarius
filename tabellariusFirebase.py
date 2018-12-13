import pyrebase

# ===== GLOBAL VARIABLES ===== #
config = {  "apiKey": "AIzaSyB0jgw-XexiMlBeyFVwUQKUSaRAd5WbDvg",
            "authDomain": "thefirstapp-80dcc.firebaseapp.com",
            "databaseURL": "https://thefirstapp-80dcc.firebaseio.com",
            "projectId": "thefirstapp-80dcc",
            "storageBucket": "thefirstapp-80dcc.appspot.com",
            "messagingSenderId": "601653648941"}

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
        newPerson = TabellariusPerson(name, faceEncodings, paths)
        self.registeredPeople[name] = newPerson

    def createPerson(self,)
        """
        This person is completly new and must be added to the firebaseDB
        """
        raise NotImplementedError

    def printRegisteredPeople(self):
        for k, v in self.registeredPeople.items():
            print("{} ==> {}, {}".format(k,v.getEncodings(), v.getPaths()))
        

if __name__ == "__main__":

    