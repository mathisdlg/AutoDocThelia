import os, json
from subprocess import Popen, PIPE

# To analyze loop files and generate the documentation associated with the code

def snake_case(name):
    """
    From "ThatString" to "that_string"
    """
    return name[0].lower() + "".join([c if c.islower() else f"_{c.lower()}" for c in name[1::]]).strip()

def CamelCase(name):
    """
    From "that_string" to "ThatString"
    """
    string = ""
    for char in name.split("_"):
        string += char.capitalize()
    return string


def parser(loopFolder: str) -> dict:
    """
    Parse the loop folder to extract the information needed to generate the documentation

    Args:
        loopFolder (str): The path to the loop folder

    Raises:
        Exception: #doc-arg-desc must be followed by an Argument object
        Exception: #doc-out-desc must be followed by an Output object

    Returns:
        dict: the dictionary containing the loop information to generate the documentation wih a specific format which is :
        {"loopFile.php": [Name: str, Desc: str , Args: list[list["Argument", "Type", "Description", "Mandatory", "Default", "Example"]], Outputs: list[list["Name", "Value"]], Orders: list[list["Ascendant", "Descendant", "Sorted field"]], Enums: dict[str, list[str]]]}
    """
    dictLoop = {}
    for loopFile in sorted(os.listdir(loopFolder)):
        if not loopFile.endswith(".php"):
            continue

        with open(os.path.join(loopFolder, loopFile), "r") as file:
            loopTmpDict = {}
            abstract = False
            descBoolean = False
            args = [["Argument", "Type", "Description", "Mandatory", "Default", "Example"]]
            outputs = [["Name", "Value"]]
            orders = [["Ascendant", "Descendant", "Sorted field"]]
            lines = file.readlines()
            for i in range(0, len(lines)):
                line = lines[i]
                if line.startswith("abstract"):
                    abstract = True
                    break
                elif line.startswith("class"):
                    loopTmpDict["Name"] = line.split(" ")[1].strip()
                    snackCaseName = snake_case(loopTmpDict["Name"])
                    if descBoolean:
                        loopTmpDict["Desc"] += '  \n`{loop type="'+snackCaseName+'" name="the-loop-name" [argument="value"], [...]}`'
                    else:
                        loopTmpDict["Desc"] = '`{loop type="'+snackCaseName+'" name="the-loop-name" [argument="value"], [...]}`'
                        descBoolean = True
                elif "#doc-desc" in line:
                    desc = line.split("#doc-desc")[1].strip()
                    if descBoolean:
                        loopTmpDict["Desc"] = desc + "  \n" + loopTmpDict["Desc"]
                    else:
                        loopTmpDict["Desc"] = desc
                        descBoolean = True
                elif "#doc-arg-desc" in line:
                    name = line.split("#doc-arg-desc")[1].strip()
                    nextLine = lines[i+1].strip().replace('"', "'")
                    if "Argument" not in nextLine:
                        raise Exception(f"Error in line {i+1} of {loopFile} : #doc-arg-desc must be followed by an Argument object")

                    if nextLine.endswith("("):
                        searchLine = lines[i+2].strip().replace('"', "'")
                    else:
                        searchLine = nextLine

                    if "Argument::" in nextLine or nextLine.startswith("new"):
                        name = searchLine.split("'")[1]
                    else:
                        raise Exception(f"Error in line {i+1} of {loopFile} : #doc-arg-desc must be followed by an Argument object")
                    args.append([name, "", desc, "", "", ""])
                elif "#doc-out-desc" in line:
                    desc = line.split("#doc-out-desc")[1].strip()
                    if "->set(" not in lines[i+1]:
                        raise Exception(f"Error in line {i+1} of {loopFile} : #doc-out-desc must be followed by an Output object")
                    if lines[i+1].strip().endswith("("):
                        name = lines[i+2].split("'")[1]
                    else:
                        name = lines[i+1].split("'")[1]
                    outputs.append([name, desc])
                        
        if not abstract:
            dictLoop[loopFile] = [loopTmpDict["Name"], loopTmpDict["Desc"], args, outputs, orders, {}] # [Name, Desc, Args, Outputs, Orders, Enums]
    return dictLoop # {"loopFile.php": [Name, Desc, Args, Outputs, Orders, Enums]}

