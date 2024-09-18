#!/bin/zsh

# Iterate over each key in the file
while IFS= read -r key; do
    # Check if the key is present in the files
    grep -q "$key" data/MS_SCQ.txt
    found_in_core=$?  # Capture the exit status of grep for the core file

    grep -q "$key" data/FT_FLASCQ.txt
    found_in_ft=$?  # Capture the exit status of grep for the ft file

    # Check conditions based on the exit statuses
    if [[ $found_in_ft -ne 0 && $found_in_core -eq 0 ]]; then
        echo "$key"
    fi
done < data/MS_FLASCQ.txt