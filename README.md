# RPG Stat Tracker

![Image of a beautiful main menu.](https://raw.githubusercontent.com/Devdeltek/DevWebsite/main/dev-website/public/stattrackerMainMenu.png)

**Description:**  


A simple python program to track stats in a table top RPG game such as DND or PF2e. This program uses tkinter for the gui, MatPlotLib to render graphs of the stats, and Pandas and Numpy to handle data. It allows a user to create multiple games, each with its own set of characters. Users are also able to manage characters in events such as character deaths or resurrections. It is able to store data for:  

 - Damage Done  

 - Damage Taken  

 - Damage Healed  

 - Kills  

 - Downs (Deaths)  

 - hits  

 - misses(together with hits for accuracy)  

 - bruh moments (for when a player is late or troublesome, use at your discretion)  

It can display data related to these fields either by session or by total, as well as by player or by character. 

**Dependencies:**  

 - Python 3  

 - Tkinter  

 - MatPlotLib  

 - Pandas  

 - Numpy  

**To Run:**  

 - Open the folder in your file explorer and run: python3 main.py  

 - May not work on Linux Or Mac, I have not check compatability yet  

**To Use:**
The Main menu has 5 buttons, New Game, Load Game, Delete Game, View Stats, and Quit  

![Image of a beautiful main menu.](https://raw.githubusercontent.com/Devdeltek/DevWebsite/main/dev-website/public/stattrackerMainMenu.png)

Clicking New Game will bring up a pop up menu prompting for a game name. Entering a name and clicking Create Game will then add that game to the options menu above Load Game.  

Clicking Load Game will start a new session of the game selected by the options menu. This is where you can add characters and manage characters, as well as track stats. Use the buttons in the top left to open pop up windows for these purposes.  

![Image of the character create menu and the stat track menu.](https://raw.githubusercontent.com/Devdeltek/DevWebsite/main/dev-website/public/stattrackerCreateChar.png)

 - Stats are entered with the bunch of buttons in the middle of the window. Damage Done, Damage Taken, Damage Healed will all use an integer value entered in the entry box. Hits, misses, kills, deaths and bruh moments are all incremental and add 1 at a time.

 - The program uses a command design pattern to allow for undo/redo of entered stats. If you undo and enter a new stat, the undone stat will be overwritten.  

 - If you just want to edit characters without storing stats, after you make the character changes click Cancel Session. End Session will ensure all character stats are stored. Do not use the X to close this window, it will mess with the session counter.  

 ![Image of the session menu with characters.](https://raw.githubusercontent.com/Devdeltek/DevWebsite/main/dev-website/public/stattrackerSessionMenu.png)

Clicking Delete Game will delete all files associated with the current game selected in the options menu, with no method of recovery. Be careful  

Click View Stats will show stats for the game selected in the options menu. It will take you to a windows with a button that says Show Stats, an options menu with a session number and a check box for players.  

![Image of the stats Menu.](https://raw.githubusercontent.com/Devdeltek/DevWebsite/main/dev-website/public/stattrackerStats1.png)

 - The Session number options menu selects which session you want to view stats of, with 0 being total. Show Stats must be clicked if the session number is changed. After Show Stats is clicked, a new options menu with the different stats tracked will show up. This allows you to change which stat is currently being view. Stats will be shown in text form, bar graph form, and pie chart form unless the stat for all characters is 0  

  - In the top left there are check boxes for each character present in the session. Unchecking the check boxes removes that character from the graphs. There is also a check box labeled players. Checking the Players box will show stats in terms of players rather than characters, so a player with multiple characters will have their stats added together.  

   - clicking the Go back to home page button will take you back to the Main Menu  

   Clicking the Quit button will close the application.