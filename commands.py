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
                        name, config = getConfig(f)
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



def format_title(title):
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


def format_option(option):
    # formats the option by filtering out 'null' and '::' parameters
    first_param = option[0]
    if isinstance(first_param, list):
        first_param = ' '.join(first_param)
    if '::' in first_param:
        return ' '.join(option)
    filtered_option = [param for param in option[1:] if 'null' not in param and '::' not in param]
    if not filtered_option:
        return ''
    return ' '.join(filtered_option)


def format_argument(argument):
    # formats the argument by filtering out 'null' and '::' parameters
    first_param = argument[0]
    if isinstance(first_param, list):
        first_param = ' '.join(first_param)
    if '::' in first_param:
        return ' '.join(argument)
    filtered_argument = [param for param in argument[1:] if 'null' not in param and '::' not in param]
    if not filtered_argument:
        return ''
    return ' '.join(filtered_argument)


def create_markdown_from_dict(data_dict):
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
                option_and_desc += f"`{item[1][0]}` {format_option(item[1])}\n\n"
                prev_title = option_title
            elif item[0].startswith('addArgument'):
                argument_title = 'Argument'
                if prev_title != argument_title:
                    option_and_desc += f"## {argument_title}\n\n"
                option_and_desc += f"`{item[1][0]}` {format_argument(item[1])}\n\n"
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
        with open(filename, 'w') as f:
            f.write(formatted_str)

    return f"Markdown file(s) was/were created successfully ✅"




if __name__ == "__main__":
    dictionnary = getCommands(input("Enter the directory to scan: "))