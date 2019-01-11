# ================================= main.py ================================== #

# ================================ LIBRARIES ================================= #
from tabellariusFunctions import *
# ============================================================================ #

# ============================ GLOBAL VARAIBLES ============================== #
facesFilePath = "/home/sebasrivera96/Documents/Dev/tabellarius/namesFaces.txt"
# ============================================================================ #

def confirmAction(option):
    confirmation = input("\n === Are you sure you want to execute option {}? [Yes/No] ===\n".format(option))
    return (confirmation == "Yes")

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
        # print("\t- [A] ==> Take a picture and display it")
        # print("\t- [B] ==> Register a new person")
        print("\t- [C] ==> Register people from a directory")
        print("\t- [D] ==> Print the registered people")
        # print("\t- [E] ==> Take a picture and look for a known person")
        print("\t- [F] ==> Erase a person given his/her name")        
        print("\t- [G] ==> Look for known people in pictures of a given directory") 
        print("\t- [H] ==> Remove the paths to images of ALL the registered users")    
        print("\t- [I] ==> Remove ALL people registered")            
        print("\t- [exit] ==> Exit")

        option = input()

        if option == 'A':
            takePic(showImage=True)
        elif option == 'B':
            newName = input("Enter the complete name: ")
            
            newPic = ""
            while newPic != 'Y' and newPic != 'N':
                newPic = input("Take a new picture? [Y/N]? ")
                newPic = newPic.upper()

            registerNewPerson(newName, takeNewPic=newPic)
        elif option == 'C':
            registerPeopleFromDir()
        elif option == 'D':
            # printKnownPeople()
            theDB.printRegisteredPeople()
        elif option == 'E':
            newPic = ""
            while newPic != 'Y' and newPic != 'N':
                newPic = input("Take a new picture? [Y/N)]? ")
            if newPic == 'Y':
                lookForKnownPeople(verbose=True, takeNewPic=True)
            elif newPic == 'N':
                lookForKnownPeople(verbose=True, takeNewPic=False)
        elif option == 'F':
            eraseName = input("Enter the name to be erased: ")
            theDB.removePerson(eraseName)
        elif option == 'G':
            lookForKnownPeopleInDir()
        elif option == 'H':
            theDB.clearAllPathsToImgs()
        elif option == 'I':
            if confirmAction(option):
                theDB.removeAllPeople()
            else:
                print("\n ===== Operation {} was cancelled =====\n".format(option))
        elif option == 'exit':
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
