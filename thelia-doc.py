import sys, os
import Modules.hooks as hooks, Modules.events as events, Modules.commands as commands


def help():
    print("\nThis is the documentation manager. Here are the commands you can use:")
    print("[1] - help: Display this help message")
    print("[2] - go to hooks documentation manager")
    print("[3] - generate events documentation")
    print("[4] - generate commands documentation")
    print("[9] - generate all documentation")
    print("")
    print("[0] - exit: Exit the program\n")


if __name__ == '__main__':
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
                hooks.main()
            case '3':
                events.main()
            case '4':
                commands.main()
            case '9':
                events.main()
                hooks.all()
                hooks.clean()
                commands.main()
            case _:
                print("Invalid choice. Please try again.\n")
                continue

    print("Goodbye!")
    sys.exit(0)