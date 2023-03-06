import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
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

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Alchemist Frum Craftkins Post Battle Summary")
        self.geometry("800x600")
        self.resizable(width=True, height=True)
        self.wm_attributes('-transparentcolor', '#ab23ff')

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

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

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="DarkOliveGreen2")

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Game", command=self.on_new_game)

        menubar.add_cascade(label="File", menu=filemenu)

        controller.config(menu=menubar)

        loadButton = tk.Button(self, height=5, width=30, text="Load Game", command=self.on_load)
        statButton = tk.Button(self, height=5, width=30, text="View Stats", command=self.on_stat)
        quitButton = tk.Button(self, height=5, width=30, text="Quit Game", command=self.on_quit)

        menu_label = tk.Label(self, text="Post Battle Summary", font=("TkDefaultFont", 64), bg="#ab23ff")

        loadButton.place(relx = 0.1, rely = 0.6)
        statButton.place(relx = 0.6, rely = 0.6)
        quitButton.place(relx = 0.5, rely = 0.9, anchor=tk.CENTER)
        menu_label.place(relx=.5, rely=.25,anchor=tk.CENTER)

    def on_load(self):
        self.controller.show_frame("GameMenu")

    def on_new_game(self):
        print("new game")

    def on_stat(self):
        self.controller.show_frame("StatsMenu")

    def on_quit(self):
        self.controller.destroy()


class GameMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page", command=self.on_main)
        button.pack()

    def on_main(self):
        self.controller.show_frame("MainMenu")


class StatsMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Character", command=self.on_new_character)

        menubar.add_cascade(label="File", menu=filemenu)

        controller.config(menu=menubar)

        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go /to the start page",
                           command=self.on_main)
        button.pack()

    def on_main(self):
        self.controller.show_frame("MainMenu")

    def on_new_character(self):
        print("new character")


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

        #https://subscription.packtpub.com/book/application-development/9781788835886/1/ch01lvl1sec12/creating-a-tkinter-hello-world

        #https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter