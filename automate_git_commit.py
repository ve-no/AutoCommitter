import requests
import json
import subprocess
import time
import os
import autoGitCommit

API_KEY = os.environ.get('API_KEY')
MODEL_NAME = "gemini-pro"

def handle_file_change(filename, status):
    """Handles actions for a changed file based on its status code."""
    if not os.path.exists(filename):
        subprocess.call(["git", "rm", filename])
        commit_message = f"Delete file {filename}"
    else:  # 'M' or 'A'
        subprocess.call(["git", "add", filename])
        commit_prompt = autoGitCommit.generate_commit_prompt()
        if commit_prompt:
            commit_message =  autoGitCommit.generate_commit_message(commit_prompt)
            if not commit_message:
                print(f"Failed to generate commit message for {filename}.")
                return

    subprocess.call(["git", "commit", "-m", commit_message])
    print(f"Generated commit message: \033[92m{commit_message}\033[0m")
    subprocess.call(["git", "push"])
    print(f"Changes in {filename} committed and pushed to remote.")

def automate_git_commit():
    """Automates the Git commit process with granular file-by-file tracking."""
    try:
        modified_files = subprocess.check_output(
            ["git", "status", "--porcelain"]
        ).decode("utf-8").splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Failed to get status from Git: {str(e)}")
        return

    for line in modified_files:
        status = line[0]
        filename = line[3:]
        handle_file_change(filename, status)

if __name__ == "__main__":
    while True:
        automate_git_commit()
        time.sleep(30 * 60)
