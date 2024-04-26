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
    
    os.remove(".tmpCmdHelp")

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
                        name = getCommandName(f)
                        launchCommand(name, fileIndex[0])
                        config = parseFile()
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
                if letter == ")" :
                    isCommandName = False
                    break
                if isCommandName and letter != " " and letter != "\n" :
                    commandName += letter

    return format(commandName.strip()).strip()


def launchCommand(name: str, repository: str) -> str :
    os.system(f"php {repository}/Thelia {name} --help 2> .tmpCmdHelp > .tmpCmdHelp")


def parseFile() -> list[str, str, list[list[str, str]], list[list[str, str]]] :
    isDescription = False
    isUsage = False
    isArgument = False
    isOption = False
    isHelp = False
    arrayCommand = ["", "", [], []]
    fileOpened = open(".tmpCmdHelp", "r")
    for line in fileOpened :
        if isDescription :
            arrayCommand[0] = line.strip()
            isDescription = False
        elif line == "Description:\n" :
            isDescription = True
            
        if isUsage :
            arrayCommand[1] = line.strip()
            isUsage = False
        elif line == "Usage:\n" :
            isUsage = True
            
        if isArgument :
            if line != "\n" :
                arrayCommand[2].append(argumentAnalyzer(line))
            else :
                isArgument = False
        elif line == "Arguments:\n" :
            isArgument = True
            
        if isOption :
            if line != "\n" :
                if "-h, --help" in line or "-q, --quiet" in line or "-V, --version" in line or "--ansi|--no-ansi" in line or "-n, --no-interaction" in line or "-e, --env=ENV" in line or "--no-debug" in line or "-v|vv|vvv, --verbose" in line :
                    continue
                else :
                    arrayCommand[3].append(optionAnalyzer(line))
            else :
                isOption = False
        elif line == "Options:\n" :
            isOption = True
            
        if isHelp :
            arrayCommand.append(line.strip())
            isHelp = False
        elif line == "Help:\n" :
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


def format_title(title: str) -> str:
    """Formats the title to ensure it starts with '## ' and includes only the first uppercase letters

    Args:
        title (str): The title to format

    Returns:
        str: The formatted title
    """
    # formats the title to ensure it starts with '## ' and includes only the first uppercase letters
    formatted_title = "## "
    found_upper = False
    used_words = set()
    for char in title:
        if char.isupper():
            found_upper = True
            formatted_title += char
        elif found_upper:
            if char.isalpha() and char.lower() not in used_words:
                used_words.add(char.lower())
                formatted_title += char
    return formatted_title + "\n\n" 


def format_option(option: list[str]) -> str:
    """Formats the option by filtering out 'null' and 'InputOption' parameters

    Args:
        option (list[str]): The option to format

    Returns:
        str: The formatted option
    """
    first_param = option[0]
    if isinstance(first_param, list):
        first_param = ' '.join(first_param)
    if 'InputOption' in first_param:
        return ' '.join(option)
    filtered_option = [param for param in option[1:] if 'null' not in param and 'InputOption' not in param]
    if not filtered_option:
        return ''
    return ' '.join(filtered_option)


def format_argument(argument: list[str]) -> str:
    """Formats the argument by filtering out 'null' and 'InputArgument' parameters

    Args:
        argument (list[str]): The argument to format

    Returns:
        str: The formatted argument
    """
    first_param = argument[0]
    if isinstance(first_param, list):
        first_param = ' '.join(first_param)
    if 'InputArgument' in first_param:
        return ' '.join(argument)
    filtered_argument = [param for param in argument[1:] if 'null' not in param and 'InputArgument' not in param]
    if not filtered_argument:
        return ''
    return ' '.join(filtered_argument)


def create_markdown_from_dict(data_dict: dict[str: str|list[list[str, list[str]]]], path: str="output") -> str:
    """Creates markdown file(s) from the dictionary

    Args:
        data_dict (dict): the dictionary containing the command names and their respective configurations
        path (str, optional): The path to save the markdown file(s). Defaults to "output".

    Returns:
        str: The message indicating the markdown file(s) was/were created successfully
    """

    for name, items in data_dict.items():
        formatted_str = ""
        has_option = False
        arguments = []
        prev_title = None 

        # Title1 section
        formatted_str += f"# {name.lower()}\n\n"

        # description section
        description = ""
        help_section = ""
        for item in items:
            if item[0].lower() == 'setdescription':
                description += format_title(item[0]) + ' '.join(item[1]) + "\n\n"
            elif item[0].lower() == 'sethelp':
                help_section += f"## Help\n\n{' '.join(item[1])}\n\n"

        # combine description and help sections
        description += help_section

        # option and Argument sections
        option_and_desc = ""
        for item in items:
            if item[0].startswith('addOption'):
                has_option = True
                option_title = 'Option'
                if prev_title != option_title:
                    option_and_desc += f"## {option_title}\n\n" 
                option_and_desc += f"- `{item[1][0]}` {format_option(item[1])}\n\n"
                prev_title = option_title
            elif item[0].startswith('addArgument'):
                argument_title = 'Argument'
                if prev_title != argument_title:
                    option_and_desc += f"## {argument_title}\n\n"
                option_and_desc += f"- `{item[1][0]}` {format_argument(item[1])}\n\n"
                prev_title = argument_title
                arguments.append(item[1][0])

        # usage section
        usage = ""
        if description:
            first_line = name.lower()
            if len(first_line) > 1:
                usage = f"## Usage\n\n```bash\n{first_line} "
                if has_option:
                    usage += "[option(s)] "
                if arguments:
                    usage += ' '.join([f"<{arg}>" for arg in arguments])
                usage += "\n```\n\n"

        formatted_str += description + usage + option_and_desc

        # example section
        bash_code = f"php Thelia {name} ..." 
        formatted_str += "## Example\n\n" + f"```bash\n{bash_code}\n```\n\n"
        filename = name.replace(':','_') + ".md"

        if path:
            filename = os.path.join(path, filename)
        if not os.path.exists(path):
            os.makedirs(path)

        with open(filename, 'w') as f:
            f.write(formatted_str.rstrip() + "\n")

    return f"Markdown file(s) was/were created successfully ✅"



def main() -> None:
    """Main function to get the directory and output directory and create the markdown file(s) from the commands in the directory
    """
    directory = input("Enter the directory to scan commands: ")
    output = input("Enter the output directory for commands [./ouput/]: ")
    if output == "":
        output = "./output/"
    dictionnary = getCommands(directory)
    print(create_markdown_from_dict(dictionnary, output))


if __name__ == "__main__":
    main()