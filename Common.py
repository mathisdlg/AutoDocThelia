import os


def integrate(fromFile: str, toFile: str, matchChain: str = None) -> None:
    """
    This function integrate the formatted text in a specified markdown file

    Args:
        fromFile (str): The file to read from
        toFile (str): The file to write in
        matchChain (str): The chain to match in the file to write in
    """
    if not os.path.exists(fromFile):
        print("The file to read in does not exist.")
        raise FileNotFoundError

    if not os.path.exists(toFile):
        print("The file to write in does not exist.")
        raise FileNotFoundError

    index = 0
    if not (matchChain is None):
        with open(toFile, "r") as file:
            content = file.readlines()
            for line in content:
                if matchChain in line:
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