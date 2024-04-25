from io import TextIOWrapper
import os

def printAndStop(things: any) -> None:
    print(things)
    input("Press enter to continue")

def getCommands(directory: str) -> dict:
    fileList = []
    listExtends = ["ContainerAwareCommand"]

    commandAddedOrExtendsAdded = True

    commands = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith(".php") and not "vendor" in path:
                index = canBeACommand(path)
                if index > 0:
                    fileList.append([path, index])

    while commandAddedOrExtendsAdded:
        commandAddedOrExtendsAdded = False
        for fileIndex in fileList:
            match getFileConfig(fileIndex, commands, fileList, listExtends):
                case 0:
                    commandAddedOrExtendsAdded = True
                case 1:
                    commandAddedOrExtendsAdded = True

    return commands


def canBeACommand(path: str) -> int:
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if (line.startswith("class") or line.startswith("abstract")):
                indexExtends = line.find("extends")
                return indexExtends
    return False


def getFileConfig(fileIndex: str, commands: dict[str: list[list[str, list[str]]]], fileList: list[str], listExtends: list[str]) -> int:
    with open(fileIndex[0], "r") as f:
        isClass = False
        for line in f:
            line = line.strip()
            if (line.startswith("class") or line.startswith("abstract")):
                indexExtends = fileIndex[1]
                extends = (line[indexExtends + len("extends"):] if not line.endswith("{") else line[indexExtends + len("extends"):line.index("{")]).strip()
                if extends in listExtends:
                    if line.startswith("class"):
                        isClass = True
                        name, config = fileIndex[0], fileIndex[1] #getConfig(f)
                        commands[name] = config
                    listExtends.append(line[line.index("class ") + len("class "):indexExtends].strip())
                    fileList.remove(fileIndex)
                    return 0 if isClass else 1


def format(sequence: str) -> str :
    if sequence[-1] in {"\'", "\""} and sequence[0] in {"\'", "\""} :
        sequence = sequence[:-1]
        sequence = sequence[1:]
    return sequence


def getConfig(file: TextIOWrapper) -> tuple[str, list[list[str, list[str]]]] :
    #dict[name] = [["setDescription", ["...
    #tuple_data = ("Name", [["setDescription", ["This command do this"]], ["addOption", ["nameOption1", "null", "InputOption::VALUE_REQUIRED", "blabla_opt2"]], ["addOption", ["option2", "InputOption::VALUE_REQUIRED", "blabla_opt4"]], ["addArgument", ["argument1", "InputArgument::OPTIONAL", "description1"]], ["addArgument", ["argument2", "InputArgument::OPTIONAL", "description2"]]])

    # (Name,[["setDescription", ["This command do this"]], ["addOption", ["option1", "option2"]], ["addArgument", ["argument1", "argument2"]]])  : arrayAllConfig
    #        |------------------------------------------|  |-----------------------------------|   : arrayConfig
    #                           |----------------------|                 |--------------------|    : arrayContent
    arrayAllConfig = []
    arrayConfig = []
    arrayContent = []
    header = True
    isConfigName = False
    isContent = False
    nbParentesis = 0
    isReturnLine = False
    configName = ""
    contentName = ""

    for line in file:
        if header :
            if "function configure" in line :
                # Begin of configure function
                header = False
        else:

            if "->" in line and nbParentesis == 0 :
                listElements = line.split("->")
                
                for iterator in range(1, len(listElements)) :
                    isConfigName = True
                    isContent = False
                    for letter in listElements[iterator] :
                        if isContent :
                            if letter == "(" :
                                nbParentesis += 1
                            if letter == "," :
                                arrayContent.append(format(contentName.strip()))
                                contentName = ""
                            elif letter == ")" :
                                nbParentesis -= 1
                                if (nbParentesis == 0) :    
                                    arrayContent.append(format(contentName.strip()))
                                    contentName = ""
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
                            nbParentesis += 1
                            isConfigName = False
                            isContent = True
                            arrayConfig.append(configName)
                            configName = ""
                            isReturnLine = True
                        elif isConfigName :
                            configName += letter
                        
            if "->" not in line and isReturnLine :
                for letter in line :
                    if letter == "(" :
                        nbParentesis += 1
                    if letter == "," :
                        arrayContent.append(format(contentName.strip()))
                        contentName = ""
                    elif letter == ")" :
                        
                        nbParentesis -= 1
                        if (nbParentesis == 0) : 
                            arrayContent.append(format(contentName.strip()))
                            contentName = ""
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
                for config in arrayAllConfig :
                    if config[0] == "setDescription" :
                        config[1] = " ".join(config[1])
                        break
                break

    name = "No name :("
    for iterator in range(len(arrayAllConfig)) :
        if arrayAllConfig[iterator][0] == "setName" :
            name = arrayAllConfig[iterator][1][0]
            arrayAllConfig.pop(iterator)
            break
    return name, arrayAllConfig



if __name__ == "__main__":
    # print(getConfig(open("/Users/mdelage/Sites/thelia/core/lib/Thelia/Command/ModuleActivateCommand.php")))
    print(len(getCommands(input("Enter the directory to scan: ")).keys()))
    ...