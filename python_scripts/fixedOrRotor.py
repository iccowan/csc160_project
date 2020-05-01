# This short python program takes the data that we know
# and provides a convenient way to combine the data into 1
# file and determine whether or not the aircraft are fixed wing
# or rotor wing.

# I later added a function to determine the time of year for
# each piece of data along with a way to separate out the year
# for ease of access when using the data.

import json

def runProgram():
    # Get the data to examine
    fileName = input("File name to update information: ")
    with open(fileName, "r") as read_file:
        data = json.load(read_file)
        read_file.close()
    
    data = data["markers"]
    
    # Get known data (this is cool)
    with open("knownACTypes.json", "r") as read_file:
        knownData = json.load(read_file)
        read_file.close()
    
    # Loop through all the data and determine the type of aircraft for each
    for d in data:
        print("AC Type:", d["manmo"])
        if d["manmo"] in knownData.keys():
            # Already known
            fOrr = knownData[d["manmo"]]
            print("Known aircraft type:", fOrr)
        else:
            # Ask and remember
            fOrr = input("Fixed (f) or Rotor (r) or Other (o)? ")
            knownData[d["manmo"]] = fOrr
        
        # Update the data
        if fOrr == "f":
            d["aircraftType"] = "fixed"
        elif fOrr == "r":
            d["aircraftType"] = "rotor"
        else:
            d["aircraftType"] = "other/unknown"
            
    # Now, save everything to the respective JSON files
    with open("combinedData.json", "r") as read_file:
        combinedData = json.load(read_file)
        read_file.close()
    
    # Combine the old data and the new data
    newData = combinedData["data"] + data;
    
    with open("combinedData.json", "w") as write_file:
        json.dump({"data": newData}, write_file)
        write_file.close()
    
    with open("knownACTypes.json", "w") as write_file:
        json.dump(knownData, write_file)
        write_file.close()
    
def getYearAndTime():
    # Get the data to examine
    with open("combinedData.json", "r") as read_file:
        data = json.load(read_file)
        read_file.close()
        
    data = data["data"]
    
    for d in data:
        # Split the HTML String
        htmlStr = d["html"]
        htmlSplit = htmlStr.split("<br />")
        
        # Get the location
        d["location"] = htmlSplit[2].strip()
        
        # Get the date
        d["date"] = htmlSplit[3].strip()
        
        # Get the year
        year = int(d["date"][6:])
        d["year"] = year
        
        # Get the time of year
        month = int(d["date"][:2])
        if month == 12 or month < 2:
            d["timeOfYear"] = "winter"
        elif 3 <= month and month <= 5:
            d["timeOfYear"] = "spring"
        elif 6 <= month and month <= 8:
            d["timeOfYear"] = "summer"
        else:
            d["timeOfYear"] = "fall"
        
        # Get the NTSB ID
        d["ntsbID"] = htmlSplit[1].split("'")[-1][1:-4]
        
        # Get the total number of injuries
        injuries = htmlSplit[0].split("<b>")[1][:-4].split("  ")[1].split(" ")
        
        injDict = {
                "none" : 0,
                "minor" : 0,
                "serious" : 0,
                "fatal" : 0,
                "totalInjuredEXCFatalities" : 0,
                "totalInjuredINCFatalities": 0,
                "totalUninjured" : 0
        }
        
        for i in injuries:
            injury = i.split("=")
            
            if injury[0] == "None" :
                injDict["none"] = int(injury[1])
                injDict["totalUninjured"] += int(injury[1])
            elif injury[0] == "Minor":
                injDict["minor"] = int(injury[1])
                injDict["totalInjuredINCFatalities"] += int(injury[1])
                injDict["totalInjuredEXCFatalities"] += int(injury[1])
            elif injury[0] == "Serious":
                injDict["serious"] = int(injury[1])
                injDict["totalInjuredINCFatalities"] += int(injury[1])
                injDict["totalInjuredEXCFatalities"] += int(injury[1])
            elif injury[0] == "Fatal":
                injDict["fatal"] = int(injury[1])
                injDict["totalInjuredINCFatalities"] += int(injury[1])
        
        d["injuries"] = injDict
        
        # Remove excess and unnecessary information
        d.pop("html")
        d.pop("inj")
        d.pop("fatal")
        
    # Now, we replace the information as a JSON
    with open("allData.json", "w") as write_file:
        json.dump({"data": data}, write_file)
        write_file.close()
        
# runProgram() # Assign aircraft types
getYearAndTime() # Get the years, time, and some more information
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        