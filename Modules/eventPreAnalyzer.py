import os
import re

# function to browse files in the current directory and retrieve information
def browse_files_current_directory(path, data, folder_name):
    class_data = []
    # iterate through the files in the directory
    with os.scandir(path) as entries:
        for entry in sorted(entries, key=lambda x: x.name): 
            # check if the entry is a file and has a '.php' extension
            if entry.is_file() and entry.name.endswith('.php'):
                file_path = os.path.join(path, entry.name)
                # extract class information
                process_file(file_path, class_data)

    if class_data:
        data.append([folder_name] + sorted(class_data))


# function to extract class information from a PHP file
def process_file(file_path, class_data):
    with open(file_path, 'r') as file:
        content = file.read()

    # extract class name
    class_name_match = re.search(r'class\s+(\w+)', content)
    if class_name_match:
        class_name = class_name_match.group(1)
    else:
        class_name = ''

    # extract constructor arguments
    constructor_match = re.search(r'__construct\s*\((.*?)\)', content, re.DOTALL)
    constructor_args = [arg.strip() for arg in constructor_match.group(1).split(',') if arg.strip()] if constructor_match else []
    constructor_str = ', '.join(constructor_args)

    # check if the file contains '@deprecated' or if it has constructor arguments
    if '@deprecated' in content:
        class_data.append(class_name + "-> ⚠️ Warning > deprecated, please use " + file_path)
    elif constructor_args:
        class_data.append(class_name + "-> " + constructor_str)
    else:
        class_data.append(class_name + "-> no constructor found in this file")


# function to browse subdirectories recursively
def browse_subdirectories(path, data):
    for element in sorted(os.listdir(path)):
        element_path = os.path.join(path, element)
        if os.path.isdir(element_path):
            browse_files_current_directory(element_path, data, element)


def main(path, output_file="dataArrayEvent.txt"):
    data = []

    # check if the provided path is a file
    if os.path.isfile(path):
        process_file(path, data)
    # check if the provided path is a directory
    elif os.path.isdir(path):
        # add root files to a list named "noCategory" if present = not in a directory
        root_files = [entry.name for entry in os.scandir(path) if entry.is_file() and entry.name.endswith('.php')]
        if root_files:
            browse_files_current_directory(path, data, "noCategory")

        # browse all folders in the provided path
        for element in sorted(os.listdir(path)):
            element_path = os.path.join(path, element)
            if os.path.isdir(element_path):
                browse_files_current_directory(element_path, data, element)
                browse_subdirectories(element_path, data)
    else:
        print("the specified path does not match any valid file or directory")

    # write data in the output file
    with open(output_file, 'w') as f:
        f.write(str(data))

if __name__ == "__main__":
    path = input("Enter the path to the event directory: ")
    main(path)