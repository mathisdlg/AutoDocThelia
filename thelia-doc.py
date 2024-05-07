#!/usr/bin/env python3

import sys, os
import Modules.hooks as hooks, Modules.events as events, Modules.commands as commands, Modules.check as check
import Modules.loopAnalyser as loops


def help():
    print("\nThis is the documentation manager. Here are the commands you can use:")
    print("[1] - help: Display this help message")
    print("[2] - generate hooks documentation")
    print("[3] - generate events documentation")
    print("[4] - generate commands documentation")
    print("[5] - generate loops documentation")
    print("[9] - generate all documentation")
    print("")
    print("[0] - exit: Exit the program\n")

def interacive():
    print("Welcome to the documentation manager!")
    help()
    while True:
        choice = input("What would you like to do ([1] - help): ")
        
        match choice:
            case '0':
                print("Exiting the program...")
                break
            case '1':
                help()
            case '2':
                directory = input("Enter the path to the Thelia directory: ")
                toFile = input("Enter the documentation path to modify: ")
                order = input("Would you like to sort the hooks [Y/n]: ")
                hooks.all(directory, toFile, order)
            case '3':
                eventPath = input("Enter the path to the event directory: ")
                destinaion = input("Enter the doc destination file path: ")
                events.main(eventPath, destinaion)
            case '4':
                directory = input("Enter the path to the Thelia directory: ")
                toFile = input("Enter the documentation path to modify: ")
                commands.main(directory, toFile)
            case '5':
                loopFolder = input("Enter the path to the root of thelia: ")
                loopDoc = input("Enter the path to the loop documentation file: ")
                loops.main(loopFolder, loopDoc)
            case '9':
                rootThelia = input("Enter the path to the root of the Thelia project to scan (Thelia Core): ")
                rootDoc = input("Enter the root path of the documentation to modify: ")
                orderHook = input("Would you like to sort the hooks: ").lower()

                generate(rootThelia, rootDoc, orderHook)
            case _:
                print("Invalid choice. Please try again.\n")
                continue

    print("Goodbye!")
    sys.exit(0)


def generate(rootThelia, rootDoc, orderHook="y"):
    hooksDoc = os.path.join(rootDoc, "docs/hooks.md")
    eventsDoc = os.path.join(rootDoc, "docs/events.md")
    commandsDoc = os.path.join(rootDoc, "docs/commands/")
    loopDoc = os.path.join(rootDoc, "docs/loops/")

    theliaEvents = os.path.join(rootThelia, "core/lib/Thelia/Core/Event/")

    events.main(theliaEvents, eventsDoc)
    hooks.all(rootThelia, hooksDoc, orderHook)
    commands.main(rootThelia, commandsDoc)
    loops.main(rootThelia, loopDoc)


def check():
    raise NotImplementedError("Not implemented yet")



if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--CI":
            if len(sys.argv)>4 and sys.argv[2] == "--generate":
                rootThelia = sys.argv[3]
                rootDoc = sys.argv[4]
                if len(sys.argv) > 5:
                    orderHook = sys.argv[5].lower()
                else:
                    orderHook = "y"
                generate(rootThelia, rootDoc, orderHook)
                sys.exit(0)
            elif len(sys.argv)>3 and sys.argv[2] == "--check":
                check()
                sys.exit(0)
            
        print("Usage:")
        print("By args:")
        print("\tpython3 thelia-doc.py --CI --generate <Thelia root> <Doc root> [<orderHook: [Y/n]>]")
        print("OR")
        print("\tpython3 thelia-doc.py --CI --check <Thelia root>")
        print("By interactive shell")
        print("\tUsage: python3 thelia-doc.py")
    else:
        interacive()