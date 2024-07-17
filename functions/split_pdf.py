import PyPDF2
import os

def split_pdf(file_path, output_dir):
    pdf = PyPDF2.PdfFileReader(file_path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output_filename = os.path.join(output_dir, f'page_{page+1}.pdf')
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

    print(f'Split PDF into {pdf.getNumPages()} pages.')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Split a PDF into individual pages.')
    parser.add_argument('file', help='PDF file to split')
    parser.add_argument('output_dir', help='Directory to save individual pages')
    args = parser.parse_args()

    split_pdf(args.file, args.output_dir)
