import re, sys, os



def get_hooks(directory: str, file: str) -> None:
    """
    This function allow you to get all the hooks in the html files of a directory and write them in a file.

    Args:
        directory (str): The directory to scan
        file (str): The file to write the hooks in
    """
    # regex to find all the hooks in the html files
    regex: re.Pattern = re.compile("{((hook name)|(hookblock))(.)*")

    if not os.path.exists(directory):
        print("The directory does not exist.")
        raise FileNotFoundError

    if not directory.startswith("./"):
        print("The directory path must start with ./")
        raise ValueError

    with open(file, "w") as f:
        # walk through the directory
        for root, dirs, files in os.walk(directory):
            # for each file in the directory
            for file in files:
                # if the file is an html file
                filepath = root+"/"+file
                if filepath.endswith(".html"):
                    with open(filepath, "r") as openFile:
                        writable = False
                        toWrite = f"{filepath}\n"
                        # for each line in the file
                        for line in openFile.readlines():
                            # if the line contains a hook and is not a comment (line ending with *})
                            if regex.search(line) and not line[-3:-1] == "*}":
                                # get the hook and write it in the file
                                hook = line.strip().split(" ", 1)[1].replace("=", ":").replace("\"", "").replace(",", "|").replace("\n", "").replace(" ", ",")[0:-1]
                                writable = True
                                toWrite += f"\t{hook}\n"
                        if writable:
                            f.write(toWrite)


def get_from_logs(file: str) -> dict:
    """
    This function get the hooks from the logs file and return them in a dictionary

    Args:
        file (str): The file to read the hooks from

    Returns:
        dict: The dictionary of hooks
    """
    if not os.path.exists(file):
        print("The file does not exist.")
        raise FileNotFoundError

    with open(file, "r") as f:
        listOfHooks = {}
        # for each line in the file
        for line in f.readlines():
            line = line.strip()
            # if the line starts with a dot, it is a key
            if line.startswith("."):
                lineSplit = line.lower().split("/")
                office = lineSplit[lineSplit.index("templates")+1].capitalize()
                theme = lineSplit[lineSplit.index("templates")+2].capitalize()
                key = lineSplit[-1]

                if office not in listOfHooks.keys():
                    listOfHooks[office] = {}
                if theme not in listOfHooks[office].keys():
                    listOfHooks[office][theme] = {}
                if key not in listOfHooks[office][theme].keys():
                    listOfHooks[office][theme][key] = []
            # if the line does not start with a dot, it is a hook
            else:
                if key not in listOfHooks[office][theme].keys():
                    listOfHooks[office][theme][key] = [line]
                else:
                    listOfHooks[office][theme][key].append(line)

    return listOfHooks


def sort_dict_hook(hookDict: dict) -> dict:
    """
    This function sort the dictionary of hooks by key

    Args:
        hookDict (dict): The dictionary of hooks

    Returns:
        dict: The sorted dictionary
    """
    # sort the dictionary by key
    for office in hookDict.keys():
        for theme in hookDict[office].keys():
            hookDict[office][theme] = {k: v for k, v in sorted(hookDict[office][theme].items(), key=lambda item: item[0].lower())}
    return hookDict


def format_md_hooks(hookDict: dict, markdown: str) -> int:
    """
    This function format the hooks in a markdown file

    Args:
        hookDict (dict): The dictionary of hooks
        markdown (str): The file to write the hooks in

    Returns:
        int: The number of hooks
    """
    counter = 0
    with open(markdown, "w") as md:
        md.write("## Default hook list\n")
        for office in hookDict.keys():
            md.write(f"\n### {office}\n")
            for theme in hookDict[office].keys():
                md.write(f"\n#### Thème: {theme}\n")
                for key in hookDict[office][theme].keys():
                    md.write(f"\n##### {key}\n\n")
                    md.write("<details>\n\n")

                    for hook in hookDict[office][theme][key]:
                        counter += 1
                        hookName = ""

                        # if the hook contains a _, replace it by \_
                        if "_" in hook:
                            hook = hook.replace("_", "\\_")

                        # if the hook contains a comma, it is a hook with multiple fields
                        if "," in hook:
                            hookName = hook.split(",")[0].split("name:")[1]

                        if hookName == "":
                            hookName = hook.split("name:")[1]
                        
                        md.write(f"* **{hookName}**\n")

                        # if the hook contains multiple fields
                        for h in hook.split(",")[1:]:
                            h = h.strip()
                            if "|" in h:
                                fields = h.split(":")
                                md.write(f"\t* {fields[0]}:\n")
                                for arg in fields[1].split("|"):
                                    md.write(f"\t\t* {arg}\n")
                            elif h != "":
                                md.write(f"\t* {h}\n")

                    md.write("\n</details>\n")
    return counter

