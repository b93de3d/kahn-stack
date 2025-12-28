#!/bin/bash
set -e

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

dir="$1"

# Check if the argument is an existing directory
if [ -d "$dir" ]; then
  # Check if the directory is empty
  if [ "$(ls -A "$dir")" ]; then
    echo "Error: The directory '$dir' is not empty."
    exit 1
  fi
else
  # If the directory doesn't exist, create it
  mkdir -p "$dir"
fi

echo "Creating new Kahn Stack project: $dir"
git clone git@github.com:b93de3d/kahn-stack.git $dir
cd $dir
chmod +x kahn.py
ln -s kahn.py kahn
kahn template deploy django_backend
template_version=$(git rev-parse --short HEAD)
rm -rf .git
git init
git add .
git commit -m "New Kahn Stack project ($template_version)"
