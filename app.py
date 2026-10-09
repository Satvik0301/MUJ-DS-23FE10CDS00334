"""A simple Streamlit app that analyzes sentiment with the Groq API."""

import json
import os
from pathlib import Path

import streamlit as st
import yaml
from dotenv import load_dotenv
from groq import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    Groq,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)


PROJECT_DIR = Path(__file__).parent
ALLOWED_SENTIMENTS = {"Positive", "Negative", "Neutral"}


def load_settings():
    """Load and validate the application settings from config.yaml."""
    config_path = PROJECT_DIR / "config.yaml"
    with config_path.open("r", encoding="utf-8") as config_file:
        settings = yaml.safe_load(config_file)

    if not isinstance(settings, dict):
        raise ValueError("config.yaml must contain a YAML mapping.")

    model = settings.get("model")
    temperature = settings.get("temperature")
    max_tokens = settings.get("max_tokens")
    max_input_length = settings.get("max_input_length")

    if not isinstance(model, str) or not model.strip():
        raise ValueError("Set a model name in config.yaml.")
    if not isinstance(temperature, (int, float)) or not 0 <= temperature <= 2:
        raise ValueError("The temperature in config.yaml must be between 0 and 2.")
    if not isinstance(max_tokens, int) or max_tokens < 1:
        raise ValueError("The max_tokens setting in config.yaml must be a positive integer.")
    if not isinstance(max_input_length, int) or max_input_length < 1:
        raise ValueError("The max_input_length setting in config.yaml must be a positive integer.")

    # Keep the requested hard limit even if someone raises the config value.
    settings["max_input_length"] = min(max_input_length, 5000)
    return settings


def load_prompt():
    """Read the analysis instructions from prompts.txt."""
    with (PROJECT_DIR / "prompts.txt").open("r", encoding="utf-8") as prompt_file:
        return prompt_file.read().strip()


def validate_result(response_text):
    """Parse the model response and check that it has the expected fields."""
    result = json.loads(response_text)
    if not isinstance(result, dict):
        raise ValueError("The response must be a JSON object.")

    sentiment = result.get("sentiment")
    explanation = result.get("explanation")
    keywords = result.get("keywords")

    if sentiment not in ALLOWED_SENTIMENTS:
        raise ValueError("The response did not contain a valid sentiment label.")
    if not isinstance(explanation, str) or not explanation.strip():
        raise ValueError("The response did not contain a short explanation.")
    if not isinstance(keywords, list) or not 3 <= len(keywords) <= 5:
        raise ValueError("The response must contain 3 to 5 keywords.")
    if any(not isinstance(word, str) or not word.strip() for word in keywords):
        raise ValueError("The response contains an invalid keyword.")

    return {
        "sentiment": sentiment,
        "explanation": explanation.strip(),
        "keywords": [word.strip() for word in keywords],
    }


def analyze_text(text, settings, prompt, api_key):
    """Send the text to Groq and return a validated analysis."""
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=settings["model"],
        temperature=settings["temperature"],
        max_tokens=settings["max_tokens"],
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )

    response_text = completion.choices[0].message.content
    if not response_text:
        raise ValueError("The model returned an empty response.")
    return validate_result(response_text)


