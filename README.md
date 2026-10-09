# AI Sentiment Analyzer

A beginner-friendly NLP project built with Python and Streamlit. It sends text to a Groq-hosted large language model (LLM) and displays whether the text is Positive, Negative, or Neutral, with a short explanation and important keywords.

## Features

- Analyze a sentence, product review, or paragraph.
- Classify sentiment as Positive, Negative, or Neutral.
- Show a short explanation and 3 to 5 keywords.
- Keep a history of completed analyses for the current browser session, with a clear-history button.
- Limit each input to 5,000 characters.
- Load the Groq model settings from `config.yaml` and the instructions from `prompts.txt`.
- Keep your API key in a local `.env` file, which Git ignores.

## Requirements

- Windows 10 or 11
- Python 3.10 or newer
- A Groq account and your own Groq API key
- Internet access while using the analyzer

## Setup on Windows

1. **Install Python if needed.** Download Python 3.10 or newer from [python.org](https://www.python.org/downloads/). During installation, select **Add Python to PATH**. Open a new PowerShell window and check with `py --version`.

2. **Open this project folder in VS Code.** Open a VS Code terminal using **Terminal > New Terminal**. The terminal should be in the folder containing `app.py`.

3. **Create a virtual environment.** In PowerShell, run:

   ```powershell
   py -m venv .venv
   ```

4. **Activate it.** In PowerShell, run:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt instead and run:

   ```bat
   .venv\Scripts\activate.bat
   ```

5. **Install the project packages.** With the virtual environment active, run:

   ```powershell
   py -m pip install -r requirements.txt
   ```

6. **Create your local environment file.** In PowerShell, run:

   ```powershell
   if (-not (Test-Path .env)) { Copy-Item .env.example .env }
   ```

   If `.env` already exists, keep it and do not overwrite it. Otherwise, open the new `.env` in VS Code and replace `your_groq_api_key_here` with your own key from the Groq Console. Keep the key private. Do not put it in `app.py`, screenshots, or GitHub. The local `.env` file is excluded from Git; `.env.example` contains only a placeholder.

7. **Run the app.** In the same terminal, run:

   ```powershell
   streamlit run app.py
   ```

   Streamlit will show a local address in the terminal and usually open the app in your browser. Leave the terminal running while you use the app. Press `Ctrl+C` in that terminal to stop it.

## Try It

Enter one example at a time and select **Analyze Sentiment**:

- Positive: `The staff were kind, and the food was delicious.`
- Negative: `The package arrived late and the item was damaged.`
- Neutral: `The store opens at 9 AM and is located on Pine Street.`

Your completed results appear in **Analysis history** until the Streamlit session ends. Select **Clear history** to remove them earlier.

## Model setting

The model is set in `config.yaml` (`openai/gpt-oss-20b`). Groq changes model availability over time and by account. If the request reports a model error, check Groq's [supported models](https://console.groq.com/docs/models) and replace the `model` value in `config.yaml` with an available chat model. No application code change is needed.

## Upload to GitHub Safely

1. Confirm that your API key is in `.env`, not in a source file. The `.gitignore` file excludes `.env` and common secret files.
2. In the project terminal, run `git status` and verify that `.env` is **not** listed. If it is listed, stop and do not upload it.
3. Initialize and commit the project:

   ```powershell
   git init
   git add .
   git status
   git commit -m "Add AI Sentiment Analyzer"
   ```

4. Create an empty repository on GitHub. Follow GitHub's instructions to connect this folder to that repository and push the commit. Before pushing, check `git status` once more to make sure `.env` is not staged.

If an API key is ever uploaded accidentally, revoke it in Groq immediately and create a new one. Removing a key in a later commit does not erase it from Git history.

## How It Works

Streamlit displays the text box and results in a browser. When you submit text, Python reads `GROQ_API_KEY` from your local `.env`, sends the text and the instructions in `prompts.txt` to the Groq API, then checks that the answer is valid JSON with an allowed sentiment and 3 to 5 keywords. The result is shown and kept in Streamlit's session state; no database is used.
