#!/bin/bash

# function to browse files in the current directory and retrieve informations
browse_files_current_directory() {
    local path=$1
    local output_file=$2

    # browse all files in the current directory
    find "$path" -maxdepth 1 -type f ! -name ".*" | sort | while read file; do
        # check if the file contains '@deprecated'
        if grep -q '@deprecated' "$file"; then
            class=$(grep -o -m 1 'class\s*\(\w\+\)' "$file" | sed 's/class\s*//')
            echo -n "- **⚠️ Warning**\n > $class is **deprecated**, please use $file\n" >> "$output_file"
            continue
        fi

        # extract the class name
        class=$(grep -o -m 1 'class\s*\(\w\+\)' "$file" | sed 's/class\s*//')

        # extract constructor arguments
        constructor=$(awk '/__construct\(/,/)/' "$file" | tr -d '\n' | sed 's/__construct\s*//; s/(\(.*\))/\1/' | awk -F '[, ]+' '{for(i=1;i<=NF;i++) if($i ~ /^\$/) print $i}' | sed 's/[()]//g' | sort -u | tr '\n' ' ')

        if [ -z "$constructor" ]; then
            echo -n "- $class -> no constructor found in this file  \n" >> "$output_file"
        else
            echo -n "- $class -> $constructor  \n" >> "$output_file"
        fi
    done
}

# check if the number of arguments is valid
if [ $# -lt 1 ]; then
    echo -n "Usage: $0 <path/to/Event/directory> [output_file_name.md]"
    exit 1
fi

# path to the folder provided as argument
path=$1
output_file="dataArrayEvent.txt"

# check if the name of the output file is given as argument and create it if it doesn't exist
if [ $# -eq 2 ]; then
    output_file=$2
fi

echo -n "[[noCategory," >> "$output_file"

# files at the root
browse_files_current_directory "$path" "$output_file"
echo -n "]," >> "$output_file"

# browse all folders in the provided path
find "$path" -mindepth 1 -type d,f ! -name ".*" | sort | while read element; do
    # check if the element is a directory
    if [ -d "$element" ]; then
        # extract the name of the folder where the event is located
        parentFolderName=$(basename "$element")

        echo -n "[$parentFolderName," >> "$output_file"

        # browse files in the folder
        browse_files_current_directory "$element" "$output_file"

        echo -n "]," >> "$output_file"
    fi
done

echo -n "]" >> "$output_file"
