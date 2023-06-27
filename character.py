import pandas as pd
import os

class characters():
    #create a load from csv option
    #add things for character images, 

    #maybe make stat class and use character as the invoker
    def __init__(self, gameDirectory, charName, playerName, color="#FFFFFF", totDamDone = 0, totDamTaken = 0, totKills = 0, totDeaths = 0, totHeal = 0, totHits = 0, totMisses = 0, totBruhMoments = 0):
        #basic character information
        self.charName = charName
        self.playerName = playerName
        self.color = color

        #path to folder for character files
        self.directory = "{}/{}".format(gameDirectory, self.charName)
        os.mkdir(self.directory)

        #series for storing current session stats and total stats for the character
        self.currStats = pd.Series({"session":0, "damDone":totDamDone, "damTaken":totDamTaken, "damHealed":totHeal, "kills":totKills, "deaths":totDeaths, "hits":totHits, "misses":totMisses, "bruhMoments":totBruhMoments})
        self.totStats = pd.Series({"damDone":totDamDone, "damTaken":totDamTaken, "damHealed":totHeal, "kills":totKills, "deaths":totDeaths, "hits":totHits, "misses":totMisses, "bruhMoments":totBruhMoments})

        #Set up temporary dataframe to create csv file with the initial stats
        history = pd.DataFrame(columns=['session', 'damDone', 'damTaken', 'damHealed', 'kills', 'deaths', 'hits', 'misses', 'bruhMoments'])
        history = pd.concat([history, self.currStats.to_frame().T])
        infile = self.directory + "/{}Backup.csv".format(self.charName)
        history.to_csv(infile, index = False)

        self.startSession()

    
    def getStats(self, sessionNum):
        infile = self.directory + "/{}Backup.csv".format(self.charName)
        temp = pd.read_csv(infile)
        history = temp.loc[temp['session']==sessionNum]
        history.insert(0, "color", [self.color], True)
        history.insert(0, "charName", [self.charName], True)
        history.insert(0, "playerName", [self.playerName], True)
        return (history)

    #Resets currStats to 0 to use for stats for a specific session
    #Input: none
    def startSession(self):
        for i in self.currStats.index:
            self.currStats.loc[i] = 0

    #appends current stats to history data frame, resets the current stats to 0,
    #and adds the current stats to the totals row of the dataframe(session 0), make csv with the data
    #Input - the session number
    def endSession(self, sessionNum):
        #open history dataframe from csv
        self.currStats['session'] = sessionNum

        infile = self.directory + "/{}Backup.csv".format(self.charName)
        history = pd.read_csv(infile, index_col='session')
        history = pd.concat([history, (self.currStats.to_frame().T).set_index('session')])

        for i in self.currStats.index:
            if(i != 'session'):
                history.loc[0, i] += self.currStats.loc[i]
                self.currStats.loc[i] = 0

        history.to_csv(infile, index = 'session')

    #cancels the session, rewrites the the csv with nothing new
    def cancelSession(self):
        #open history dataframe from csv
        infile = self.directory + "/{}Backup.csv".format(self.charName)
        history = pd.read_csv(infile, index_col='session')

        history.to_csv(infile, index = 'session')


    def currString(self):
        temp = ""
        for i in self.currStats.items():
            if(i[0] != 'session'):
                temp += i[0] + ": " + str(i[1]) + "\n"

        return temp


    #Updates a stat for the command design pattern
    def updateStat(self, amount, stat):
        self.currStats[stat] += amount
        self.totStats[stat] += amount

    def undoStat(self, amount, stat):
        self.currStats[stat] -= amount
        self.totStats[stat] -= amount

    def __eq__(self, name):
        if isinstance(name, str):
            return (self.charName == name)

        return False