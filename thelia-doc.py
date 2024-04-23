import sys
import hooks


def help():
    print("This is the documentation manager. Here are the commands you can use:")
    print("[1] - help: Display this help message")
    print("[2] - go to hooks documentation manager")
    print("[3] - go to event documentation manager")
    print("[0] - exit: Exit the program")


if __name__ == '__main__':
    print("Welcome to the documentation manager!")
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
                raise NotImplementedError("Event documentation manager is not implemented yet.")
                # events.main()
            case _:
                print("Invalid choice. Please try again.\n")
                continue

    print("Goodbye!")
    sys.exit(0)