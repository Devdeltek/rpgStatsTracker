import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import game
import pickle
import os
import shutil
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

#store a list of game names as a pickle
#add view window, can be seperate tab or opened in a new window, should be able to view current session and totals in real time for active characters, or past session for all characters who are relevant
#can toggle between which characters are shown in the graphs, current session - active characters, total - all characters, previous session - all charactes present in that session based on csv files
#add drop down to rename characters
#end session takes back to main menu, make sure clicking x will call end session stuff
#each game should have a pickle

#on start up unpickle the list of game names, open a main menu with a drop down to select a game based on the game name list. When a game name is selected the program
#will  open a pickle./games/{gameName}/{gameName}.bin to load the game information. start session will be called on that game and user will be moved to a game screen with tabs for
#each character and a tab for real time graphs. Drop down menus will allow for things like changing character names, changing session number, ect. There will be an input field
#for stats that increase by more than 1, a button for each stat that increases by one, and a list to the right of all the current commands so you can undo easier. End the session
#by either pressing x or an end session button, when session is ended the view page will be opened in its own window to show session stats and total stats, then when that is closed program will end


#Figure out where the scope of the gamelist and the current game being played should be

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        #initializes tkinter window
        tk.Tk.__init__(self, *args, **kwargs)

        #calls the endProgram function on close to pickle the game list
        self.protocol("WM_DELETE_WINDOW", self.endProgram)


        #list of the names of all games
        self.gamelist = []

        #if a pickle of the list exists, read it in
        if(os.path.isfile('./gamelist.bin')):
            with open('./gamelist.bin', "rb") as f:
                self.gamelist = pickle.load(f)

        #Sets attributes for the window
        self.title("Alchemist Frum Craftkins Post Battle Summary")
        self.geometry("800x600")
        self.resizable(width=True, height=True)
        self.wm_attributes('-transparentcolor', '#ab23ff')

        #makes a font, needed for the frames
        self.title_font = tkfont.Font(family='Arial', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, GameMenu, StatsMenu):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        #Show the main menu frame
        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    #pickles the game list to store all games
    def endProgram(self):
        with open("./gamelist.bin", "wb") as f:
                pickle.dump(self.gamelist, f)
        self.destroy()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #sets background color
        self.config(bg="DarkOliveGreen2")

        #makes a drop down menu for all games saved
        self.firstOption = tk.StringVar(value="No Games")
        self.gameOptions = tk.OptionMenu(self, self.firstOption, "No Games", *self.controller.gamelist)
        self.gameOptions.place(relx=0.1, rely=0.5)

        #if gamelist is already populated fill in gameoptions with existing games
        if self.controller.gamelist:
            self.firstOption.set('Choose')

            self.gameOptions['menu'].delete(0, 'end')

            for i in self.controller.gamelist:
                self.gameOptions['menu'].add_command(label=i, command=tk._setit(self.firstOption, i))

        
        #loads the buttons and label
        loadButton = tk.Button(self, height=5, width=30, text="Load Game", command=lambda: self.on_load(self.firstOption.get()))
        deleteButton = tk.Button(self, height=2, width=10, text="Delete Game", command=lambda: self.on_delete(self.firstOption.get()))
        newButton = tk.Button(self, height=5, width=30, text="New Game", command=self.on_new_game)
        statButton = tk.Button(self, height=5, width=30, text="View Stats", command=lambda: self.on_stat(self.firstOption.get()))
        quitButton = tk.Button(self, height=5, width=30, text="Quit", command=self.on_quit)

        menu_label = tk.Label(self, text="Post Battle Summary", font=("TkDefaultFont", 64), bg="#ab23ff")

        loadButton.place(relx = 0.1, rely = 0.6)
        deleteButton.place(relx = 0.6, rely = 0.5)
        newButton.place(relx = 0.1, rely = 0.8)
        statButton.place(relx = 0.6, rely = 0.6)
        quitButton.place(relx = 0.6, rely = 0.8)
        menu_label.place(relx=.5, rely=.25,anchor=tk.CENTER)

    #Load game button function
    def on_load(self, gameName):
        temp = None
        if gameName in self.controller.gamelist:
            with open( "./games/{}/{}.bin".format(gameName, gameName), "rb") as f:
                temp = pickle.load(f)

            self.controller.frames['GameMenu'].set_game(temp)
            self.controller.show_frame("GameMenu")

    def on_delete(self, gameName):
        temp = None
        if(gameName in self.controller.gamelist):
            shutil.rmtree("./games/" + gameName)
            self.controller.gamelist.remove(gameName)

            self.gameOptions['menu'].delete(0, 'end')

            for i in self.controller.gamelist:
                self.gameOptions['menu'].add_command(label=i, command=tk._setit(self.firstOption, i))

        

    #new game button function
    def on_new_game(self):
        #make new window for the popup
        top= tk.Toplevel(self.controller)
        top.geometry("300x150")
        top.title("Add Game")

        #add widgets
        tk.Label(top, text= "Create New Game", font=('Mistral 18 bold')).place(x=20,y=10)
        tk.Label(top, text= "Enter a Unique Name", font=('Mistral 10')).place(x=150,y=50)
        nameEntry = tk.Entry(top)
        nameEntry.place(x=20, y=50)
        nameEntry.focus_set()
        createButton = tk.Button(top, height=2, width=10, text="Create Game", command=lambda: self.on_create_game(nameEntry.get(), top))
        createButton.place(x=100, y=100)


    #Create the game object and pickle it in the right location, add the game name to the gamelist, destroy the child menu
    def on_create_game(self, name, popWin):
        warning = tk.Label(popWin, text= "", font=('Mistral 12 bold'))
        warning.place(x=100,y=80)

        #check if a string was entered and if the string already exists in the gamelist
        if name == "":
            warning.config(text = "Enter a valid string")
        elif name in self.controller.gamelist:
            warning.config(text="Game already exists")
        else:
            #adds the game to the game list and updates the drop down menu
            self.controller.gamelist.append(name)
            self.firstOption.set('Choose')

            self.gameOptions['menu'].delete(0, 'end')

            temp = game.game(name)
            temp.endSession()

            with open("{}/{}.bin".format(temp.directory, temp.name), "wb") as f:
                pickle.dump(temp, f)

            for i in self.controller.gamelist:
                self.gameOptions['menu'].add_command(label=i, command=tk._setit(self.firstOption, i))

            popWin.destroy()


    #stat button function
    def on_stat(self, gameName):
        temp = None
        if gameName in self.controller.gamelist:
            with open( "./games/{}/{}.bin".format(gameName, gameName), "rb") as f:
                temp = pickle.load(f)

            self.controller.frames['StatsMenu'].set_game(temp)
            self.controller.show_frame("StatsMenu")

    #quit button function
    def on_quit(self):
        self.controller.endProgram()


