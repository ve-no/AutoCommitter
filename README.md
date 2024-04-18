
# **AutoGitCommit - Your AI-Powered Git Commit Assistant**

**Brief Description**

* A convenient tool that helps you generate descriptive Git commit messages using advanced language models (powered by Google's Generative Language API).

**Installation**

1. **Prerequisites:**
   * A Google Cloud Platform project with the Generative Language API enabled.
   * A valid API key for the Generative Language API.
   * Python 3
   * Git

2. **Download the scripts:**
   ```bash
   git clone https://github.com/ve-no/AutoCommitter.git
   ```

3. **Setup:**
   ```bash
   cd <repo-name>
   ./setup_commit_helper.sh
   ```
   * The setup script will download `autoGitCommit.py`, place it in your local bin directory, and set up a convenient alias.
   * You will be prompted to enter your Google Cloud API key.

**Usage**

1. **Stage your changes:**
   ```bash
   git add <files>
   ```

2. **Generate and commit:**
   ```bash
   commit
   ```
   *  This runs `autoGitCommit.py`, which does the following:
      * Analyzes your staged changes
      * Calls the Generative Language API to create a commit message
      * Prompts you for confirmation
      * Executes `git commit` and `git push` if you're happy with the message

**Customization**

* **Model Configuration:** In `autoGitCommit.py`, you can adjust the `MODEL_NAME` to explore different language models provided by the Generative Language API.

**Important Notes**

* Before using, replace "gemini-pro" in `autoGitCommit.py` with a model name suitable for your project and available from the Generative Language API.
* It's always best practice to review the generated commit messages before finalizing your commits.

**Example**

```bash
# ... make and stage changes...

commit  # Run the command

# Output:
# Generated commit message: Setup: Install autoGitCommit script as an alias
# Is this commit message okay? (y/n): y
# Changes committed and pushed to remote.
```

**Why Use AutoGitCommit**

* Save time crafting commit messages
* Get inspiration for clearer and more informative commits
* Ensure consistency in your commit history

**Project Structure**

* `autoGitCommit.py` - The main Python script responsible for commit message generation and Git commands.
* `setup_commit_helper.sh` - A convenient Bash setup script for installation.

**Contributing**

Welcome contributions! Feel free to open issues or submit pull requests.
