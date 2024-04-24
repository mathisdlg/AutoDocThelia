import sys, os
from Common import integrate

help="eventAnalyser.py [SOURCE FILE] [DESTINATION FILE]"
helpAccess="-h or --help to show help"

def main(sourceFile, saveFile):
    # the file path where the data array is

    arrayFile = "dataArrayEvent.txt"

    # source file parsing

    header = True
    firstLines = True
    arrayAllEvents = []
    arrayConstants = []
    nbBracket = 0


    with open(sourceFile, "r") as file :
        for line in file.readlines() :
            if header :
                if "{" in line :
                    header = False
                    nbBracket += 1
            elif firstLines :
                if "//" in line and "end" not in line.lower() :
                    arrayEvent = []
                    firstLines = False
                    category = ""
                    isCategory = False
                    for letter in line :
                        if letter.isalpha() :
                            isCategory = True
                        elif letter == "-" or letter == "\n" :
                            isCategory = False
                        if isCategory :
                            category += letter.lower()
                    categorySplit = category.strip().lower().split(" ")
                    if categorySplit[-1] in ["management", "event", "events", "module", "modules"] and len(categorySplit) > 1:
                        index = category.find(categorySplit[-1])
                        category = category[0:index]
                    arrayEvent.append(category.capitalize())
            else :
                if "//" in line and "end" not in line.lower() :
                    arrayAllEvents.append(arrayEvent)
                    arrayEvent = []
                    category = ""
                    isCategory = False
                    for letter in line :
                        if letter.isalpha() :
                            isCategory = True
                        elif letter == "-" or letter == "\n" :
                            isCategory = False
                        if isCategory :
                            category += letter.lower()
                    categorySplit = category.strip().lower().split(" ")
                    if categorySplit[-1] in ["management", "event", "events", "module", "modules"] and len(categorySplit) > 1:
                        index = category.find(categorySplit[-1])
                        category = category[0:index]
                    arrayEvent.append(category.capitalize())
                elif "* " in line and "/" not in line :
                    comment = ""
                    isComment = False
                    for letter in line :
                        if letter.isalpha() :
                            isComment = True
                        elif letter == "\n"  :
                            isComment = False
                        if isComment :
                            comment += letter
                    arrayConstants.append(comment.strip())
                elif "public const" in line :
                    constant = "**"+line.strip().split("public const ")[1].replace(";", "")
                    index = constant.find("=")-1
                    constant = constant[:index]+"**"+constant[index:]
                    
                    arrayConstants.append(constant.strip())
                    arrayEvent.append(arrayConstants)
                    arrayConstants = []
                elif "function" in line :
                    arrayConstants = []
                elif "{" in line :
                    nbBracket += 1
                elif "}" in line :
                    nbBracket -= 1
                    if nbBracket <= 0 :
                        arrayAllEvents.append(arrayEvent)
    arrayAllEvents.sort()

    # Data fusion

    arrayAllEventsSecondData = []
    firstChar = True
    firstComma = True
    lastCharIsBracket = False

    with open(arrayFile, "r") as file :
        for line in file :
            for character in line :
                if firstChar :
                    firstChar = False
                else :
                    if character == "[" :
                        arrayEventSecondaryData = []
                        firstArgument = ""
                        secondArgument = ""
                        firstComma = True
                        lastCharIsBracket = False
                    elif not lastCharIsBracket and character == "]" :
                        arrayEventSecondaryData.append(firstArgument.strip())
                        arrayEventSecondaryData.append(secondArgument.replace("\\n", "\n"))
                        arrayAllEventsSecondData.append(arrayEventSecondaryData)
                        lastCharIsBracket = True
                    elif lastCharIsBracket and character == "]" :
                        break
                    elif firstComma and character == "," :
                        firstComma = False
                    elif firstComma :
                        firstArgument += character
                    elif not firstComma :
                        secondArgument += character

    # Array exploitation to make a markdown file

    arrayNoCategory = list(arrayAllEventsSecondData)

    with open(saveFile, "w") as file :
        file.write("## Every event list\n\n")
        for event in arrayAllEvents :
            file.write("### " + event[0] + "\n\n<details><summary>Detail</summary>\n\n")
            
            for iterator in range(1, len(event)) :
                for element in event[iterator] :
                    file.write(element + "  \n")
                file.write("\n")
            
            file.write("__________________\n\n")
            
            for eventSecondData in arrayAllEventsSecondData :
                if (eventSecondData[0] != "Nocategory") and (eventSecondData[0].lower().replace(" ", "") in event[0].lower().replace(" ", "") or eventSecondData[0].lower() in event[0].lower().replace(" ", "").replace("ies", "y") or eventSecondData[0].lower().replace("saleelement", "") in event[0].lower().replace(" ", "")) :
                    file.write(eventSecondData[1] + "\n\n")
                    if eventSecondData in arrayNoCategory :
                        arrayNoCategory.remove(eventSecondData)
            file.write("</details>\n\n")

        file.write("### No classified" + "\n\n<details><summary>Detail</summary>\n\n")
        for event in arrayNoCategory :
            file.write("**" + event[0] + "** : \n" + event[1] + "\n\n")
        file.write("</details>\n\n")
    
    docFile = input("Enter the events documentation file to modify : ")
    integrate(saveFile, docFile, "Every event list")

        
if __name__ == "__main__":

    # Verification of the number of arguments

    if len(sys.argv) < 2 :
        print("Error : missing argument")
        print(help, "\n", helpAccess)
        exit(1)
    elif len(sys.argv) > 3 :
        print("Error : Too many arguments")
        print(help, "\n", helpAccess)
        exit(1)

    # Need help ?

    if sys.argv[1] == "-h" or sys.argv[1] == "--help" :
        print("""
    Parse the source file to get information about Thelia events constants.
    Analyze the dataArrayEvent.txt file to obtain information on Thelia event methods.
    The source file should be the TheliaEvents.php file.
    You should include absolute path in the files names.

    To get the parsing result in the file you want :
        eventAnalyser.py [SOURCE FILE] [DESTINATION FILE]

    To get the parsing result in the default file 'parsedEvents.md' in the same repository as eventAnalyser.sh :
        eventAnalyser.py [SOURCE FILE]
    """)
        exit(0)
    
    # the file path where the analyse is done

    if not os.path.exists(sys.argv[1]) :
        print("Error : Destination file not found")
        print(help, "\n", helpAccess)
        exit(2)
    else :
        sourceFile = sys.argv[1]
    
    # the file path where the analyse is save

    if len(sys.argv) == 3 :
        saveFile = sys.argv[2]
    else :
        saveFile = "parsedEvents2.md"
    
    main(sourceFile, saveFile)