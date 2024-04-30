# To analyze loop files and generate the documentation associated with the code

def parser() :
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



def generate_markdown(data):
    title, description, arguments, outputs, orders = data

    # read the content of the Markdown file and retrieve "Example" if they exist
    try:
        with open(f"{title.replace(' ', '_')}.md", "r") as file:
            file_content = file.read()
    except FileNotFoundError:
        file_content = ""

    examples_content = copy_examples_section(file_content)


    # create the title and description
    content = f"# {title}\n\n" + '`{' + f'loop type="{title}" name="the-loop-name" [argument="value"], [...]' + '}`\n'

    # create the first sections
    content += generate_section("Arguments", arguments)
    content += generate_section("Output", outputs)

    # add the "Examples" section copied from the file if it exists
    if examples_content:
        content = content + "\n" + examples_content

    content += generate_section("Orders", orders)

    # write to the Markdown file
    with open(f"{title.replace(' ', '_')}.md", "w") as file:
        file.write(content)
