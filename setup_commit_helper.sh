#!/bin/bash

PYTHON_SCRIPT_NAME="autoGitCommit.py"
ALIAS_NAME="commit"
SCRIPT_DOWNLOAD_PATH="$HOME/.local/bin"

NEW_SCRIPT_NAME="automate_git_commit.py"  # Replace with the actual script name
NEW_ALIAS_NAME="autocommit"       # Replace with your desired alias

# Create the download directory if it doesn't exist
mkdir -p "$SCRIPT_DOWNLOAD_PATH"

# Download the script
cp $PYTHON_SCRIPT_NAME $SCRIPT_DOWNLOAD_PATH
cp $NEW_SCRIPT_NAME $SCRIPT_DOWNLOAD_PATH

# Prompt for API key
read -p "Enter your API key: " API_KEY

# Add alias to .zshrc, including environment variable setup
echo "export API_KEY=$API_KEY" >> ~/.zshrc
echo "alias $ALIAS_NAME='python3 $SCRIPT_DOWNLOAD_PATH/$PYTHON_SCRIPT_NAME'" >> ~/.zshrc
echo "alias $NEW_ALIAS_NAME='python3 $SCRIPT_DOWNLOAD_PATH/$NEW_SCRIPT_NAME'" >> ~/.zshrc

# Let the user know it's done
echo "Setup complete! You can now use the '$ALIAS_NAME' command."
echo "To apply changes, either restart your terminal or run: source ~/.zshrc"