def integrate(fromFile: str, toFile: str) -> None:
    """
    This function integrate the formatted hooks in a specified markdown file

    Args:
        fromFile (str): The file to read the hooks from
        toFile (str): The file to write the hooks in
    """
    if not os.path.exists(fromFile):
        print("The file does not exist.")
        raise FileNotFoundError

    if not os.path.exists(toFile):
        print("The file does not exist.")
        raise FileNotFoundError

    index = 0
    with open(toFile, "r") as file:
        content = file.readlines()
        for line in content:
            if "## Default hook list" in line:
                index = content.index(line)
                break

    with open(fromFile, "r") as file:
        if index != 0:
            fileMode = "w"
        else:
            fileMode = "a"
        
        with open(toFile, fileMode) as fileToWrite:
            fileToWrite.writelines(content[0:index])
            for line in file.readlines():
                fileToWrite.write(line)


def all() -> None:
    directory = input("Enter the directory to scan: ")

    file = input("Enter the file to read the hooks from [log.txt] : ")
    markdownFile = input("Enter the file to write the hooks in [hooks.md] : ")

    toFile = input("Enter the file to write the hooks in [documentation.md] : ")

    order = input("Do you want to sort the hooks by key [Y/n] : ").lower()

    if not directory.startswith("./"):
        directory = "./"+directory
    if file == "":
        file = "log.txt"
    if markdownFile == "":
        markdownFile = "hooks.md"
    if toFile == "":
        toFile = "documentation.md"

    try:
        get_hooks(directory, file)
        print("Hooks successfully extracted.")
    except ValueError as e:
        ...
    except FileNotFoundError as e:
        ...
    except Exception as e:
        print("An error occured get_hooks.\n", e)

    try:
        hooks = get_from_logs(file)
        if order != "n":
            hooks = sort_dict_hook(hooks)
        counter = format_md_hooks(hooks, markdownFile)
        print(f"{counter} hooks successfully formatted.")
    except Exception as e:
        print("An error occured in get_from_logs.\n", e)

    try:
        integrate(markdownFile, toFile)
        print("Hooks successfully integrated.")
    except Exception as e:
        print("An error occured in integrate.\n", e)


def clean() -> None:
    removed = False
    if os.path.exists("log.txt"):
        os.remove("log.txt")
        removed = True
    if os.path.exists("hooks.md"):
        os.remove("hooks.md")
        removed = True
    if removed:
        print("Files successfully removed.")
    else:
        print("No files to remove.")


def help() -> None:
    """
    This function display the help message
    """
    print("\nThis script allow you to get all the hooks in the html files of a directory and write them in a markdown file.")
    print("\nUsage:")
    print("[1] - help")
    print("[2] - scan the directory to get the hooks")
    print("[3] - format the hooks in a markdown file")
    print("[4] - integrate the formatted hooks in the documentation markdown file")
    print("[5] - all the steps in one command")
    print("[6] - clean the files created by the script(log.txt, hooks.md)")
    print("")
    print("[0] - exit")

def main() -> None:
    """
    This function is the main function of the hook script
    """
    print("Welcome to the hooks script.")
    help()

    while True:
        choice = input("\nEnter your choice ([1] - help): ")
        
        match choice:
            case "0":
                break

            case "1":
                help()

            case "2":
                directory = input("Enter the directory to scan: ")
                if not directory.startswith("./"):
                    directory = "./"+directory
                file = input("Enter the file to write the hooks in [log.txt] : ")

                if file == "":
                    file = "log.txt"

                try:
                    get_hooks(directory, file)
                    print("Hooks successfully extracted.")
                except ValueError as e:
                    ...
                except FileNotFoundError as e:
                    ...
                except Exception as e:
                    print("An error occured.\n", e)

            case "3":
                file = input("Enter the file to read the hooks from [log.txt] : ")
                order = input("Do you want to sort the hooks by key [Y/n] : ").lower()
                markdownFile = input("Enter the file to write the hooks in [hooks.md] : ")

                if file == "":
                    file = "log.txt"
                if markdownFile == "":
                    markdownFile = "hooks.md"

                try:
                    hooks = get_from_logs(file)
                    if order != "n":
                        hooks = sort_dict_hook(hooks)
                    counter = format_md_hooks(hooks, markdownFile)
                    print(f"{counter} hooks successfully formatted.")
                except Exception as e:
                    print("An error occured.\n", e)
            
            case "4":
                file = input("Enter the file to read the hooks from [hooks.md] : ")
                toFile = input("Enter the file to write the hooks in [documentation.md] : ")

                if file == "":
                    file = "hooks.md"
                if toFile == "":
                    toFile = "documentation.md"

                try:
                    integrate(file, toFile)
                    print("Hooks successfully integrated.")
                except Exception as e:
                    print("An error occured.\n", e)

            case "5":
                all()

            case "6":
                clean()
            
            case _:
                print("Invalid choice. Please try again.")
                continue


if __name__ == "__main__":
    main()
    print("Goodbye!\n")
    sys.exit()