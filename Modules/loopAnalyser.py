import os

# To analyze loop files and generate the documentation associated with the code

def parser(loopFolder):
    dictLoop = {}
    for loopFile in sorted(os.listdir(loopFolder)):
        if loopFile.endswith(".php"):
            with open(os.path.join(loopFolder, loopFile), "r") as file:
                loopTmpDict = {}
                abstract = False
                args = [["Argument", "Description", "Default", "Example"]]
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
                    elif "#doc-usage" in line:
                        if loopTmpDict.get("Desc") is None:
                            loopTmpDict["Desc"] = "`"+line.split("#doc-usage")[1].strip()+"`"
                        else:
                            loopTmpDict["Desc"] += "  \n"+"`"+line.split("#doc-usage")[1].strip()+"`"
                    elif "#doc-desc" in line:
                        desc = line.split("#doc-desc")[1].strip()
                        if loopTmpDict.get("Desc") is None:
                            loopTmpDict["Desc"] = desc
                        else:
                            loopTmpDict["Desc"] = desc+"  \n"+loopTmpDict["Desc"]
                    elif "#doc-arg-name" in line:
                        name = line.split("#doc-arg-name")[1].strip()
                        desc = ""
                        default = ""
                        example = ""
                        for x in range(1, 4):
                            nextLine = lines[i+x]
                            if "*/" in nextLine or nextLine.strip().split("*")[1].strip() == "":
                                break
                            match nextLine.strip().split(" ")[1]: # TODO
                                case "#doc-arg-desc":
                                    desc = nextLine.split("#doc-arg-desc")[1].strip()
                                case "#doc-arg-default":
                                    default = nextLine.split("#doc-arg-default")[1].strip()
                                case "#doc-arg-example":
                                    example = nextLine.split("#doc-arg-example")[1].strip()
                        args.append([name, desc, default, example])
                    elif "#doc-out-name" in line:
                        name = line.split("#doc-out-name")[1].strip()
                        value = lines[i+1].split("#doc-out-desc")[1].strip()
                        outputs.append([name, value])
                            
            if not abstract:
                dictLoop[loopFile] = [loopTmpDict["Name"], loopTmpDict["Desc"], args, outputs, orders]
    return dictLoop


def getFromCommand():
    ...


def generate_section(title, data):
    section_content = f"\n## {title}\n\n"

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
    title, description, arguments, outputs, orders = data

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

def main(loopFolder, loopDoc):
    print("This is a test version of the loop documentation generator.")
    for loopFile in parser(loopFolder).values():
        generate_markdown(loopFile, loopDoc)

if __name__ == "__main__":
    loopFolder = "thelia/core/lib/Thelia/Core/Template/Loop/"
    for loopFile in parser(loopFolder).values():
        generate_markdown(loopFile, "output")