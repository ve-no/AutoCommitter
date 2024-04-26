import requests
import json
import subprocess
import os
import time  # Import the 'time' module for scheduling

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

def generate_commit_prompt():
    """
    Generates a commit message prompt based on the changes in the staged files.

    Returns:
        str: The commit message prompt.

    Raises:
        subprocess.CalledProcessError: If the 'git diff' command fails.
    """
    diff_output = subprocess.check_output(["git", "diff", "--cached"]).decode("utf-8")
    if not diff_output:
        print("No changes in the staged files.")

    changed_files = []
    start = -1
    for idx, line in enumerate(diff_output.splitlines()):
        if line.startswith("diff --git"):
            if start != -1:
                changed_files.append((filename, diff_output[start:idx]))
            start = idx
            filename = line.split()[-1]
    if start != -1:
        changed_files.append((filename, diff_output[start:]))

    prompt = "Write a concise commit message that summarizes the following:\n\n"
    for filename, diff_content in changed_files:
        prompt += f"- Changes in file: {filename}\n\n{diff_content}\n"
    prompt += "\n**Tips:**\n"
    prompt += "- Use imperative present tense (e.g., 'Fix bug', not 'Fixed bug')\n"
    prompt += "- Aim for a single line, with a maximum of 50 characters\n"

    return prompt


def automate_git_commit():
    """
    Automates the Git commit process:
        - Finds modified files.
        - Adds each modified file.
        - Generates a commit message.
        - Commit and push the changes.
    """
    modified_files = subprocess.check_output(
        ["git", "status", "--porcelain"]
    ).decode("utf-8").splitlines()



    if not modified_files:
        print("No modified files to commit.")
        return

    for line in modified_files:
        status = line[0]
        filename = line[3:]  # Extract filename
        print(filename)
        print(status)
        # if status in ['M', 'A']:  # Check if modified or added
        subprocess.call(["git", "add", filename])

    prompt = generate_commit_message(generate_commit_prompt())

    if prompt:
        print(f"Generated commit message: {prompt}")
        subprocess.call(["git", "commit", "-m", prompt])
        subprocess.call(["git", "push"])
        print("Changes committed and pushed to remote.")
    else:
        print("Commit generation failed.")

if __name__ == "__main__":
    while True:
        automate_git_commit()
        time.sleep(1 * 6)  # Sleep for 30 minutes
