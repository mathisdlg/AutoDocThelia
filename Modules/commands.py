from io import TextIOWrapper
import os



def printAndStop(things: any) -> None:
    """Prints the things and stops the program

    Args:
        things (any): The things to print
    """
    print(things)
    input("Press enter to continue")


def getCommands(directory: str) -> dict[str: list[list[str, list[str]]]]:
    """Get all the commands in the directory

    Args:
        directory (str): The directory to scan

    Returns:
        dict: The commands with the name as key and the config as value
    """
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
    """Check if the file can be a command (if it extends something o not)

    Args:
        path (str): The path of the file

    Returns:
        int: The index of the extends or -1 if it does not extend anything
    """
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if (line.startswith("class") or line.startswith("abstract")):
                indexExtends = line.find("extends")
                return indexExtends
    return -1


def getFileConfig(fileIndex: list[str], commands: dict[str: list[list[str, list[str]]]], fileList: list[str], listExtends: list[str]) -> int:
    """Get the config of the file

    Args:
        fileIndex (list[str]): the path of the file and the index of the extends
        commands (dict): the commands dictionnary
        fileList (list[str]): the list of all possible commands files
        listExtends (list[str]): the list of the extends

    Returns:
        int: 0 if the command has been added, 1 if the extends has been added
    """
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
                        name, config = getConfig(f)
                        commands[name] = config
                    listExtends.append(line[line.index("class ") + len("class "):indexExtends].strip())
                    fileList.remove(fileIndex)
                    return 0 if isClass else 1


def format(sequence: str) -> str :
    """Format the sequence with the right format (remove the first and last character if they are " or ')

    Args:
        sequence (str): The sequence to format

    Returns:
        str: The formatted sequence
    """
    if sequence[-1] in {"\'", "\""} and sequence[0] in {"\'", "\""} :
        sequence = sequence[:-1]
        sequence = sequence[1:]
    return sequence


def getConfig(file: TextIOWrapper) -> tuple[str, list[list[str, list[str]]]] :
    """Analyse configure function in the file

    Args:
        file (TextIOWrapper): The file to analyse

    Returns:
        tuple[str, list[list[str, list[str]]]]: The name of the command and the config
    """

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
                            if letter == "," and nbFirstChar == 0 and nbParenthesis < 2 :
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
                        if nbFirstChar == 0 :
                            isFirstChar = True
                    if letter == "(" :
                        nbParenthesis += 1
                    if letter == "," and nbFirstChar == 0 and nbParenthesis < 2 :
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



def generate_markdown_files(data_command_dict, output_path="."):
    """
        function that generates as many markdown files as there are keys in the dictionary

        Args: data_command_dict -> a dictionary that contains every command's informations
              output_path -> optional argument which is the path where then markdown file(s) will be created

        Return: a string if everything went well
    """
    # Créer le répertoire de sortie s'il n'existe pas
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for dictKey, dictValue in data_command_dict.items():
        file_name = os.path.join(output_path, dictKey+".md")
        #file_name = f"{output_path}/{dictKey}.md"
        with open(file_name, "w") as f:
            # Write title with docusaurus
            f.write(f"---\ntitle: {dictKey}\n---\n\n")

            # write description
            f.write(f"{dictValue[0]}\n\n")
            
            # write usage
            f.write("## Usage\n\n")
            f.write(f"`{dictValue[1]}`\n\n")
            
            # write arguments
            f.write("## Argument\n\n")
            for arg in dictValue[2]:
                f.write(f"* `{arg[0]}`: {arg[1]}\n")
            f.write("\n")
            
            # write options
            f.write("## Option\n\n")
            for option in dictValue[3]:
                f.write(f"* `{option[0]}`: {option[1]}\n")
            f.write("\n")
            
            # write help if available
            if len(dictValue) > 4:
                f.write("## Help\n\n")
                f.write(f"{dictValue[4]}\n")

    return "Markdown file(s) was/were created successfully ✅"      



def main(directory: str, output: str = "./output/") -> None:
    """Main function to get the directory and output directory and create the markdown file(s) from the commands in the directory
    """
    if output == "":
        output = "./output/"
    dictionnary = getCommands(directory)
    print(create_markdown_from_dict(dictionnary, output))



if __name__ == "__main__":
    directory = input("Enter the directory to scan commands: ")
    output = input("Enter the output directory for commands [./ouput/]: ")
    main(directory, output)