import CommonFunctions.formatTools as q
import csv
import datetime


async def checkPlaytimeCSV(username):
    try:
        shame = False
        
        with open("StoredData/hours.csv", mode="r") as csvf:
            csvReader = csv.DictReader(csvf)
            
            q.newline(baronly=True)
            
            q.sendLogMessage(f"Searching for playtime of user: {username}")
            
            for row in csvReader:
                if row['username'] == username:
                    playerPlaytime = int(row['minutesplayed'])
                    q.sendLogMessage(f"Found {username} with {playerPlaytime} minutes played", type="Success")
                    break
        
        if playerPlaytime == 360 or playerPlaytime == 420 or playerPlaytime == 480 or playerPlaytime == 540:
            shame = True
        
        q.newline()
        
        return playerPlaytime, shame
    
    except Exception as e:
        q.sendLogMessage(f"Error checking playtime of {username}: {e}", type="Error")
        return None, None


async def updatePlaytime(username = "", additionalMinutes = 0, resetAll = False):
    
    try:
        
        if resetAll == True:
            with open("StoredData/hours.csv", mode="r") as csvf:
                csvReader = csv.DictReader(csvf)
                
                data = list(csvReader)
                
                csvf.close()
                
            for row in data:
                try:
                    row['minutesplayed'] = str(0)
                    q.newline(baronly=True)
                    q.sendLogMessage(f"Reset {row['username']}'s minutes.", type="Success")
                except Exception as e:
                    q.sendLogMessage(f"Error occured while reseting a user's playtime: {e}'", type="Error")
            
        else:
        
            q.newline()
        
            #q.sendLogMessage(f"Updating {username}'s playtime by {additionalMinutes} minutes")
            
            with open("StoredData/hours.csv", mode="r") as csvf:
                csvReader = csv.DictReader(csvf)
                
                data = list(csvReader)
                
                csvf.close()
                
            if all(row['username'] not in username for row in data) and username != "":
                q.sendLogMessage(f"Could not find username '{username}' in file, notifying Ben through DMs", type="Warning")
                
                return None
            
            if all(row['username'] == username and str(row['discorduserid']) == "0" for row in data):
                q.sendLogMessage(f"Discord ID is empty for user: {username}, getting Discord ID through Ben using DMs", type="Warning")
                
                return None
            
            #q.sendLogMessage(f"Updating {username}'s playtime by {additionalMinutes} minutes", type="Info")

            for row in data:
                
                #q.sendLogMessage(f"Updating {row['username']}")
                
                if row['username'] in username:                
                    row['minutesplayed'] = str(int(row['minutesplayed']) + additionalMinutes)
                    q.sendLogMessage(f"Increased {username}'s minutes played by {additionalMinutes}", type="Success")
                    q.sendLogMessage(f"New Minutes: {row['minutesplayed']} ({(int(row['minutesplayed']))/60} Hours)", type="Info")
            
        
        with open("StoredData/hours.csv", mode="w", newline='') as csvf:
            fieldnames = ['username', 'minutesplayed', 'discorduserid']
            
            csvWriter = csv.DictWriter(csvf, fieldnames=fieldnames)
            
            csvWriter.writeheader()
            csvWriter.writerows(data)
            
            csvf.close()
                
            return True
        
    except Exception as e:
        q.sendLogMessage(f"Error updating {username}'s playtime: {e}", type="Error")
        return "Error"


async def getUserID(player):
    try:
        q.sendLogMessage(f"Searching for userID of player: {player}")
        
        with open("StoredData/hours.csv", mode="r") as csvf:
            csvReader = csv.DictReader(csvf)
            
            data = list(csvReader)
        
        for row in data:
            if row['username'] == player:
                q.sendLogMessage(f"Found {player} with userID: {row['discorduserid']}", type="Success")
                return row['discorduserid']
            
        q.sendLogMessage(f"Could not find {player} in file.", type="Warning")
        
        return None
    
    except Exception as e:
        q.sendLogMessage(f"Error finding userID of {player}: {e}", type="Error")
        return None

async def updateRecord(playername, discordID):
    try:
        q.sendLogMessage(f"Updating '{playername}' discord ID to '{discordID}'")
        
        with open("StoredData/hours.csv", mode="r") as csvf:
            csvReader = csv.DictReader(csvf)
            
            data = list(csvReader)
            
        for row in data:
            if row['username'] == playername and row['discorduserid'] == "0":
                row['discorduserid'] = discordID
                #q.sendLogMessage(f"Updated '{playername}' discord ID to '{discordID}'", type="Success")
        
        with open("StoredData/hours.csv", mode="w", newline='') as csvf:
            fieldnames = ['username', 'minutesplayed', 'discorduserid']
            
            csvWriter = csv.DictWriter(csvf, fieldnames=fieldnames)
            
            csvWriter.writeheader()
            csvWriter.writerows(data)
            
        csvf.close()
            
        return True
    
    except Exception as e:
        q.sendLogMessage(f"Error updating {playername}'s discord ID: {e}", type="Error")
        return False

async def createRecord(playername, minutesplayed, discordID):
    try:
        q.sendLogMessage(f"Creating record for {playername} with {minutesplayed} minutes played and discord ID {discordID}")
        
        with open("StoredData/hours.csv", mode="a", newline='') as csvf:
            fieldnames = ['username', 'minutesplayed', 'discorduserid']
            
            csvWriter = csv.DictWriter(csvf, fieldnames=fieldnames)
            
            csvWriter.writerow({'username': playername, 'minutesplayed': minutesplayed, 'discorduserid': discordID})
            
        return True

    except Exception as e:
        q.sendLogMessage(f"Error creating record for {playername}: {e}", type="Error")
        return False
    
async def addToWachedMovies(movieName, date=None, requestUser=None):
    try:
        if not movieName:
            q.sendLogMessage("No movie name provided", type="Error")
            return False
        
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        q.newline(baronly=True)
            
        q.sendLogMessage(f"Adding {movieName} to watched movies list with time: {date}")
                
        with open("StoredData/watchedMovies.csv", mode="a") as csvf:
            csvf.write("\n")
            fieldnames = ['movieName', 'dateWatched', 'requestedBy']
            
            csvWriter = csv.DictWriter(csvf, fieldnames=fieldnames)
            
            csvWriter.writerow({'movieName': movieName, 'dateWatched': date, 'requestedBy': {requestUser}})
            
        q.sendLogMessage(f"Added {movieName} to watched movies list with time: {date}", type="Success")
        
        return True
    
    except Exception as e:
        q.sendLogMessage(f"Error adding {movieName} to watched movies list: {e}", type="Error")