def groq_error_message(error, model):
    """Return a useful message without exposing provider response details."""
    if isinstance(error, AuthenticationError):
        return "Groq rejected the API key. Check GROQ_API_KEY in the project-root .env file, then restart the app."
    if isinstance(error, PermissionDeniedError):
        return "This Groq account or API key does not have access to the configured model. Check the model in config.yaml."
    if isinstance(error, NotFoundError):
        return f"The configured Groq model '{model}' was not found. Choose an available chat model in config.yaml."
    if isinstance(error, RateLimitError):
        return "Groq rate limit or usage quota reached. Wait and try again, or check the limits for your Groq account."
    if isinstance(error, APITimeoutError):
        return "Groq took too long to respond. Check your internet connection and try again."
    if isinstance(error, APIConnectionError):
        return "Could not connect to Groq. Check your internet connection and try again."
    if isinstance(error, BadRequestError):
        details = getattr(error, "body", None)
        if isinstance(details, dict):
            details = details.get("error", details)
        if isinstance(details, dict):
            code = str(details.get("code", "")).lower()
            message = str(details.get("message", "")).lower()
            model_error_codes = {"model_not_found", "model_decommissioned", "model_not_available"}
            if code in model_error_codes or "model does not exist" in message or "model is unavailable" in message:
                return f"The configured Groq model '{model}' is unavailable. Choose an available chat model in config.yaml."
        return "Groq rejected the request. Check the model and its supported request settings in config.yaml."
    if isinstance(error, APIStatusError):
        return f"Groq returned an API error (HTTP {error.status_code}). Try again later."
    return "The Groq request failed unexpectedly. Check your settings and internet connection, then try again."


def show_analysis(analysis):
    """Display the result with a visual cue for each sentiment."""
    st.subheader("Analysis")
    sentiment = analysis["sentiment"]
    if sentiment == "Positive":
        st.success(f"Sentiment: {sentiment}")
    elif sentiment == "Negative":
        st.error(f"Sentiment: {sentiment}")
    else:
        st.info(f"Sentiment: {sentiment}")

    st.write(analysis["explanation"])
    st.markdown("**Important keywords**")
    st.write(", ".join(analysis["keywords"]))


load_dotenv(PROJECT_DIR / ".env", override=True)
st.set_page_config(page_title="AI Sentiment Analyzer", page_icon="A", layout="centered")
st.title("AI Sentiment Analyzer")
st.write("Enter a sentence, review, or paragraph to identify its overall sentiment.")

try:
    settings = load_settings()
    prompt = load_prompt()
except (OSError, ValueError, yaml.YAMLError):
    st.error("The app could not load config.yaml or prompts.txt. Check that both files exist and are valid.")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []

max_input_length = settings["max_input_length"]
user_text = st.text_area(
    "Text to analyze",
    height=180,
    max_chars=max_input_length,
    placeholder="For example: The delivery was quick and the product works perfectly.",
)
st.caption(f"{len(user_text)} / {max_input_length} characters")

if st.button("Analyze Sentiment", type="primary"):
    if not user_text.strip():
        st.error("Please enter some text before analyzing.")
    elif len(user_text) > max_input_length:
        st.error(f"Please keep your text to {max_input_length:,} characters or fewer.")
    else:
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key:
            st.error("Groq API key is missing. Add GROQ_API_KEY to your local .env file, then restart the app.")
        else:
            try:
                analysis = analyze_text(user_text, settings, prompt, api_key)
            except json.JSONDecodeError:
                st.error("The model response was not valid JSON. Please try again.")
            except ValueError as error:
                st.error(f"The model response could not be used: {error}")
            except (APIStatusError, APIConnectionError) as error:
                st.error(groq_error_message(error, settings["model"]))
            except Exception:
                # Do not display provider exception details, which could contain sensitive information.
                st.error("The Groq request failed unexpectedly. Check your settings and internet connection, then try again.")
            else:
                show_analysis(analysis)
                st.session_state.history.insert(
                    0,
                    {"text": user_text, **analysis},
                )

st.divider()
history_header, clear_column = st.columns([4, 1])
with history_header:
    st.subheader("Analysis history")
with clear_column:
    if st.button("Clear history", disabled=not st.session_state.history):
        st.session_state.history.clear()
        st.rerun()

if st.session_state.history:
    for index, item in enumerate(st.session_state.history, start=1):
        preview = item["text"].replace("\n", " ").strip()
        if len(preview) > 60:
            preview = f"{preview[:57]}..."
        with st.expander(f"{item['sentiment']} | {preview}", expanded=index == 1):
            st.write(item["text"])
            st.write(item["explanation"])
            st.caption(f"Keywords: {', '.join(item['keywords'])}")
else:
    st.caption("Your completed analyses will appear here for this session.")