#Add old/current character stuff

#switch between characters with buttons at the top or right click menu, add colors to characters
class GameMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.listOfCommands = []
        
        self.game = None
        self.charButtons = []
        self.currCharacter = None
        self.stats = tk.StringVar(value="here")
        self.title = tk.StringVar(value="Empty Game, should not be here")
        self.command_pivot = -1

        self.valueEntry = tk.Entry(self)
        self.valueEntry.place(relx=.1, rely=.2)

        self.removeEntry = tk.Entry(self)
        self.removeEntry.place(relx=.6, rely=.75)

        removeCommand = tk.Button(self, height=1, width=15, text="Remove Command", command=lambda: self.on_remove_command(self.removeEntry.get()))

        self.commandLabel = tk.Text(self)
        self.commandLabel.place(relx=.6, rely = .1)

        displayTots = tk.Label(self, textvariable=self.stats)
        displayTots.place(relx=.1, rely=.5)

        label = tk.Label(self, textvariable=self.title, font=controller.title_font)
        label.place(relx = .5, rely = .15, anchor=tk.CENTER)

        notice = tk.Label(self, text="ctrl-z to undo, ctrl-y to redo. Undone commands marked with X")
        notice.place(relx = .7, rely = .82, anchor=tk.CENTER)

        notice2 = tk.Label(self, text="Only exit with cancel/end session buttons for this screne")
        notice2.place(relx = .8, rely = .07, anchor=tk.CENTER)

        button = tk.Button(self, height=2, width=10, text="End Session", command=self.on_main)
        button.place(relx=.85, rely=.85)

        cancelButton = tk.Button(self, height=2, width=10, text="Cancel Session", command=self.on_cancel_session)
        cancelButton.place(relx=.10, rely=.85)

        #totDamDone = 0, totDamTaken = 0, totKills = 0, totDeaths = 0, totHeal = 0, totHits = 0, totMisses = 0, totBruhMoments = 0
        addDamDone = tk.Button(self, height=2, width=10, text="Damage Done", command=lambda: self.on_increase(self.currCharacter, self.valueEntry.get(), "damDone"))
        addDamTaken = tk.Button(self, height=2, width=10, text="Damage Taken", command=lambda: self.on_increase(self.currCharacter, self.valueEntry.get(), "damTaken"))
        addDamHealed = tk.Button(self, height=2, width=10, text="Damage Healed", command=lambda: self.on_increase(self.currCharacter, self.valueEntry.get(), "damHealed"))

        addKill = tk.Button(self, height=2, width=10, text="Log Kill", command=lambda: self.on_increase(self.currCharacter, 1, "kills"))
        addDeath = tk.Button(self, height=2, width=10, text="Log Death", command=lambda: self.on_increase(self.currCharacter, 1, "deaths"))
        addHits = tk.Button(self, height=2, width=10, text="Log Hit", command=lambda: self.on_increase(self.currCharacter, 1, "hits"))
        addMiss = tk.Button(self, height=2, width=10, text="Log Miss", command=lambda: self.on_increase(self.currCharacter, 1, "misses"))
        addBruh = tk.Button(self, height=2, width=10, text="Log Bruh", command=lambda: self.on_increase(self.currCharacter, 1, "bruhMoments"))

        addDamDone.place(relx=.1, rely=.3)
        addDamTaken.place(relx=.2, rely=.3)
        addDamHealed.place(relx=.3, rely=.3)

        addKill.place(relx=.1, rely=.4)
        addDeath.place(relx=.2, rely=.4)
        addHits.place(relx=.3, rely=.4)
        addMiss.place(relx=.4, rely=.4)
        addBruh.place(relx=.5, rely=.4)

        removeCommand.place(relx=.8, rely=.75)

        self.topButtonWidth = 10

        self.offset = 0

        newCharButton = tk.Button(self, height=1, width=self.topButtonWidth, text="New Character", command=self.on_new_character)
        newCharButton.place(x=self.offset, y=0)

        self.controller.update_idletasks()

        self.offsetIncrease = newCharButton.winfo_width()
        self.offset += self.offsetIncrease

        editListButton = tk.Button(self, height=1, width=self.topButtonWidth, text="Edit Char List", command=self.on_edit_character_list)
        editListButton.place(x=self.offset, y=0)

        self.offset += self.offsetIncrease

        editCharButton = tk.Button(self, height=1, width=self.topButtonWidth, text="Edit Char", command=self.on_edit_character)
        editCharButton.place(x=self.offset, y=0)

        self.offset += self.offsetIncrease


        self.startOffset = self.offset

        #add somethng to edit character color or name


    def on_main(self):
        if(not self.game is None):
            self.game.endSession()
            with open("{}/{}.bin".format(self.game.directory, self.game.name), "wb") as f:
                pickle.dump(self.game, f)
        self.controller.unbind('<Control-z>')
        self.controller.unbind('<Control-y>')

        self.command_pivot = -1
        self.commandLabel.delete("1.0", "end")

        self.controller.show_frame("MainMenu")
        

    def on_increase(self, char, amount, stat):
        try:
            amount = int(amount)
            if(amount < 0):
                raise Exception('BadBadNotGood')
            if(self.currCharacter):
                self.listOfCommands = self.game.newCommand(char, amount, stat)

            self.valueEntry.delete(0, 'end')
            self.command_pivot += 1
            self.updateCommandList()
        except:
            print("Bad input")
        

    def updateCommandList(self):
        self.commandLabel.delete("1.0", "end")
        temp = ""
        i = 0
        for s in self.listOfCommands:
            temp += str(i) + ": "
            temp += s
            if(i > self.command_pivot):
                temp += 'X'
            temp += "\n"
            i += 1
            self.commandLabel.insert(tk.END, temp)
            temp = ""

        self.stats.set(self.currCharacter.currString())

    def on_new_character(self):
        #make new window for the popup
        top= tk.Toplevel(self.controller)
        top.geometry("300x300")
        top.title("Add Character")


        #add widgets
        tk.Label(top, text= "Create New Character", font=('Mistral 18 bold')).place(x=20,y=10)
        tk.Label(top, text= "Enter a Unique Name", font=('Mistral 10')).place(x=150,y=50)
        nameEntry = tk.Entry(top)
        nameEntry.place(x=20, y=50)
        tk.Label(top, text= "Enter a Player Name", font=('Mistral 10')).place(x=150,y=80)
        playerEntry = tk.Entry(top)
        playerEntry.place(x=20, y=80)
        tk.Label(top, text= "Optional Color", font=('Mistral 10')).place(x=150,y=110)
        colorEntry = tk.Entry(top)
        colorEntry.place(x=20, y=110)
        nameEntry.focus_set()

        createButton = tk.Button(top, height=2, width=10, text="Create Character", command=lambda: self.on_create_character(nameEntry.get(), playerEntry.get(), colorEntry.get(), top))
        createButton.place(x=100, y=150)

    def on_create_character(self, name, player, color, popWin):
        warning = tk.Label(popWin, text= "", font=('Mistral 12 bold'))
        warning.place(x=100,y=180)

        if(color == ""):
            color = '#FFFFFF'

        #check if a string was entered and if the string already exists in the game
        if(name == "" or player == ""):
            warning.config(text = "Enter valid strings")
        elif(name in self.game.currCharacterNames or name in self.game.oldCharacterNames):
            warning.config(text="Character already exists")
        else:
            #adds the game to the game list and updates the drop down menu
            for i in self.charButtons:
                i.destroy()
            self.charButtons.clear()
            self.offset = self.startOffset
            j = 0


            self.game.addCharacter(name, player, color)
            for i in self.game.activeCharacters:
                temp = tk.Button(self, height=1, width=self.topButtonWidth, text=i.charName, bg = i.color)
                self.charButtons.append(temp)
                self.charButtons[j].place(x=self.offset, y=0)
                self.charButtons[j].configure(command=lambda t = i: self.on_switch_character(t))
                self.offset +=self.offsetIncrease
                j+=1

            popWin.destroy()

    def on_edit_character(self):
        #make new window for the popup
        if(self.currCharacter != None):
            top= tk.Toplevel(self.controller)
            top.geometry("300x300")
            top.title("Edit Character")


            #add widgets
            tk.Label(top, text= "Edit Character", font=('Mistral 18 bold')).place(x=20,y=10)
            tk.Label(top, text= "Char Name: ", font=('Mistral 10')).place(x=150,y=50)
            nameEntry = tk.Entry(top)
            nameEntry.insert(0,self.currCharacter.displayName)
            nameEntry.place(x=20, y=50)
            tk.Label(top, text= "Player Name: ", font=('Mistral 10')).place(x=150,y=80)
            playerEntry = tk.Entry(top)
            playerEntry.insert(0,self.currCharacter.playerName)
            playerEntry.place(x=20, y=80)
            tk.Label(top, text= "Color: ", font=('Mistral 10')).place(x=150,y=110)
            colorEntry = tk.Entry(top)
            colorEntry.insert(0,self.currCharacter.color)
            colorEntry.place(x=20, y=110)
            nameEntry.focus_set()

            editButton1 = tk.Button(top, height=2, width=10, text="Change Character Info", command=lambda: self.editCharacter(nameEntry.get(), playerEntry.get(), colorEntry.get(), top))
            editButton1.place(x=100, y=150)

    def editCharacter(self, name, player, color, popWin):
        warning = tk.Label(popWin, text= "", font=('Mistral 12 bold'))
        warning.place(x=100,y=180)

        if(color == ""):
            color = '#FFFFFF'

        #check if a string was entered and if the string already exists in the game
        if(name == "" or player == "" or color == ""):
            warning.config(text = "Enter valid strings")
        else:
            #adds the game to the game list and updates the drop down menu
            self.currCharacter.displayName = name
            self.currCharacter.playerName = player
            self.currCharacter.color = color
            self.placeCharacterButtons()

            popWin.destroy()

    def on_edit_character_list(self):
        top= tk.Toplevel(self.controller)
        top.geometry("300x300")
        top.title("Edit Character List")


        #add widgets
        tk.Label(top, text= "Character List", font=('Mistral 18 bold')).place(x=20,y=10)

        optionOne = tk.StringVar(value="choose")
        optionTwo = tk.StringVar(value="choose")

        currCharacterOptions = tk.OptionMenu(top,   optionOne, "choose", *self.game.currCharacterNames)
        currCharacterOptions.place(relx=0.1, rely=0.5)

        tk.Label(top, text= "Active").place(relx=.1,rely=.45)


        oldCharacterOptions = tk.OptionMenu(top, optionTwo, "choose", *self.game.oldCharacterNames)
        oldCharacterOptions.place(relx=0.5, rely=0.5)
        tk.Label(top, text= "Inactive").place(relx=.5,rely=.45)



        removeActiveButton = tk.Button(top, height=2, width=10, text="Remove From Active", command=lambda: self.on_remove_active(optionOne.get(), top))
        removeActiveButton.place(relx=.1, rely=.6)

        moveActiveButton = tk.Button(top, height=2, width=10, text="Add to Active", command=lambda: self.on_add_active(optionTwo.get(), top))
        moveActiveButton.place(relx=.1, rely=.7)

        tempActiveButton = tk.Button(top, height=2, width=10, text="make temp Active", command=lambda: self.on_temp_active(optionTwo.get(), top))
        tempActiveButton.place(relx=.1, rely=.8)

        deleteButton = tk.Button(top, height=2, width=10, text="Delete Char", command=lambda: self.on_delete_char(optionTwo.get(), top))
        deleteButton.place(relx=.6, rely=.8)
        tk.Label(top, text= "Deletes from inactive characters").place(relx=.5,rely=.9)

        #drop down of game.currCharacters with button to kill
        #drop down of gaame.oldCharacters with buttons to revive or temporarly bring back
        return 0

    def on_remove_active(self, charName, popWin):
        if(charName != "choose"):
            self.game.moveCharacterToOld(charName)
            self.placeCharacterButtons()
            popWin.destroy()
        else:
            print("Bad Option")

    def on_add_active(self, charName, popWin):
        if(charName != "choose"):
            self.game.moveCharacterToCurrent(charName)
            self.placeCharacterButtons()
            popWin.destroy()
        else:
            print("Bad Option")

    def on_temp_active(self, charName, popWin):
        if(charName != "choose"):
            self.game.viewOldCharacter(charName)
            self.placeCharacterButtons()
            popWin.destroy()
        else:
            print("Bad Option")

    def on_delete_char(self, charName, popWin):
        if(charName != "choose"):
            self.game.deleteCharacter(charName)
            self.placeCharacterButtons()
            popWin.destroy()
        else:
            print("Bad Option")


    def on_cancel_session(self):
        if(not self.game is None):
            self.game.cancelSession()
            with open("{}/{}.bin".format(self.game.directory, self.game.name), "wb") as f:
                pickle.dump(self.game, f)

        self.controller.unbind('<Control-z>')
        self.controller.unbind('<Control-y>')

        self.game = None

        self.command_pivot = -1
        self.commandLabel.delete("1.0", "end")

        self.controller.show_frame("MainMenu")



    #add frame background color switch
    def on_switch_character(self, char):
        self.title.set(char.displayName)
        self.config(background=char.color)
        self.currCharacter = char
        self.stats.set(self.currCharacter.currString())


    def set_game(self, game):
        self.commandLabel.delete("1.0", "end")
        self.controller.bind('<Control-z>', self.undoCommand, "+")
        self.controller.bind('<Control-y>', self.redoCommand, "+")
        
        self.command_pivot = -1
        for i in self.charButtons:
            i.destroy()
        self.charButtons.clear()
        self.game = game
        self.game.startSession()
        self.title.set(self.game.name)
        self.placeCharacterButtons()
        
            #chatgpt

    def placeCharacterButtons(self):
        self.offset = self.startOffset
        for i in self.charButtons:
                i.destroy()
        j = 0
        self.charButtons.clear()
        for i in self.game.activeCharacters:
            temp = tk.Button(self, height=1, width=self.topButtonWidth, text=i.displayName, bg = i.color)
            self.charButtons.append(temp)
            self.charButtons[j].place(x=self.offset, y=0)
            self.charButtons[j].configure(command=lambda t = i: self.on_switch_character(t))
            self.offset += self.offsetIncrease
            j+=1
            self.on_switch_character(i)


    def undoCommand(self, e):
        self.command_pivot = self.game.undo()
        self.updateCommandList()


    def redoCommand(self, e):
        self.command_pivot = self.game.redo()
        self.updateCommandList()

    def on_remove_command(self, spot):
        try:
            spot = int(spot)
            if(spot < 0):
                raise Exception('BadBadNotGood')
            self.command_pivot = self.game.removeCommandByIndex(spot)
            self.updateCommandList()
            self.removeEntry.delete(0, 'end')
        except:
            print("bad input")




