# ================================= main.py ================================== #

# ================================ LIBRARIES ================================= #
from tabellariusFunctions import *
# ============================================================================ #

# ============================ GLOBAL VARAIBLES ============================== #
facesFilePath = "/home/sebasrivera96/Documents/Dev/tabellarius/namesFaces.txt"
# ============================================================================ #

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
        print("\t- [s] ==> Register people from a directory")
        print("\t- [p} ==> Print the registered people")
        print("\t- [l] ==> Take a picture and look for a known person")
        print("\t- [c] ==> Erase a person from the list of known people")        
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
                newPic = newPic.upper()

            registerNewPerson(newName, takeNewPic=newPic)
        elif option == 's':
            registerPeopleFromDir()
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
        elif option == 'c':
            eraseName = input("Enter the name to be erased: ")
            theDB.removePerson(eraseName)
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
    # if more arguments are given, execute a different action
    elif len(sys.argv) > 1:
        pass

    theDB.updatePaths()
