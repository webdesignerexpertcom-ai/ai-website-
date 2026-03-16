import streamlit as st
import os
import re
from huggingface_hub import InferenceClient
import time

st.set_page_config(layout="wide", page_title="AI Website Generator")

# Page title
st.title("⚡ AI Website Generator")

# Custom UI Styling
st.markdown("""
<style>
/* Dark Modern UI Styling */
.stApp {
    background-color:#020617;
    color: white;
}
textarea {
    background:#1e293b !important;
    color:white !important;
    border: 1px solid #334155;
    border-radius: 8px;
}
/* Style the generate button */
div.stButton > button:first-child {
    background:#6366f1;
    color:white;
    border-radius:8px;
    border:none;
    padding: 0.5rem 1rem;
    font-weight: 600;
}
div.stButton > button:hover {
    background:#4f46e5;
    color:white;
}
</style>
""", unsafe_allow_html=True)


# Layout: Prompt Box | Website Preview
col1, col2 = st.columns([1,2])

with col1:
    st.subheader("Enter Website Requirements")
    prompt = st.text_area(
        "Describe your website",
        placeholder="Example: A modern landing page for a fitness app with hero section, pricing cards and contact form.",
        height=200
    )
    generate = st.button("Generate Website")

with col2:
    st.subheader("Website Preview")
    preview = st.empty()

def extract_code(text, lang):
    pattern = rf"```{lang}\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

if generate and prompt:
    try:
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

        with st.spinner("Generating beautiful website..."):
            code = None
            for i in range(5):
                try:
                    response = client.chat_completion(
                        messages=[
                            {"role": "system", "content": "You are an expert web developer."},
                            {"role": "user", "content": system_prompt}
                        ],
                        max_tokens=4000
                    )
                    code = response.choices[0].message.content
                    break
                except Exception as e:
                    if i == 4:
                        st.error(f"Failed after 5 attempts: {str(e)}")
                        st.stop()
                    time.sleep(5)
            
            if code:
                # Extract parts
                html_code = extract_code(code, "html")
                css_code = extract_code(code, "css")
                js_code = extract_code(code, "javascript")
                
                # If extraction fails, try to fallback directly
                if not html_code and not css_code and not js_code:
                    html_code = code.replace("```html", "").replace("```", "")
                    css_code = ""
                    js_code = ""

                # Save generated files
                os.makedirs("generated", exist_ok=True)
                
                # We need a proper base HTML layout if the model just returns a snippet 
                # but usually GPT-4 returns a full document. Check for <html>
                if "<html>" not in html_code.lower() and "<html" not in html_code.lower():
                    html_code = f"<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n<title>Generated Site</title>\n</head>\n<body>\n{html_code}\n</body>\n</html>"

                with open("generated/index.html","w", encoding="utf-8") as f:
                    f.write(html_code)
                with open("generated/style.css","w", encoding="utf-8") as f:
                    f.write(css_code)
                with open("generated/script.js","w", encoding="utf-8") as f:
                    f.write(js_code)
                    
                # Combine codes for streamlit preview
                combined_html = html_code
                if css_code:
                    if "</head>" in combined_html.lower():
                        combined_html = re.sub(r'</head>', f'<style>{css_code}</style></head>', combined_html, flags=re.IGNORECASE)
                    else:
                        combined_html = f"<style>{css_code}</style>" + combined_html
                        
                if js_code:
                    if "</body>" in combined_html.lower():
                        combined_html = re.sub(r'</body>', f'<script>{js_code}</script></body>', combined_html, flags=re.IGNORECASE)
                    else:
                        combined_html = combined_html + f"<script>{js_code}</script>"

                # Preview
                import streamlit.components.v1 as components
                with preview.container():
                    components.html(combined_html, height=600, scrolling=True)

                st.success("Website generated successfully!")

                # Expandable code section
                st.markdown("### HTML / CSS / JS Code Output")
                with st.expander("View Source Code"):
                    if html_code:
                        st.markdown("**index.html**")
                        st.code(html_code, language="html")
                    if css_code:
                        st.markdown("**style.css**")
                        st.code(css_code, language="css")
                    if js_code:
                        st.markdown("**script.js**")
                        st.code(js_code, language="javascript")
                    if not html_code and not css_code and not js_code:
                        st.code(code)

                # Download section
                st.markdown("### Download")
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    with open("generated/index.html","rb") as f:
                        st.download_button("Download index.html", f, "index.html", key="dl_html", mime="text/html")
                with col_btn2:
                    with open("generated/style.css","rb") as f:
                        st.download_button("Download style.css", f, "style.css", key="dl_css", mime="text/css")
                with col_btn3:
                    with open("generated/script.js","rb") as f:
                        st.download_button("Download script.js", f, "script.js", key="dl_js", mime="text/javascript")

    except Exception as e:
        st.error(f"Error: {str(e)}")
