from io import TextIOWrapper
import os

def getCommands(directory: str) -> dict:
    fileList = []
    listExtends = ["ContainerAwareCommand"]

    commandAddedOrExtendsAdded = True

    commands = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith(".php") and not "vendor" in path:
                if canBeACommand(path):
                    fileList.append(path)

    while commandAddedOrExtendsAdded:
        commandAddedOrExtendsAdded = False
        for file in fileList:
            print(file)
            match getFileConfig(file, commands, fileList, listExtends):
                case 0:
                    print("Command found")
                    commandAddedOrExtendsAdded = True
                case 1:
                    print("New extends found")
                    commandAddedOrExtendsAdded = True
                case 2:
                    print("Command not found but can be a command")
                case 3:
                    print("Not a command at all")

    return commands


def canBeACommand(path: str) -> bool:
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if (line.startswith("class") or line.startswith("abstract")):
                indexExtends = line.find("extends")
                return indexExtends != -1
    return False


def getFileConfig(path: str, commands: dict[str: list[list[str, list[str]]]], fileList: list[str], listExtends: list[str]) -> int:
    with open(path, "r") as f:
        isClass = False
        for line in f:
            line = line.strip()
            if (line.startswith("class") or line.startswith("abstract")):
                indexExtends = line.find("extends")
                if indexExtends != -1:
                    extends = line[indexExtends + len("extends"):] if not line.endswith("{") else line[indexExtends + len("extends"):line.index("{")].strip()
                    if extends in listExtends:
                        if line.startswith("class"):
                            isClass = True
                            name, config = getConfig(f)
                            commands[name] = config
                        listExtends.append(line[line.index("class ") + len("class "):indexExtends].strip())
                        return 0 if isClass else 1
                    else:
                        fileList.append(path)
                        return 2
    return 3


def format(sequence: str) -> str :
    if sequence[-1] in {"\'", "\""} and sequence[0] in {"\'", "\""} :
        sequence = sequence[:-1]
        sequence = sequence[1:]
    return sequence


def getConfig(file: TextIOWrapper) -> tuple[str, list[list[str, list[str]]]] :

    # list structure
    # arrayAllConfig : [["setDescription", ["This command do this"]], ["addOption", ["option1", "option2"]]]
    # arrayConfig :     |------------------------------------------|  |-----------------------------------|
    # arrayContent :                       |----------------------|                 |--------------------|
    arrayAllConfig = []
    arrayConfig = []
    arrayContent = []
    
    # Define if we are in a header line or not
    header = True
    
    # Define if the letter we analyse is part of the config name (examples : "setDescription", "addOption", ...)
    isConfigName = False
    
    # Define if the letter we analyse is part of the content
    isContent = False
    
    # Count the number of parents. If this number > 0, a parenthesis is open while the previous one has not yet been closed.
    nbParenthesis = 0
    
    # Define if the line we are analyzing is part of the previous one
    isReturnLine = False
    
    # Define if the letter we are analyzing is the first one of the current content
    isFirstChar = True
    # Define if the first char is a " or a '
    firstChar = ""
    # Count the number of first characters. If this number > 0, then the string is not closed and commas should not be treated as field separators.
    nbFirstChar = 0
    
    configName = ""
    contentName = ""

    for line in file:
        if header :
            if "function configure" in line :
                # Begin of configure function
                header = False
        else:

            if "->" in line and nbParenthesis == 0 :
                listElements = line.split("->")
                
                for iterator in range(1, len(listElements)) :
                    isConfigName = True
                    isContent = False
                    isFirstChar = True
                    for letter in listElements[iterator] :
                        if isContent :
                            if isFirstChar and (letter == "\"" or letter == "\'") :
                                isFirstChar = False
                                firstChar = letter
                                nbFirstChar += 1
                            elif not isFirstChar and letter == firstChar :
                                nbFirstChar -= 1
                            if letter == "(" :
                                nbParenthesis += 1
                            if letter == "," and nbFirstChar == 0 :
                                arrayContent.append(format(contentName.strip()))
                                contentName = ""
                                isFirstChar = True
                            elif letter == ")" :
                                nbParenthesis -= 1
                                if (nbParenthesis == 0) :    
                                    arrayContent.append(format(contentName.strip()))
                                    contentName = ""
                                    isFirstChar = True
                                    arrayConfig.append(arrayContent)
                                    arrayContent = []
                                    arrayAllConfig.append(arrayConfig)
                                    arrayConfig = []
                                    isReturnLine = False
                                else :
                                    contentName += letter
                            elif letter != "\n" :
                                contentName += letter
                        elif letter == "(" :
                            nbParenthesis += 1
                            isConfigName = False
                            isContent = True
                            arrayConfig.append(configName)
                            configName = ""
                            isReturnLine = True
                        elif isConfigName :
                            configName += letter
                        
            if "->" not in line and isReturnLine :
                isFirstChar = True
                for letter in line :
                    if isFirstChar and (letter == "\"" or letter == "\'") :
                        isFirstChar = False
                        firstChar = letter
                        nbFirstChar += 1
                    elif not isFirstChar and letter == firstChar :
                        nbFirstChar -= 1
                    if letter == "(" :
                        nbParenthesis += 1
                    if letter == "," and nbFirstChar == 0 :
                        arrayContent.append(format(contentName.strip()))
                        contentName = ""
                        isFirstChar = True
                    elif letter == ")" :
                        
                        nbParenthesis -= 1
                        if (nbParenthesis == 0) : 
                            arrayContent.append(format(contentName.strip()))
                            contentName = ""
                            isFirstChar = True
                            arrayConfig.append(arrayContent)
                            arrayContent = []
                            arrayAllConfig.append(arrayConfig)
                            arrayConfig = []
                            isReturnLine = False
                        else :
                            contentName += letter
                            
                    elif letter != "\n" :
                        contentName += letter


            # End of configure function
            if "}" in line :
                break

    name = "No name :("
    for iterator in range(len(arrayAllConfig)) :
        if arrayAllConfig[iterator][0] == "setName" :
            name = arrayAllConfig[iterator][1][0]
            arrayAllConfig.pop(iterator)
            break
    return name, arrayAllConfig




if __name__ == "__main__":
    print(getConfig(open("/Users/mnordest/Sites/thelia/core/lib/Thelia/Command/ModuleActivateCommand.php")))
    # print(get_commands(input("Enter the directory to scan: ")))
    ...