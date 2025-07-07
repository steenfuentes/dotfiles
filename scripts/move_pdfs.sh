#!/bin/bash

# Check if source and target directories are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <source_directory> <target_directory>"
    exit 1
fi

source_dir="$1"
target_dir="$2"

# Check if source directory exists
if [ ! -d "$source_dir" ]; then
    echo "Error: Source directory '$source_dir' does not exist"
    exit 1
fi

# Check if target directory exists, create if it doesn't
if [ ! -d "$target_dir" ]; then
    mkdir -p "$target_dir"
fi

# Find all PDFs recursively and move them to target directory
find "$source_dir" -type f -iname "*.pdf" -exec mv -i {} "$target_dir" \;

echo "PDF files have been moved to $target_dir"
