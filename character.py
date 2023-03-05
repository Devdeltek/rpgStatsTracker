import pandas as pd
import os

class characters():
    #todo: pickle, csv
    #create a load from csv option
    #add things for character images, 

    #maybe make stat class and use character as the invoker
    def __init__(self, gameDirectory, charName, playerName, totDamDone = 0, totDamTaken = 0, totKills = 0, totDeaths = 0, totHeal = 0, totHits = 0, totMisses = 0, totBruhMoments = 0):
        self.charName = charName
        self.playerName = playerName

        self.directory = "{}/{}".format(self.gameDirectory, self.charName)
        os.mkdir(directory)

        self.currStats = {"session":0, "damDone":totDamDone, "damTaken":totDamTaken, "damHealed":totHeal, "kills":totKills, "deaths":totDeaths, "hits":totHits, "misses":totMisses, "bruhMoments":totBruhMoments}
        self.totStats = {"damDone":totDamDone, "damTaken":totDamTaken, "damHealed":totHeal, "kills":totKills, "deaths":totDeaths, "hits":totHits, "misses":totMisses, "bruhMoments":totBruhMoments}

        #Set up temporary dataframe to create csv file with the initial stats
        history = pd.DataFrame(columns=['session', 'damDone', 'damTaken', 'damHealed', 'kills', 'deaths', 'hits', 'misses', 'bruhMoments'])
        history.append(currStats.to_frame().T)
        infile = directory + "/{}Backup.csv".format(self.charName)
        history.to_csv(infile, index_col = 0)

        startSession()

    
    #Resets currStats to 0 to use for stats for a specific session
    #Input: none
    def startSession(self):
        for i in self.currStats.items():
            self.currStats[i] = 0

    #appends current stats to history data frame, resets the current stats to 0,
    #and adds the current stats to the totals row of the dataframe(session 0), make csv with the data
    #Input - the session number
    def endSession(self, sessionNum):
        #open history dataframe from csv
        self.currStats['session'] = sessionNum

        infile = directory + "/{}Backup.csv".format(self.charName)
        history = pandas.read_csv(infile, index_col = 0)
        history.append(currStats.to_frame().T)

        for i in self.currStats.items():
            self.history.loc[0, i] += currStats[i]
            self.currStats[i] = 0

        history.loc[0, 'session'] = 0
        history.to_csv(infile, index_col = 0)


    #Updates a stat for the command design pattern
    def updateStat(self, amount, stat):
        self.currStats[stat] += amount
        self.totStats[stat] += amount

    def __eq__(self, name):
        if isinstance(name, str):
            return (self.charName == name)

        return False