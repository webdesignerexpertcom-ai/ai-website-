import re
import os
import time
from huggingface_hub import InferenceClient
import streamlit as st

def extract_code(text, lang):
    pattern = rf"```{lang}\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def generate_website(prompt):
    # Use Streamlit secrets for the Hugging Face API key
    hf_token = st.secrets["HF_TOKEN"]
    # Using a reliable coding model from Hugging Face
    client = InferenceClient(model="Qwen/Qwen2.5-Coder-32B-Instruct", token=hf_token)
    
    system_prompt = f"""
    Create a complete website based on this description:

    {prompt}

    Return modern and beautiful HTML, CSS, and JavaScript.
    Separate them clearly using markdown code blocks:
    ```html
    ...HTML code here...
    ```
    ```css
    ...CSS code here...
    ```
    ```javascript
    ...JS code here...
    ```
    Make sure to use an integrated approach where the HTML has proper semantics and class names for the CSS to target.
    Ensure the design is beautiful, modern, and fully functional.
    """

    for i in range(5):
        try:
            response = client.chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert web developer."},
                    {"role": "user", "content": system_prompt}
                ],
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            if i == 4:
                raise e
            time.sleep(5)
    return None

def save_generated_files(html_code, css_code, js_code):
    os.makedirs("data/generated", exist_ok=True)
    
    # Ensure proper base HTML layout
    if "<html>" not in html_code.lower() and "<html" not in html_code.lower():
        html_code = f"<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n<title>Generated Site</title>\n</head>\n<body>\n{html_code}\n</body>\n</html>"

    with open("data/generated/index.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    with open("data/generated/style.css", "w", encoding="utf-8") as f:
        f.write(css_code)
    with open("data/generated/script.js", "w", encoding="utf-8") as f:
        f.write(js_code)
    
    return html_code, css_code, js_code
