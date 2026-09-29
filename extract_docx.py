import zipfile
import xml.etree.ElementTree as ET
import re

def extract_text_from_docx(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        xml_content = zip_ref.read('word/document.xml')
    
    root = ET.fromstring(xml_content)
    
    # Define namespace
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }
    
    # Extract all text elements
    texts = []
    for elem in root.iter():
        if elem.tag.endswith('}t'):
            if elem.text:
                texts.append(elem.text)
    
    return ' '.join(texts)

if __name__ == '__main__':
    text = extract_text_from_docx('Basic Identities reformatted.docx')
    with open('extracted_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Text saved to extracted_text.txt")
