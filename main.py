import tkinter as tk
#store a list of game names as a pickle
#add view window, can be seperate tab or opened in a new window, should be able to view current session and totals in real time for active characters, or past session for all characters who are relevant
#can toggle between which characters are shown in the graphs, current session - active characters, total - all characters, previous session - all charactes present in that session based on csv files
#add drop down to rename characters
#end session takes back to main menu, make sure clicking x will call end session stuff
#each game should have a pickle

#on start up unpickle the list of game names, open a main menu with a drop down to select a game based on the game name list. When a game name is selected the program
# will  open a pickle./{gameName}/{gameName}.bin to load the game information. start session will be called on that game and user will be moved to a game screen with tabs for
#each character and a tab for real time graphs. Drop down menus will allow for things like changing character names, changing session number, ect. There will be an input field
#for stats that increase by more than 1, a button for each stat that increases by one, and a list to the right of all the current commands so you can undo easier. End the session
#by either pressing x or an end session button, when session is ended the view page will be opened in its own window to show session stats and total stats, then when that is closed program will end
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent



if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()