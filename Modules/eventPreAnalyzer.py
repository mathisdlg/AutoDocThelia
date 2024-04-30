import os
import sys
import re

# function to browse files in the current directory and retrieve information
def browse_files_current_directory(path, output_file):
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.php'):
                file_path = os.path.join(path, entry.name)
                
                # read the file content
                with open(file_path, 'r') as file:
                    content = file.read()

                # check if the file contains '@deprecated'
                if '@deprecated' in content:
                    class_name = re.search(r'class\s+(\w+)', content).group(1)
                    with open(output_file, 'a') as f:
                        f.write(f"- **⚠️ Warning** > {class_name} is **deprecated**, please use {file_path}")
                    continue

                # extract the class name
                class_name_match = re.search(r'class\s+(\w+)', content)
                if class_name_match:
                    class_name = class_name_match.group(1)
                else:
                    class_name = ''

                # extract constructor arguments
                constructor_match = re.search(r'__construct\s*\((.*?)\)', content, re.DOTALL)
                constructor_args = [arg.strip() for arg in constructor_match.group(1).split(',') if arg.strip()] if constructor_match else []
                constructor_str = ', '.join(constructor_args)

                if not constructor_args:
                    with open(output_file, 'a') as f:
                        f.write(f"- {class_name} -> no constructor found in this file")
                else:
                    with open(output_file, 'a') as f:
                        f.write(f"- {class_name} -> {constructor_str}")


def main():
    # check if the number of arguments is valid
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "[-r] <path/to/Event/directory> [output_file_name.md]")
        sys.exit(1)

    # check if -r option is provided
    if sys.argv[1] == "-r":
        replace = True
        del sys.argv[1]
    else:
        replace = False

    # path to the folder provided as argument
    path = sys.argv[1]

    # Create the output directory if it does not exist
    if len(sys.argv) == 3:
        output_dir = os.path.dirname(sys.argv[2])
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # check if the output file name is provided as an argument
    if len(sys.argv) == 3:
        output_file = sys.argv[2]
    else:
        output_file = "dataArrayEvent.txt"

    # check if output file already exists
    if os.path.exists(output_file) and not replace:
        print(f"Error: Output file '{output_file}' already exists. Please choose a different name or use the -r option to replace it.")
        print("Usage:", sys.argv[0], "[-r] <path/to/Event/directory> [output_file_name.md]")
        sys.exit(1)

    # files at the root
    browse_files_current_directory(path, output_file)

    # browse all folders in the provided path
    for element in os.listdir(path):
        element_path = os.path.join(path, element)
        if os.path.isdir(element_path):
            parentFolderName = os.path.basename(element_path)
            with open(output_file, 'a') as f:
                f.write(f"[{parentFolderName},")

            # browse files in the folder
            browse_files_current_directory(element_path, output_file)

            with open(output_file, 'a') as f:
                f.write("],")

    with open(output_file, 'a') as f:
        f.write("]")
