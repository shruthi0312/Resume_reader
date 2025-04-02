import docx
from PyPDF2 import PdfReader

class DocumentReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_doc(self):
        doc = docx.Document(self.file_path)
        return [para.text for para in doc.paragraphs]  

    def read_pdf(self):
        try:
            with open(self.file_path, "rb") as file:  # Fixed indentation
                pdf_reader = PdfReader(file)
                return [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
        except FileNotFoundError:
            return ["Error: File not found!"]

    def extract_text(self):
        if self.file_path.endswith(('.doc', '.docx')):
            return self.read_doc()  
        elif self.file_path.endswith('.pdf'):
            return self.read_pdf()  
        else:
            return ["Unsupported format."]  

    def save_text(self, output_file):  
        text = self.extract_text()
        with open(output_file, "w", encoding="utf-8") as file:
            for line in text: 
                file.write(line + "\n")
        return f"Text saved to {output_file}"


def doJob():
    return "This is extracted text"
    # reader = DocumentReader("resumes/Deepak_12Yrs_SalesforceBSA.docx")  
    # print(reader.extract_text())    
    # reader.save_text("New_file1.txt") 

# reader = DocumentReader("resumes/Deepak_12Yrs_SalesforceBSA.docx")  
# print(reader.extract_text())    
# reader.save_text("New_file1.txt")  
