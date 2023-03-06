import os
import pickle
class game():
    #list of characters, session number, name
    #todo
    #if character folder/files are not found, delete from list
    #add information for tkinter window
    #have little from and boil write in notebook when a stat is logged, like a loading wheel
    def __init__(self, name, sessionNum = 0):
        #game information
        self.name = name
        self.sessionNum = num

        #character information
        self.activeCharacters = []
        self.currCharacterNames = []
        self.oldCharacterNames = []

        #command pattern stuff
        self._history_pivot = 0
        self._command_list = []

        #creates a folder for the game information to be saved
        self.directory = "./games/{}".format(self.name)
        os.mkdir(directory)

    #adds a character to the game
    def addCharacter(self, character):
        #check if character already exists
        self.activeCharacters[numActiveCharacters] = character
        self.currCharacterNames.append(character.charName)

    #Loads all current characters into active characters
    def startSession(self):
        _command_list.clear()
        _history_pivot = 0

        self.sessionNum = self.sessionNum + 1

        for c in currCharacterNames:
            with open(self.directory + "{}/{}.bin".format(c, c), "rb") as f:
                self.activeCharacters.append(pickle.load(f))

        for c in self.activeCharacter:
            c.startSession()


    #Pickles all active characters and clears the active character list
    def endSession():
        _command_list.clear()
        _history_pivot = 0

        for c in self.activeCharacters:
            c.endSession(self.sessionNum)
            with open(c.directory + c.charName + ".bin", "wb") as f:
                pickle.dump(c, f)

        self.activeCharacters.clear()

    #Moves current character to old character incase a character dies
    def moveCharacterToOld(self, name):
        self.oldCharacterNames.append(name)
        self.currCharacterNames.remove(name)


    #Moves old character back to the current characters
    #Incase old character is revived
    def moveCharacterToCurrent(self, name):
        self.currCharacterNames.append(name)
        self.oldCharacterNames.remove(name)

        with open(self.directory + "{}/{}.bin".format(name, name), "rb") as f:
            self.activeCharacters.append(pickle.load(f))
        activeCharacters[-1].startSession()

    #adds an old character to the active characters for this session so they can be updated/viewed in the report
    #incase old character comes back for one session
    def viewOldCharacter(self, name):
        with open(self.directory + "{}/{}.bin".format(name, name), "rb") as f:
            self.activeCharacters.append(pickle.load(f))
        activeCharacters[-1].startSession()

    def newCommand(self, command):
        command.execute()
        _command_list.append(command)
        _history_pivot += 1        

    def history(self):
        return _command_list

    def undo(self):
        if(_history_pivot != 0):
            _command_list[i].unExecute()
            _history_pivot -= 1

    def redo(self):
        if(_history_pivot != _command_list.size()-1):
            _command_list[_history_pivot].execute()
            _history_pivot += 1