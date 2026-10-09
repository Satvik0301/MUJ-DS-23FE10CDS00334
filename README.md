# AI Sentiment Analyzer

An AI-powered sentiment analysis application built with Python, Streamlit, and the Groq API. It classifies text as Positive, Negative, or Neutral and provides an explanation of the result.

## Student Details

- Name: Satvik Kumar
- Registration Number: 23FE10CDS00334
- Branch: B.Tech CDS
- Batch: Class E/subject section B
- GitHub Username: Satvik0301

## Project Details

- Project Title: AI Sentiment Analyzer
- Training Program: Class E Training Program
- Project Type: Individual NLP Project

## Project Description

AI Sentiment Analyzer is a Python-based application that uses a Large Language Model (LLM) through the Groq API to analyze the sentiment expressed in a given piece of text.

The application classifies the input as Positive, Negative, or Neutral and provides a brief explanation of the predicted sentiment. It also identifies relevant keywords and maintains a session history of previously analyzed text.

The project demonstrates the practical application of Natural Language Processing (NLP), large language models, API integration, and interactive web application development.

## Features

- **Sentiment Classification:** Classifies text as Positive, Negative, or Neutral.
- **Sentiment Explanation:** Provides an explanation for the predicted sentiment.
- **Keyword Identification:** Highlights relevant keywords from the input.
- **Session History:** Keeps a history of analyses during the current session.
- **Interactive Interface:** Provides a simple web interface using Streamlit.
- **LLM Integration:** Uses the Groq API to process text and generate analysis results.

## Technologies Used

- **Python** — Core programming language
- **Streamlit** — Interactive web application interface
- **Groq API** — Large language model integration
- **python-dotenv** — Environment variable management
- **PyYAML** — YAML configuration file handling

## Project Structure

- `app.py` — Main application and user interface
- `prompts.txt` — Prompt instructions for sentiment analysis
- `config.yaml` — Application configuration
- `.env.example` — Example environment variable configuration
- `.gitignore` — Specifies files excluded from version control
- `requirements.txt` — Python dependencies

## Installation and Setup

### Prerequisites

- Python installed on your system
- Git installed on your system
- A Groq API key

### 1. Clone the Repository

git clone https://github.com/Satvik0301/AI-Sentiment-Analyzer.git
cd AI-Sentiment-Analyzer

### 2. Create a Virtual Environment

On Windows:

python -m venv .venv

### 3. Install Dependencies

On Windows:

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

### 4. Configure Environment Variables

1. Create a `.env` file in the project root directory.
2. Use `.env.example` as a reference for the required environment variables.
3. Add your own Groq API key using the variable name expected by the application.

**Security note:** Do not commit your `.env` file or publish your API key. Keep `.env` excluded through `.gitignore`.

### 5. Run the Application

On Windows:

.\.venv\Scripts\python.exe -m streamlit run app.py

Streamlit will display a local URL in the terminal. Open that URL in your browser to use the application.

## Testing

The application has been tested with positive, negative, and neutral text inputs to check its sentiment classification functionality.

Testing should also cover the explanation, keyword identification, and session history features.

## Learning Outcomes

This project provides practical experience with:

- Natural Language Processing and sentiment analysis
- Integrating a large language model through an API
- Building interactive applications with Streamlit
- Managing API keys through environment variables
- Organizing and maintaining a Python project using Git and GitHub

## GitHub Repository

[AI Sentiment Analyzer — GitHub Repository](https://github.com/Satvik0301/AI-Sentiment-Analyzer)
