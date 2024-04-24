from io import TextIOWrapper
import os

def get_commands(directory: str, listExtends: list[str] = ["ContainerAwareCommand"]) -> dict:
    commands = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith(".php") and not "vendor" in path:
                with open(path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if (line.startswith("class") or line.startswith("abstract")):
                            index = line.find("extends")
                            if index != -1:
                                extends = line[index + len("extends"):] if not line.endswith("{") else line[index + len("extends"):line.index("{")].strip()
                                if line.startswith("class") and extends in listExtends:
                                    name, config = getConfig(f)
                                    commands[name] = config
                                elif line.startswith("abstract") and extends in listExtends:
                                    listExtends.append(line[line.index("abstract class ") + len("abstract class "):index].strip())
    return commands

def scan_file(fileName: str, listExtends: list[str]) -> dict:
    ...          


def getConfig(file: TextIOWrapper) -> tuple[str, list[list[str, list[str]]]] :
    # (Name,[["setDescription", ["This command do this"]], ["addOption", ["option1", "option2"]], ["addArgument", ["argument1", "argument2"]]])  : arrayAllConfig
    #        |------------------------------------------|  |-----------------------------------|   : arrayConfig
    #                           |----------------------|                 |--------------------|    : arrayContent
    arrayAllConfig = []
    arrayConfig = []
    arrayContent = []
    header = True
    isConfigName = False
    isContent = False
    isArrow = False
    isNewConfig = False
    nbParentesis = 0
    isReturnLine = False
    name = ""
    configName = ""
    contentName = ""

    for line in file:
        if header :
            if "function configure" in line :
                # Begin of configure function
                header = False
        else:
            
            #parentesisCounter = line.count("(")
            #if parentesisCounter > 0:
            #    if parentesisCounter - line.count(")") == 1: # $this->setName("hello:world") without "->setDescription("output hello world");

            #    if parentesisCounter - line.count(")") == 0: # $this->setName("hello:world")->setDescription("output hello world");

            if "->" in line and nbParentesis == 0 :
                listElements = line.split("->")
                for iterator in range(1, len(listElements)) :
                    isConfigName = True
                    isContent = False
                    for letter in listElements[iterator] :
                        if isContent :
                            if letter == "," :
                                arrayContent.append(contentName)
                                contentName = ""
                            elif letter == ")" :
                                arrayContent.append(contentName)
                                contentName = ""
                                arrayConfig.append(arrayContent)
                                isReturnLine = False
                            elif letter != "\n" :
                                contentName += letter
                        elif letter == "(" :
                            isConfigName = False
                            isContent = True
                            arrayConfig.append(configName)
                            configName = ""
                            isReturnLine = True
                        elif isConfigName :
                            configName += letter
            if "->" not in line and isReturnLine :
                contentName = ""
                for letter in line :
                    if letter == "," :
                        arrayContent.append(contentName)
                    elif letter == ")" :
                        arrayConfig.append(arrayContent)
                        isReturnLine = False
                    else :
                        contentName += letter


           
                    ...
            # End of configure function
            if "}" in line :
                break
            ...

            #     
            #         
            #         
                    
            #     if isConfigName :
            #         result += letter
            #     elif letter == "(" :
            #         isConfigName = True
    







if __name__ == "__main__":
    # print(get_commands(input("Enter the directory to scan: ")))
    ...