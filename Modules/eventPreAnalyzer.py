import os, re

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


def main(path, output_file="dataArrayEvent.txt"):
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