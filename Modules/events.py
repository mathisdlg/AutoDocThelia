import os
import eventAnalyzer


def main() -> None:
    """
    This is the event documentation generator.
    """
    eventPath = input("Enter the path to the event directory: ")
    if not eventPath.endswith("/"):
        eventPath += "/"
    source = eventPath + "TheliaEvents.php"
    destination = input("Enter the destination file path [parsedEvent2.md] : ")
    if destination == "":
        destination = "parsedEvent2.md"

    os.system("./Scripts/eventPreAnalyzer.sh -r " + eventPath)

    if os.path.exists("dataArrayEvent.txt"):
        eventAnalyzer.main(source, destination)
        os.remove("dataArrayEvent.txt")
        print("dataArrayEvent.txt removed.")
    else:
        print("Error: dataArrayEvent.txt not found.")