def updateDictWithCommands(loopDict: dict, theliaRoot: str) -> dict:
    """
    Update the loop dictionary with the Matthias commands

    Args:
        loopDict (dict): The dictionary containing the loop information
        theliaRoot (str): The path to the Thelia root

    Returns:
        dict: The updated loop dictionary
    """
    pipes = Popen(["php", os.path.join(theliaRoot, "Thelia"), "loop:info", "--all"], stdout=PIPE, stderr=PIPE)
    commands, _ = pipes.communicate()
    pipes.kill()
    json_data = json.loads(commands)
    for loopKey in list(json_data.keys()):
        if "-" in loopKey:
            loopKeyModified = loopKey.replace("-", "_")
            json_data[loopKeyModified] = json_data.pop(loopKey)

    for loop in loopDict.keys():
        jsonLoopTmp = json_data[snake_case(loop[0:-4])]
        if jsonLoopTmp["warning"] != "" and jsonLoopTmp["warning"] != None:
            loopDict[loop][1] = "Warning:" + jsonLoopTmp["warning"] + "  \n" + loopDict[loop][1]

        # args = [["Argument", "Type", "Description", "Mandatory", "Default", "Example"]]
        argList = [ arg[0] for arg in loopDict[loop][2] ]
        if "args" not in jsonLoopTmp:
            continue
        
        extend = snake_case(jsonLoopTmp["extends"].split("\\")[-1])
        argsOfExtend = []
        if extend in json_data:
            loopDict[loop][1] += f"  \nThis loop is an extend of [{extend}](./{CamelCase(extend)}) loop."
            argsOfExtend = [arg[0] for arg in json_data[extend]["args"]]

        for arg in jsonLoopTmp["args"]:
            if arg in argList:
                index = argList.index(arg)

                if arg in argsOfExtend:
                    del loopDict[loop][2][index]
                    continue

                loopDict[loop][2][index][1] = jsonLoopTmp["args"][arg][0]

                if jsonLoopTmp["args"][arg][1] == None:
                    loopDict[loop][2][index][3] = ""
                else:
                    loopDict[loop][2][index][3] = jsonLoopTmp["args"][arg][1]

                if jsonLoopTmp["args"][arg][2] == None:
                    loopDict[loop][2][index][4] = ""
                else:
                    loopDict[loop][2][index][4] = jsonLoopTmp["args"][arg][2]

                loopDict[loop][2][index][5] = jsonLoopTmp["args"][arg][3]
        
        # orders = [["Ascendant", "Descendant", "Sorted field"]]
        if "enums" not in jsonLoopTmp:
            continue

        for enum in jsonLoopTmp["enums"]:
            if enum == "order":
                for order in jsonLoopTmp["enums"]["order"]:
                    loopDict[loop][4].append([order[0], order[1], ""])
            else:
                loopDict[loop][5][enum] = [[enum]] # To do table for enums with the generate section function
                for enumValue in jsonLoopTmp["enums"][enum]:
                    if enumValue in loopDict[loop][5][enum]:
                        continue
                    loopDict[loop][5][enum].append(enumValue)

    return loopDict


def generate_section(title, data):
    section_content = ""
    
    # check if the section is empty
    if not data:
        return section_content

    section_content += f"\n## {title}\n\n"

    # check if the first element is a list to determine the section type
    if isinstance(data[0], list):
        # displays data in tabular form

        # get column titles
        column_titles = data[0]
        # construct column titles line
        section_content += "|"
        for col_title in column_titles:
            section_content += f" {col_title} |"
        section_content += "\n"
        # construct separation line
        section_content += "|"
        for _ in column_titles:
            section_content += "-----------------|"
        section_content += "\n"
        
        # iterate through data to generate table rows
        for item in data[1:]:
            # exclude values at the end of sub-tables if they are not of list type
            if isinstance(item, list):
                section_content += "|"
                for value in item:
                    section_content += f" {value} |"
                section_content += "\n"

        # add values retrieved below the table, if they exist
        if not isinstance(data[-1], list):
            section_content += f"\n{data[-1]}\n"

    else:
        # generate list type section
        for item in data:
            section_content += f"* {item}\n"

    return section_content


def copy_examples_section(file_content):
    # find the position of the title "Examples"
    examples_index = file_content.find("## Example")
    if examples_index == -1:
        return None
    # find the position of the next title after "Examples"
    next_title_index = file_content.find("##", examples_index + 1)
    if next_title_index == -1:
        next_title_index = len(file_content)
    # copy the content between "Examples" and the next title
    examples_content = file_content[examples_index:next_title_index]
    
    # Remove trailing newline characters
    examples_content = examples_content.rstrip('\n')
    
    return examples_content + '\n'



def generate_markdown(data, output_path=None):
    title, description, arguments, outputs, orders, enums = data

    # read the content of the Markdown file and retrieve "Example" if they exist
    try:
        with open(f"{title.replace(' ', '_')}.md", "r") as file:
            file_content = file.read()
    except FileNotFoundError:
        file_content = ""

    examples_content = copy_examples_section(file_content)

    # create the title and description
    content = f"# {title}\n\n" + description + "\n"

    # create the first sections
    content += generate_section("Arguments", arguments)
    content += generate_section("Output", outputs)

    # add the "Examples" section copied from the file if it exists
    if examples_content:
        content = content + "\n" + examples_content
    
    if len(enums) > 0:
        for enum in enums:
            content += generate_section(enum, enums[enum])

    if len(orders) > 1:
        content += generate_section("Orders", orders)

    # determine the output file path
    if output_path:
        # create the directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_file_path = f"{output_path}/{title.replace(' ', '_')}.md"
    else:
        output_file_path = f"{title.replace(' ', '_')}.md"

    # write to the Markdown file
    with open(output_file_path, "w") as file:
        file.write(content)

def main(theliaRoot, loopDoc="output"):
    loopFolder = os.path.join(theliaRoot, "core/lib/Thelia/Core/Template/Loop/")
    
    loopDict = updateDictWithCommands(parser(loopFolder), theliaRoot)

    for loopFile in loopDict.values():
        generate_markdown(loopFile, loopDoc)

if __name__ == "__main__":
    theliaRoot = "thelia"
    
    main(theliaRoot)