# if done from session endGame display bar chart, pie chart, and line chart for session stats, show bar chart and pie chart for total stats
#if done from main menu omit the line chart, get total stats by adding everything up 
class StatsMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="light goldenrod")
        self.stats = pd.DataFrame()
        self.selectiveStats = pd.DataFrame()
        self.game = None
        self.characters = []
        self.charButtons = []
        self.charsToShow = []
        self.usePlayers = tk.IntVar(value=0)

        self.statsLabel = tk.Text(self, height = 12, width = 35)
        self.statsLabel.place(relx=.6, rely = .1)


        removeActiveButton = tk.Button(self, height=2, width=10, text="show stats", command=lambda: self.on_get_stats(self.optionOne.get()))
        removeActiveButton.place(relx=.1, rely=.2)

        self.title = tk.StringVar(value="Empty Game, should not be here")

        self.optionOne = tk.IntVar(value=0)
        self.optionTwo = tk.StringVar(value="damDone")



        label = tk.Label(self, textvariable=self.title, font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label1 = tk.Label(self, text="Session #, 0 for totals")
        label1.place(relx=0.15, rely=0.15)

        players = tk.Checkbutton(self, text="Players", variable = self.usePlayers, command=lambda: self.on_get_stats(self.optionOne.get())).place(relx=.8,rely=.03)



        button = tk.Button(self, text="Go back to home page",
                           command=self.on_main)
        button.pack()

    def on_main(self):
        self.controller.show_frame("MainMenu")


    def set_game(self, game):
        self.game = game
        self.characters = self.game.getStats()
        self.title.set(self.game.name)
        self.sessionOptions = tk.OptionMenu(self, self.optionOne, 0, *range(1, self.game.sessionNum+1))
        self.sessionOptions.place(relx=0.2, rely=0.2)

    def on_get_stats(self, sessionNum):
        df = pd.DataFrame()
        for c in self.characters:
            df = pd.concat([df, c.getStats(sessionNum)])

        df = df.dropna()
        self.stats = df
        self.stats = self.stats.set_index('charName')

        if(self.usePlayers.get() != 0):
            self.stats = self.stats.groupby(['playerName'], as_index=True).sum()
            self.stats['color'] = [x[:7] for x in self.stats['color']] 

        self.stats['accuracy'] = np.where(self.stats['hits'] + self.stats['misses'] > 0, self.stats['hits'] / (self.stats['hits'] + self.stats['misses']), 0)

        self.selectiveStats = self.stats
        self.statOptions = tk.OptionMenu(self, self.optionTwo, "damDone", *self.stats.columns[4:], command=self.on_show_stats)
        self.statOptions.place(relx=0.3, rely=0.2)
        self.placeCharacterToggles()
        self.on_show_stats()


    def on_show_stats(self, *args):
        statNames = self.optionTwo.get()
        self.updateStatList(statNames)
        self.updateGraphs(statNames)

    def updateStatList(self, statName):
        self.statsLabel.delete("1.0", "end")
        temp = ""
        temp += statName + "\n"
        for index, row in self.stats.iterrows():
            temp += index + ": "
            temp += str(row[statName])
            temp += "\n"
            self.statsLabel.insert(tk.END, temp)
            temp = ""

    def updateGraphs(self, statNames):
        if((self.selectiveStats[statNames] == 0).all()):
            return 0
        f = Figure(figsize=(8,3), dpi=100)
        a = f.add_subplot(121)
        a.set_title('pie chart')
        a1 = f.add_subplot(122)
        a1.set_title('bar graph')

        a.pie(self.selectiveStats[statNames], labels = self.selectiveStats.index, colors = self.selectiveStats["color"])
        a1.bar(self.selectiveStats.index, self.selectiveStats[statNames], color = self.selectiveStats["color"])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().place(relx=0, rely=0.45)

        
        canvas._tkcanvas.place(relx=0, rely=0.45)

    def on_toggle_char(self):
        self.selectiveStats = self.stats
        i = 0
        for t in self.charsToShow:
            if(t.get() == 0):
                self.selectiveStats = self.selectiveStats.drop(axis=0, labels=self.selectiveStats.index[i])
                i -= 1
            i += 1

        self.updateGraphs(self.optionTwo.get())


    def placeCharacterToggles(self):
        offset = 5
        for i in self.charButtons:
                i.destroy()
        j = 0
        self.charButtons.clear()
        self.charsToShow.clear()
        for i in self.stats.index:
            self.charsToShow.append(tk.IntVar(value=1))
            temp = tk.Checkbutton(self, text=i, variable = self.charsToShow[j])
            self.charButtons.append(temp)
            self.charButtons[j].place(x=offset, y=10)
            self.charButtons[j].configure(command=lambda: self.on_toggle_char())
            offset += 60
            j+=1

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()