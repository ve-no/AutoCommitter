#!/bin/bash

# Settings
PYTHON_SCRIPT_NAME="autoGitCommit.py"
ALIAS_NAME="commit"
SCRIPT_DOWNLOAD_PATH="$HOME/.local/bin"

# Create the download directory if it doesn't exist
mkdir -p "$SCRIPT_DOWNLOAD_PATH"

# Download the script
cp $PYTHON_SCRIPT_NAME $SCRIPT_DOWNLOAD_PATH

# Prompt for API key
read -p "Enter your API key: " API_KEY

# Add alias to .zshrc, including environment variable setup
echo "alias $ALIAS_NAME='export API_KEY=$API_KEY; python3 $SCRIPT_DOWNLOAD_PATH/$PYTHON_SCRIPT_NAME'" >> ~/.zshrc

# Let the user know it's done
echo "Setup complete! You can now use the '$ALIAS_NAME' command."
echo "To apply changes, either restart your terminal or run: source ~/.zshrc"
