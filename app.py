import streamlit as st
import os
import re
from components.ai_logic import generate_website, extract_code, save_generated_files
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="AI Website Generator")

# Page title
st.title("⚡ AI Website Generator")

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

if generate and prompt:
    try:
        with st.spinner("Generating beautiful website..."):
            code = generate_website(prompt)
            
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

                # Save generated files using the component logic
                html_code, css_code, js_code = save_generated_files(html_code, css_code, js_code)
                    
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
                    with open("data/generated/index.html","rb") as f:
                        st.download_button("Download index.html", f, "index.html", key="dl_html", mime="text/html")
                with col_btn2:
                    with open("data/generated/style.css","rb") as f:
                        st.download_button("Download style.css", f, "style.css", key="dl_css", mime="text/css")
                with col_btn3:
                    with open("data/generated/script.js","rb") as f:
                        st.download_button("Download script.js", f, "script.js", key="dl_js", mime="text/javascript")

    except Exception as e:
        st.error(f"Error: {str(e)}")
