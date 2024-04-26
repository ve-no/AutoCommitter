import requests
import json
import subprocess
import time
import os

API_KEY = os.environ.get('API_KEY')
MODEL_NAME = "gemini-pro"


def generate_commit_message(prompt):
    """
    Generates a commit message based on the given prompt.

    Args:
        prompt (str): The prompt to generate the commit message from.

    Returns:
        str: The generated commit message.

    Raises:
        None
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    else:
        print(f"Error: {response.status_code}")
        return None

def generate_commit_prompt(filename):
    """
    Generates a commit message prompt based on the changes in the staged files.

    Args:
        filename (str): Name of the file to create the prompt for.

    Returns:
        str: The commit message prompt.

    Raises:
        subprocess.CalledProcessError: If the 'git diff' command fails.
    """
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--cached", filename],
            stderr=subprocess.STDOUT
        ).decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Failed to get diff for file: {filename}, Error: {str(e)}")
        return None

    prompt = f"Write a concise commit message that summarizes the changes in {filename}:\n\n{diff_output}\n"
    prompt += "**Tips:**\n"
    prompt += "- Use imperative present tense (e.g., 'Fix bug', not 'Fixed bug')\n"
    prompt += "- Aim for a single line, with a maximum of 50 characters\n"
    return prompt


def handle_file_change(filename, status):
    """Handles actions for a changed file based on its status code."""
    if status == 'D':
        subprocess.call(["git", "rm", filename])
        commit_message = f"Delete file {filename}"
    else:  # 'M' or 'A'
        subprocess.call(["git", "add", filename])
        commit_prompt = generate_commit_prompt(filename)
        if commit_prompt:
            commit_message = generate_commit_message(commit_prompt)
            if not commit_message:
                print(f"Failed to generate commit message for {filename}.")
                return

    subprocess.call(["git", "commit", "-m", commit_message])
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
        if os.path.exists(filename):
            handle_file_change(filename, status)
        else:
            print(f"File {filename} has been deleted but not staged. Skipping.")


if __name__ == "__main__":
    while True:
        automate_git_commit()
        time.sleep(60)  # Wait for 30 minutes before checking again
