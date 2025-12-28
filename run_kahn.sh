#!/bin/sh

# Start from the current directory
dir="$PWD"

# Resolve the path of this script to avoid executing itself
self_path="$(realpath "$0")"

while true; do
    # Check if an executable `kahn` file exists that is not itself
    if [[ -x "$dir/kahn" && "$(realpath "$dir/kahn")" != "$self_path" ]]; then
        # Execute the found script and forward all arguments
        "$dir/kahn" "$@"
        exit 0
    fi

    # Move to the parent directory
    dir=$(dirname "$dir")

    # If we reach the root directory and haven't found a script, exit
    if [[ "$dir" == "/" || -z "$dir" ]]; then
        echo "No available kahn script found in any parent directories."
        exit 1
    fi
done