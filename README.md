## Git Commit Message Generator with AI

This Python script leverages a powerful language model to automatically generate Git commit messages based on your code changes. The script also performs `git commit` and `git push` for a streamlined workflow.

### Dependencies

* **Python 3:** You'll need Python 3 installed on your system. Download it from https://python.org if you don't have it already.
* **requests library:** Install this library using pip:
    ```bash
    pip install requests
    ```

### Environment Variables

* **API_KEY:** You must obtain an API key for the generative language model you want to use (e.g., from the Google Cloud Platform).  Once you have it, set the environment variable:
    ```bash
    export API_KEY=your_api_key
    ```

### Usage

1. **Make changes to your code:** Add, modify, or delete files within your Git repository.
2. **Stage your changes:** Use `git add` to stage the files you want to commit.
3. **Run the script:** Execute the Python script (e.g., `python commit_generator.py`)
4. **Commit and Push:** The script will generate a commit message, commit your changes, and push them to your remote repository.

### Notes

* Make sure you have a remote repository set up for your project. The script assumes a standard remote named 'origin'.
* The script uses the 'gemini-pro' language model by default. You can customize the `MODEL_NAME` variable if you want to use a different model.

### Example

```bash
# Modify some files in your project
git add .  # Stage the changes
python commit_generator.py


