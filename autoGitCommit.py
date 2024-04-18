import requests
import json
import subprocess
import os

# in bash,run `export API_KEY=your_api_key`
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
    # Use git diff to get the changes in the staged files
    diff_output = subprocess.check_output(["git", "diff", "--cached"]).decode("utf-8")

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

    # Generate the commit message prompt based on the changes
    prompt = "Write a concise commit message that summarizes the following:\n\n"
    for filename, diff_content in changed_files:
        prompt += f"- Changes in file: {filename}\n\n{diff_content}\n"
    prompt += "\n**Tips:**\n"
    prompt += "- Use imperative present tense (e.g., 'Fix bug', not 'Fixed bug')\n"
    prompt += "- Aim for a single line, with a maximum of 50 characters\n"

    return prompt

if __name__ == "__main__":
    while True:
        prompt = generate_commit_message(generate_commit_prompt())

        if prompt:
            print(f"Generated commit message: {prompt}")

            confirmation = input("Is this commit message okay? (y/n): ")
            if confirmation.lower() in ['y', '']:
                subprocess.call(["git", "commit", "-m", prompt])
                subprocess.call(["git", "push"])
                print("Changes committed and pushed to remote.")
                break
            else:
                print("Regenerating commit message...")
        else:
            print("Commit generation failed.")
            break


