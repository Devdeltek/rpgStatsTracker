import os
import pickle
import character
import command
import shutil

#Fix sessionNUmber incrementation

class game():
    #list of characters, session number, name
    #todo
    #if character folder/files are not found, delete from list
    #add information for tkinter window
    #have little from and boil write in notebook when a stat is logged, like a loading wheel
    def __init__(self, name, sessionNum = 0):
        #game information
        self.name = name
        self.sessionNum = 0

        #character information
        self.activeCharacters = []
        self.currCharacterNames = []
        self.oldCharacterNames = []

        #command pattern stuff
        self._history_pivot = -1
        self._command_list = []
        self._command_history = []

        #creates a folder for the game information to be saved
        self.directory = "./games/{}".format(self.name)
        os.makedirs(self.directory)

    #adds a character to the game
    def addCharacter(self, charName, playerName, color="#FFFFFF", totDamDone = 0, totDamTaken = 0, totKills = 0, totDeaths = 0, totHeal = 0, totHits = 0, totMisses = 0, totBruhMoments = 0):
        #check if character already exists
        PC = character.characters(self.directory, charName, playerName, color, totDamDone, totDamTaken, totKills, totDeaths, totHeal, totHits, totMisses, totBruhMoments)
        self.activeCharacters.append(PC)
        self.currCharacterNames.append(charName)

    #Loads all current characters into active characters
    def startSession(self):
        self._command_list.clear()
        self._command_history.clear()
        self._history_pivot = -1

        self.sessionNum +=1

        for c in self.currCharacterNames:
            with open(self.directory + "/{}/{}.bin".format(c, c), "rb") as f:
                self.activeCharacters.append(pickle.load(f))

        for c in self.activeCharacters:
            c.startSession()


    #Pickles all active characters and clears the active character list
    def endSession(self):
        self._command_list.clear()
        self._command_history.clear()
        self._history_pivot = -1

        for c in self.activeCharacters:
            c.endSession(self.sessionNum)
            with open(c.directory + '/' + c.charName + ".bin", "wb") as f:
                pickle.dump(c, f)

        self.activeCharacters.clear()

        #cancels the session
    def cancelSession(self):
        self._command_list.clear()
        self._command_history.clear()
        self._history_pivot = -1
        self.sessionNum -= 1

        for c in self.activeCharacters:
            c.cancelSession()
            with open(c.directory + '/' + c.charName + ".bin", "wb") as f:
                pickle.dump(c, f)

        self.activeCharacters.clear()

    def getStats(self):
        allCharacters = []
        for c in self.currCharacterNames:
            with open(self.directory + "/{}/{}.bin".format(c, c), "rb") as f:
                allCharacters.append(pickle.load(f))

        for c in self.oldCharacterNames:
            with open(self.directory + "/{}/{}.bin".format(c, c), "rb") as f:
                allCharacters.append(pickle.load(f))

        return allCharacters


    #Moves current character to old character incase a character dies
    def moveCharacterToOld(self, name):
        self.oldCharacterNames.append(name)
        self.currCharacterNames.remove(name)


    #Moves old character back to the current characters
    #Incase old character is revived
    def moveCharacterToCurrent(self, name):
        self.currCharacterNames.append(name)
        self.oldCharacterNames.remove(name)

        with open(self.directory + "/{}/{}.bin".format(name, name), "rb") as f:
            self.activeCharacters.append(pickle.load(f))
        self.activeCharacters[-1].startSession()

    #adds an old character to the active characters for this session so they can be updated/viewed in the report
    #incase old character comes back for one session
    def viewOldCharacter(self, name):
        with open(self.directory + "/{}/{}.bin".format(name, name), "rb") as f:
            self.activeCharacters.append(pickle.load(f))
        self.activeCharacters[-1].startSession()

    def deleteCharacter(self, name):
        self.oldCharacterNames.remove(name)
        for c in self.activeCharacters:
            if(c.charName == name):
                self.activeCharacters.remove(c)
        shutil.rmtree(self.directory + '/' + name)



    def newCommand(self, char, amount, stat):
        newCom = command.CharCommand(char, amount, stat)
        newCom.execute()

        self._history_pivot += 1

        if(self._history_pivot == len(self._command_list)):
            self._command_list.append(newCom)
            self._command_history.append(newCom.toString())
        else:
            self._command_list[self._history_pivot] = newCom
            self._command_history[self._history_pivot] = newCom.toString()

        return self._command_history

    def history(self):
        return self._command_history


    def undo(self):
        if(self._history_pivot >= 0):
            self. _command_list[self._history_pivot].unExecute()
            self._history_pivot -= 1
        return self._history_pivot

    def redo(self):
        if(self._history_pivot != len(self._command_list)-1):
            self._history_pivot += 1
            tempCom = self._command_list[self._history_pivot]
            self._command_list[self._history_pivot].execute()
        return self._history_pivot

    def removeCommandByIndex(self, spot):
        if(spot <= self._history_pivot):
            self._command_list[spot].unExecute()
            self._command_list.pop(spot)
            self._command_history.pop(spot)
            self._history_pivot -= 1
        elif(spot < len(self._command_list)):
            self._command_list.pop(spot)
            self._command_history.pop(spot)

        return self._history_pivot