import os
import pickle
class game():
    #list of characters, session number, name
    #todo
    #if character folder/files are not found, delete from list
    #add information for tkinter window
    #have little from and boil write in notebook when a stat is logged, like a loading wheel
    def __init__(self, name, sessionNum = 0):
        self.name = name
        self.sessionNum = num
        self.activeCharacters = []
        self.currCharacterNames = []
        self.oldCharacterNames = []

        self.directory = "./games/{}".format(self.name)
        os.mkdir(directory)



    def addCharacter(self, character):
        #check if character already exists
        self.activeCharacters[numActiveCharacters] = character
        self.currCharacterNames.append(character.charName)

    def startSession(self):
        self.sessionNum = self.sessionNum + 1

        for c in currCharacterNames:
            with open(self.directory + "{}/{}.bin".format(c, c), "rb") as f:
                self.activeCharacters.append(pickle.load(f))

        for c in self.activeCharacter:
            c.startSession()


    def endSession():
        #run all command things for each character
        for c in self.activeCharacters:
            c.endSession(self.sessionNum)
            with open(c.directory + c.charName + ".bin", "wb") as f:
                pickle.dump(c, f)

        self.activeCharacters.clear()


    def moveCharacterToOld(self, name):
        self.oldCharacterNames.append(name)
        self.currCharacterNames.remove(name)


    def moveCharacterToCurrent(self, name):
        self.currCharacterNames.append(name)
        self.oldCharacterNames.remove(name)

        with open(self.directory + "{}/{}.bin".format(name, name), "rb") as f:
            self.activeCharacters.append(pickle.load(f))
        activeCharacters[-1].startSession()

    def viewOldCharacter(self, character):
        with open(self.directory + "{}/{}.bin".format(name, name), "rb") as f:
            self.activeCharacters.append(pickle.load(f))
        activeCharacters[-1].startSession()