---
title: AI Website Generator
emoji: ⚡
colorFrom: indigo
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---

# AI Website Generator

A powerful AI-powered website generator built with Streamlit and Hugging Face.

## Features
- Generate HTML/CSS/JS from natural language prompts.
- Live preview of the generated website.
- Downloadable source files.
- Modern and responsive UI.

## Local Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your secrets in `.streamlit/secrets.toml`:
   ```toml
   HF_TOKEN = "your_huggingface_token"
   ```
4. Run the app: `streamlit run app.py`
