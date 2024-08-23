import PyPDF2
import os

def split_pdf(input_pdf_path, output_folder):
    with open(input_pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        num_pages = reader.numPages
        for i in range(0, num_pages, 3):
            writer = PyPDF2.PdfFileWriter()
            for page_num in range(i, min(i + 3, num_pages)):
                writer.addPage(reader.getPage(page_num))
            output_pdf_path = os.path.join(output_folder, f'output_{i // 3 + 1}.pdf')
            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)

if __name__ == "__main__":
    input_pdf_path = input("Enter the path to the PDF file: ")
    output_folder = input("Enter the path to the output folder: ")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    split_pdf(input_pdf_path, output_folder)
    print("PDF split successfully.")
