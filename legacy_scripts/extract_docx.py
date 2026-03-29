import zipfile
import xml.etree.ElementTree as ET

def extract_text(docx_path):
    with zipfile.ZipFile(docx_path) as docx:
        xml_content = docx.read('word/document.xml')
    tree = ET.fromstring(xml_content)
    # The namespace for Word processing XML
    ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    
    # Extract all text nodes
    texts = []
    for node in tree.iter(ns + 't'):
        if node.text:
            texts.append(node.text)
    
    return '\n'.join(texts)

def main():
    text = extract_text('assessment-development-centers-developer-reference.docx')
    with open('docx_content.txt', 'w', encoding='utf-8') as f:
        f.write(text)

main()
