import requests
import json
import subprocess
import os


# Replace with your actual API Key
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

    # Extract relevant information from the diff
    # Here, we split the diff output by file, and then extract the filename and the diff content
    # We include the filename and the diff content in the prompt
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
    prompt = "Generate a commit message for the following changes:\n\n"
    for filename, diff_content in changed_files:
        prompt += f"- Changes in file: {filename}\n\n{diff_content}\n"

    return prompt

# prompt = "Write a story about a magic backpack"
prompt = generate_commit_message(generate_commit_prompt())

if prompt:
    print(prompt)
else:
    print("Story generation failed.")
