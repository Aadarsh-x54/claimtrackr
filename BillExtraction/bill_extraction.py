from PyPDF2 import PdfReader
from openai import OpenAI
import yaml
import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(CURRENT_DIR, "config.yaml")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key and os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        api_key = data.get('OPENAI_API_KEY', 'KEY HERE')

def get_pdf_data(fpath):
    text = ""
    pdf = PdfReader(fpath)
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        page_text = page.extract_text()
        text += page_text
    return text

def get_llm():
    openai_client = OpenAI(
        api_key=api_key
    )

    return openai_client

def get_invoice_info_from_llm(data):
    llm = get_llm()
    prompt = "Act as an expert in extracting information from medical invoices. You are given with the invoice details of a patient. Go through the given document carefully and extract the 'disease' and the 'expense amount' from the data. Return the data in json format = {'disease':"",'expense':""}"
    messages=[
        {"role": "system", 
        "content": prompt}
        ]
    
    user_content = f"INVOICE DETAILS: {data}"

    messages.append({"role": "user", "content": user_content})

    response = llm.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.4,
                max_tokens=2500)
        
    data = json.loads(response.choices[0].message.content)

    return data

if __name__ == '__main__':
    bill_folder = os.path.join(CURRENT_DIR, "Bills")
    # Default to available sample bill in Bills directory
    bill_name = "Bodyache.pdf" if os.path.exists(os.path.join(bill_folder, "Bodyache.pdf")) else "MedicalBill1.pdf"

    bill_path = os.path.join(bill_folder, bill_name)
    if not os.path.exists(bill_path):
        print(f"{bill_path} does not exist. Please check the file location")
    else:
        bill_info = get_pdf_data(bill_path)
        invoice_details = get_invoice_info_from_llm(bill_info)

        print(f"Disease: {invoice_details['disease']}")
        print(f"Expense: {invoice_details['expense']}")
