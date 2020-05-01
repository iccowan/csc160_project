import json

def convert():
    # Get the data to examine
    fileName = input("File name to convert: ")
    with open(fileName, "r") as read_file:
        data = json.load(read_file)
        read_file.close()
    data = data["data"]

    # Create a file and make it a csv
    output_file_name = fileName.split(".")[0] + ".csv"
    with open(output_file_name, "w") as read_file:
        read_file.write("manmo,lat,long,aircraftType,location,date,year,timeOfYear,ntsbID,no_injuries,minor_injuries,serious_injuries,fatal_injuries,total_injuries_exc_fatal,total_injuries_inc_fatal, total_uninjured\n")

        for d in data:
            addString = str(d["manmo"]) + "," + str(d["lat"]) + "," + str(d["long"]) + "," + str(d["aircraftType"]) + ",\"" + str(d["location"]) +"\"," + str(d["date"]) + "," + str(d["year"]) + "," + str(d["timeOfYear"]) + "," + str(d["ntsbID"]) + "," + str(d["injuries"]["none"]) + "," + str(d["injuries"]["minor"]) + "," + str(d["injuries"]["serious"]) + "," + str(d["injuries"]["fatal"]) + "," + str(d["injuries"]["totalInjuredEXCFatalities"]) + "," + str(d["injuries"]["totalInjuredINCFatalities"]) + "," + str(d["injuries"]["totalUninjured"]) + "\n"
            read_file.write(addString)

        read_file.close()

convert()