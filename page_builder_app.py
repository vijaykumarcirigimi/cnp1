import streamlit as st
import os
import zipfile
import xml.etree.ElementTree as ET
import json
import cssutils
import logging
import google.generativeai as genai
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Disable CSS parsing warnings
cssutils.log.setLevel(logging.CRITICAL)

# Load env variables (if standard .env is used)
load_dotenv()

st.set_page_config(page_title="Edstellar Page Builder", page_icon="📝", layout="wide")

def extract_docx_text_from_bytes(file_bytes):
    """Extracts raw text from a docx file byte stream."""
    text = []
    with zipfile.ZipFile(file_bytes) as docx:
        xml_content = docx.read('word/document.xml')
        tree = ET.XML(xml_content)
        for node in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
            if node.text:
                text.append(node.text)
    return "\n".join(text)

def scope_selectorList(selectorList, scope_id):
    """Prefixes generic CSS rules with a distinct wrapper ID to prevent bleeding."""
    for selector in selectorList:
        text = selector.selectorText
        # Preserve root bindings but scope them inside the module block
        if text.startswith(':root') or text.startswith('body') or text.startswith('html'):
            selector.selectorText = text.replace(':root', f'#{scope_id}').replace('body', f'#{scope_id}').replace('html', f'#{scope_id}')
        else:
            selector.selectorText = f"#{scope_id} {text}"

def scope_module_css(html_content, scope_id):
    """Takes isolated raw HTML, scopes its <style> tags, and wraps it in a <div>."""
    soup = BeautifulSoup(html_content, "html.parser")
    styles = []
    for style in soup.find_all('style'):
        sheet = cssutils.parseString(style.string)
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                scope_selectorList(rule.selectorList, scope_id)
            elif rule.type == rule.MEDIA_RULE:
                for inner_rule in rule.cssRules:
                    if inner_rule.type == inner_rule.STYLE_RULE:
                        scope_selectorList(inner_rule.selectorList, scope_id)
        styles.append(sheet.cssText.decode('utf-8'))
        style.decompose() # Remove the old style

    body = soup.find('body')
    if body:
        inner_html = "".join([str(c) for c in body.contents])
    else:
        inner_html = str(soup)

    final_css = "\n".join(styles)
    scoped_html = f'<style>\n{final_css}\n</style>\n<div id="{scope_id}">\n{inner_html}\n</div>'
    return scoped_html

def get_mapping_from_gemini(docx_text):
    """Asks Gemini to extract the page flow architecture table into a JSON list."""
    prompt = f"""
    You are an AI architect parsing a Consulting Page Design developer reference.
    Below is the raw extracted text from a Microsoft Word document.
    Find the 'PAGE FLOW OVERVIEW' table or section. It should map section names to HTML module names (like 'edstellar-hero-classic-split.html').
    Return a strictly formatted JSON list of strings containing the exact filenames in chronological order.
    Do NOT return markdown blocks (no ```json), just the raw list array like ["file1.html", "file2.html"].
    
    TEXT:
    {docx_text[:15000]}  # passing first 15k chars is usually enough for the TOC
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text.strip())
    except Exception as e:
        st.error(f"Failed to parse JSON list from Gemini: {response.text}")
        return []

def inject_content_with_gemini(module_filename, scoped_html, docx_text, index):
    """Uses Gemini to intelligently substitute the boilerplate text in the scoped HTML with correct text."""
    prompt = f"""
    I am building an automated landing page.
    Below is the raw text of the entire design requirement document, and the specific HTML boilerplate for Section {index+1} (Module: {module_filename}).
    
    Your job is to read the document, find the specific content intended for Section {index+1} (or content that logically maps to the module `{module_filename}`), and inject it into the HTML provided.
    
    RULES:
    1. DO NOT change any CSS classes, inline styles, IDs, or structural div layouts.
    2. REPLACE placeholders (like "Generic Headline", "Placeholder paragraph content") with the specific text from the document.
    3. Return ONLY the final valid HTML block. Do NOT wrap in ```html markdown blocks. Do not add any conversational text.
    
    DOCX TEXT:
    {docx_text}

    SCOPED BOILERPLATE HTML TO INJECT:
    {scoped_html}
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    
    html = response.text.strip()
    if html.startswith("```html"):
        html = html[7:]
    if html.endswith("```"):
        html = html[:-3]
    return html.strip()


# --- Streamlit UI ---

st.title("🚀 Edstellar AI Page Builder")
st.markdown("Upload a Consulting Page `.docx` Developer Reference to automatically build the final stitched HTML.")

# API Key Handling
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")
else:
    st.sidebar.success("Gemini API Key detected via Environment!")

if api_key:
    genai.configure(api_key=api_key)

uploaded_file = st.file_uploader("Upload Developer Reference Document (.docx)", type="docx")

if uploaded_file is not None and api_key:
    if st.button("Build Landing Page"):
        progress_bar = st.progress(0)
        status = st.empty()
        
        status.info("Extracting text from DOCX...")
        docx_text = extract_docx_text_from_bytes(uploaded_file)
        
        status.info("Asking Gemini to extract Page Flow Overview...")
        module_sequence = get_mapping_from_gemini(docx_text)
        
        if not module_sequence:
            st.error("Could not extract module sequence. Ensure document contains a typical mapping table.")
            st.stop()
            
        st.write("### Identified Module Flow:")
        st.json(module_sequence)
        
        library_path = os.path.join(os.getcwd(), "Library")
        if not os.path.exists(library_path):
            st.error(f"Library folder not found at {library_path}. Ensure it exists next to this app.")
            st.stop()
            
        final_blocks = []
        
        # We need a generic wrapper
        master_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Consulting Page | Edstellar</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
"""
        master_footer = "</body>\n</html>"
        
        for idx, module_file in enumerate(module_sequence):
            status.info(f"Processing Block {idx+1}/{len(module_sequence)}: {module_file}")
            progress_bar.progress((idx) / len(module_sequence))
            
            file_p = os.path.join(library_path, module_file)
            if not os.path.exists(file_p):
                # Perhaps handle slight name mismatches
                st.warning(f"Could not find {module_file} in Library. Skipping.")
                continue
                
            with open(file_p, 'r', encoding='utf-8') as f:
                raw_html = f.read()
                
            # 1. Scope the CSS exclusively for this module
            scope_id = f"section_{idx:02d}_generated"
            scoped_html = scope_module_css(raw_html, scope_id)
            
            # 2. Ask Gemini to perform text injection 
            try:
                injected_html = inject_content_with_gemini(module_file, scoped_html, docx_text, idx)
                final_blocks.append(injected_html)
            except Exception as e:
                st.error(f"Error injecting {module_file}: {e}")
                final_blocks.append(scoped_html) # fallback to boilerplate
                
        progress_bar.progress(1.0)
        status.success("Page Successfully Built!")
        
        final_output = master_header + "\n".join(final_blocks) + "\n" + master_footer
        
        st.download_button(
            label="Download Final HTML",
            data=final_output,
            file_name="generated-landing-page.html",
            mime="text/html"
        )
        
elif uploaded_file is not None and not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to run the builder.")
