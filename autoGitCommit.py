import requests
import json
import subprocess
import os

# in bash,run `export API_KEY=your_api_key`
API_KEY = os.environ.get('API_KEY')
MODEL_NAME = "gemini-pro"

def generate_commit_message(prompt):
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

# prompt = generate_commit_message(generate_commit_prompt())

# if prompt:
#     print(prompt.split("\n")[0])
# else:
#     print("commit generation failed.")


def commit_and_push(commit_message):
    # Stage the changes
    # subprocess.call(["git", "add", "."])

    # Commit with the generated message
    subprocess.call(["git", "commit", "-m", commit_message])

    # Push to the current branch (assumes a remote is set up)
    subprocess.call(["git", "push"])

if __name__ == "__main__":  # Good practice to guard code in a main block
    prompt = generate_commit_message(generate_commit_prompt())

    if prompt:
        commit_message = prompt.split("\n")[0]  # Use the generated message
        print(f"Generated commit message: {commit_message}")

        # Perform the commit and push
        commit_and_push(commit_message)
        print("Changes committed and pushed to remote.")
    else:
        print("Commit generation failed.")



