# AI Sentiment Analyzer

A simple NLP project that uses the Groq API to analyze text sentiment.

## Features
- Classifies text as Positive, Negative, or Neutral
- Provides a short explanation of the result
- Extracts important keywords
- Keeps a history of previous analyses during the session

## Technologies Used
- Python
- Streamlit
- Groq API

## Setup

### 1. Clone the repository

    git clone https://github.com/Satvik0301/AI-Sentiment-Analyzer.git
    cd AI-Sentiment-Analyzer

### 2. Create a virtual environment

    python -m venv .venv

### 3. Install dependencies

    .\.venv\Scripts\python.exe -m pip install -r requirements.txt

### 4. Configure your API key

Copy .env.example to .env and add your Groq API key to the .env file.

    GROQ_API_KEY=your_api_key_here

### 5. Run the application

    .\.venv\Scripts\python.exe -m streamlit run app.py

## Project Files
- app.py – Main application
- prompts.txt – LLM prompt instructions
- config.yaml – Model and application settings
- .env.example – Example API configuration
- requirements.txt – Required Python packages

Note: Keep your API key private. Never upload your .env file to GitHub.