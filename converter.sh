#!/bin/bash

# Loop through all .dat files in the current directory
for file in *.dat; do
    # Check if files with .dat extension exist
    if [ -e "$file" ]; then
        # Get the filename without .dat extension and add .orb
        newname="${file%.dat}.orb"
        # Rename the file
        mv "$file" "$newname"
        echo "Renamed: $file -> $newname"
    fi
done