#!/bin/zsh

# Loop through all MKV files in the current directory
for file in *.mkv; do
    # Extract the base name without extension
    base_name=${file:r}

    # Run ffmpeg command to extract subtitle and save as ASS file
    ffmpeg -i "$file" -map 0:2 -c copy "${base_name}.ass"
done

