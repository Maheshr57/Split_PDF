import os
from flask import Flask, request, send_from_directory, redirect, url_for
import fitz  # PyMuPDF

app = Flask(__name__)

def get_downloads_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def split_pdf(file_path, split_points):
    doc = fitz.open(file_path)
    download_folder = get_downloads_folder()
    
    split_files = []
    start = 0
    for i, end in enumerate(split_points):
        split_doc = fitz.open()  # Create a new PDF document
        for page_num in range(start, end):
            split_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        split_file_path = os.path.join(download_folder, f"pdf-split-{i+1}.pdf")
        split_doc.save(split_file_path)
        split_files.append(split_file_path)
        start = end
    
    # Automatically add remaining pages to the last split
    if start < doc.page_count:
        split_doc = fitz.open()
        for page_num in range(start, doc.page_count):
            split_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        split_file_path = os.path.join(download_folder, f"pdf-split-{len(split_points)+1}.pdf")
        split_doc.save(split_file_path)
        split_files.append(split_file_path)
    
    return split_files

@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h2>Upload a PDF to Split</h2>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="application/pdf">
                <br><br>
                <label for="split_points">Enter page numbers to split at (comma-separated):</label><br>
                <input type="text" id="split_points" name="split_points">
                <br><br>
                <input type="submit" value="Upload and Split">
            </form>
        </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    split_points = request.form['split_points']
    if file.filename == '' or split_points == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(get_downloads_folder(), file.filename)
        file.save(file_path)
        
        # Parse split points from input
        split_points = [int(p.strip()) for p in split_points.split(',') if p.strip().isdigit()]
        
        # Split PDF
        split_files = split_pdf(file_path, split_points)
        
        download_links = [url_for('download_file', filename=os.path.basename(f)) for f in split_files]
        links_html = ''.join([f'<li><a href="{link}">{os.path.basename(link)}</a></li>' for link in download_links])
        
        return f'''
        <html>
            <body>
                <h2>Download Split PDFs</h2>
                <ul>
                    {links_html}
                </ul>
            </body>
        </html>
        '''
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(get_downloads_folder(), filename)

if __name__ == "__main__":
    app.run(debug=True)
