import PyPDF2
import re
import os

def read_pdf(file_path):
    result = []
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                content = page.extract_text()
                result.append(content)
        os.remove(file_path)  # Remove the PDF file after reading
        dir_path = os.path.dirname(file_path)
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            os.remove(file_path)
        return result
    except Exception as e:
        print(f"An error occurred while reading the PDF file: {e}")
    finally:
        try:
            os.rmdir(os.path.dirname(file_path))  # Remove the directory containing the PDF file
        except OSError as e:
            print(f"Error removing directory: {e}")

def remove_punctuation(text):
    accent_map = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ã': 'a', 'õ': 'o', 'â': 'a', 'ê': 'e', 'î': 'i',
        'ô': 'o', 'û': 'u', 'à': 'a', 'è': 'e', 'ì': 'i',
        'ò': 'o', 'ù': 'u', 'ç': 'c'
    }

    cleaned_text = ""
    for char in text:
        cleaned_text += accent_map.get(char, char)
    return cleaned_text

def extract_info(input_str):
    # Remove punctuation and convert to lowercase
    clean_input = remove_punctuation(input_str).lower()
    
    # Define regular expressions to extract information
    cep_regex = re.compile(r'cep:\s?(\S+)', re.IGNORECASE)
    area_territorial_regex = re.compile(r'área territorial:\s?(\S+)', re.IGNORECASE)
    testada_regex = re.compile(r'testada:\s?(\S+)', re.IGNORECASE)
    area_predial_regex = re.compile(r'área predial:\s?(\S+)', re.IGNORECASE)

    # Find matches using regular expressions
    cep_match = cep_regex.search(clean_input)
    area_territorial_match = area_territorial_regex.search(clean_input)
    testada_match = testada_regex.search(clean_input)
    area_predial_match = area_predial_regex.search(clean_input)

    # Initialize an empty dictionary to store extracted information
    extracted_info = {}

    # Extract and store information if matches are found
    if cep_match:
        cep = cep_match.group(1).replace("-", "").replace(".", "")  # Remove hyphen and dot from CEP
        extracted_info["CEPImovel"] = str(cep)
    if area_territorial_match:
        extracted_info["Area Territorial"] = str(area_territorial_match.group(1))
    if testada_match:
        extracted_info["Testada"] = str(testada_match.group(1))
    if area_predial_match:
        extracted_info["Area Predial"] = str(area_predial_match.group(1))

    return extracted_info
