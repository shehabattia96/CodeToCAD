#!/bin/sh

set -e # exit script if there is an error.

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

# Get the current Git commit epoch time
git_commit_epoch=$(git show -s --format=%ct HEAD)

# Define the source and destination paths
SOURCE_PATH="$SCRIPT_DIR/../codetocad/capabilities.json"
DESTINATION_PATH="$SCRIPT_DIR/../docs/capabilities/capabilities_${git_commit_epoch}.json"

# Copy the file
cp "$SOURCE_PATH" "$DESTINATION_PATH"

echo "File copied to $DESTINATION_PATH"