from flask import Flask, request, jsonify, send_file
import PyPDF2
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/split-pdf', methods=['POST'])
def split_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files['pdf']
    output_pages = json.loads(request.form['outputPages'])

    # Save the uploaded PDF
    input_path = 'input.pdf'
    pdf_file.save(input_path)

    try:
        with open(input_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            
            for output_file, pages_str in output_pages.items():
                pdf_writer = PyPDF2.PdfWriter()
                
                # Parse page ranges
                pages = parse_page_ranges(pages_str)
                
                for page_num in pages:
                    if 1 <= page_num <= len(pdf.pages):
                        page = pdf.pages[page_num - 1]
                        pdf_writer.add_page(page)
                    else:
                        print(f"Warning: Page {page_num} is out of range and will be skipped.")
                
                with open(output_file, 'wb') as output:
                    pdf_writer.write(output)

        # Clean up the input file
        os.remove(input_path)

        return jsonify({"message": "PDF split successfully. Check your downloads folder for the output files."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def parse_page_ranges(pages_str):
    pages = set()
    for part in pages_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return sorted(pages)

if __name__ == '__main__':
    app.run()