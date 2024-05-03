from io import TextIOWrapper
import os
import asyncio




def printAndStop(things: any) -> None:
    """Prints the things and stops the program

    Args:
        things (any): The things to print
    """
    print(things)
    input("Press enter to continue")


async def getCommands(directory: str) -> dict[str: list[list[str, list[str]]]]:
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
        tasks = []

        for fileIndex in fileList:
            tasks.append(asyncio.create_task(matchGetFileConfig(fileIndex, commands, fileList, listExtends, directory)))
        
        for task in tasks:
            await task
            commandAddedOrExtendsAdded = commandAddedOrExtendsAdded or task.result()

    return commands

async def matchGetFileConfig(fileIndex: list[str], commands: dict[str: list[list[str, list[str]]]], fileList: list[str], listExtends: list[str], directory: str) -> bool:
    match await getFileConfig(fileIndex, commands, fileList, listExtends, directory):
        case 0:
            return True
        case 1:
            return True
        case 2:
            return False
    return False


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


async def getFileConfig(fileIndex: list[str], commands: dict[str: list[list[str, list[str]]]], fileList: list[str], listExtends: list[str], directory: str) -> int:
    """Get the config of the file

    Args:
        fileIndex (list[str]): the path of the file and the index of the extends
        commands (dict): the commands dictionnary
        fileList (list[str]): the list of all possible commands files
        listExtends (list[str]): the list of the extends

    Returns:
        int: 0 if the command has been added, 1 if the extends has been added, 2 if the command has not been added
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
                        name = getCommandName(f)
                        stdout, retCode = await launchCommand(name, directory)
                        if retCode:
                            fileList.remove(fileIndex)
                            return 2

                        config = await parseFile(stdout)
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


def getCommandName(file: TextIOWrapper) -> str :
    # To get the command name
    
    # Define if the letter we are analyzing is part of the command name
    isCommandName = False
    
    commandName = ""
    
    for line in file :
        # Research of the line were the command name is set
        if "->setName" in line :
            # To get only the name field
            lineForParsing = line.strip().split("->setName")
            for letter in lineForParsing[1] :
                # Begin og the command name
                if letter == "(" :
                    isCommandName = True
                    continue
                # End of the command name
                if letter == ")" :
                    isCommandName = False
                    break
                if isCommandName and letter != " " and letter != "\n" :
                    commandName += letter
        # If the command name is write on many lines
        elif isCommandName :
            for letter in line :
                if letter == "(" :
                    isCommandName = True
                    continue
                if letter == ")" :
                    isCommandName = False
                    break
                if isCommandName and letter != " " and letter != "\n" :
                    commandName += letter

    return format(commandName.strip()).strip()


async def launchCommand(name: str, repository: str) -> bytes:
    absPath = os.path.abspath(repository)
    process = await asyncio.create_subprocess_exec(f"php",  f"{absPath}/Thelia", name, "--help", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    pipes = await process.communicate()

    return pipes[0], process.returncode
    


async def parseFile(stdout: bytes) -> list[str, str, list[list[str, str]], list[list[str, str]]] :
    isDescription = False
    isUsage = False
    isArgument = False
    isOption = False
    isHelp = False
    arrayCommand = ["", "", [], []]

    buf = stdout.decode("utf-8").split("\n")

    for line in buf:
        if isDescription :
            arrayCommand[0] = line.strip()
            isDescription = False
        elif line == "Description:" :
            isDescription = True
            
        if isUsage :
            arrayCommand[1] = line.strip()
            isUsage = False
        elif line == "Usage:" :
            isUsage = True
            
        if isArgument :
            if line != "" :
                arrayCommand[2].append(argumentAnalyzer(line))
            else :
                isArgument = False
        elif line == "Arguments:" :
            isArgument = True
            
        if isOption :
            if line != "" :
                if "-h, --help" in line or "-q, --quiet" in line or "-V, --version" in line or "--ansi|--no-ansi" in line or "-n, --no-interaction" in line or "-e, --env=ENV" in line or "--no-debug" in line or "-v|vv|vvv, --verbose" in line :
                    continue
                else :
                    arrayCommand[3].append(optionAnalyzer(line))
            else :
                isOption = False
        elif line == "Options:" :
            isOption = True
            
        if isHelp :
            arrayCommand.append(line.strip())
            isHelp = False
        elif line == "Help:" :
            isHelp = True
    return arrayCommand


def argumentAnalyzer(line: str) -> list[str, str] :
    arrayArguments = []
    lineAnalyzed = line.split(" ")
    while "" in lineAnalyzed :
        lineAnalyzed.remove("")
    arrayArguments.append(lineAnalyzed[0])
    lineAnalyzed.pop(0)
    arrayArguments.append(" ".join(lineAnalyzed).strip())
    return arrayArguments


def optionAnalyzer(line: str) -> list[str, str] :
    arrayOptions = []
    lineAnalyzed = line.split(" ")
    while "" in lineAnalyzed :
        lineAnalyzed.remove("")
    if "," in lineAnalyzed[0] :
        arrayOptions.append(lineAnalyzed[0] + " " + lineAnalyzed[1])
        lineAnalyzed.pop(0)
        lineAnalyzed.pop(0)
    else :
        arrayOptions.append(lineAnalyzed[0])
        lineAnalyzed.pop(0)
    arrayOptions.append(" ".join(lineAnalyzed).strip())
    return arrayOptions


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
            if dictValue[2]:
                f.write("## Argument\n\n")
                for arg in dictValue[2]:
                    f.write(f"* `{arg[0]}`: {arg[1]}\n")
                f.write("\n")
            
            # write options
            if dictValue[3]:
                f.write("## Option\n\n")
                for option in dictValue[3]:
                    f.write(f"* `{option[0]}`: {option[1]}\n")
                f.write("\n")
            
            # write help if available
            if len(dictValue) > 4 and dictValue[4]:
                f.write("## Help\n\n")
                f.write(f"{dictValue[4]}")
    
    # markdown layout (spaces)
    with open(file_name, "r+") as f:
        content = f.read().rstrip() + "\n"
        f.seek(0)
        f.write(content)
        f.truncate()

    return "Markdown file(s) was/were created successfully ✅" 


def main(directory: str, output: str = "./output/") -> None:
    """Main function to get the directory and output directory and create the markdown file(s) from the commands in the directory
    """
    if output == "":
        output = "./output/"
    dictionnary = asyncio.run(getCommands(directory))
    print(generate_markdown_files(dictionnary, output))


if __name__ == "__main__":
    directory = input("Enter the directory to scan commands: ")
    output = input("Enter the output directory for commands [./ouput/]: ")

    main(directory, output)