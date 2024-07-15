import json
import base64
import io
import zipfile
import PyPDF2

def parse_page_ranges(pages_str):
    pages = set()
    for part in pages_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return sorted(pages)

def handler(event, context):
    try:
        body = json.loads(event['body'])
        pdf_base64 = body['pdf']
        output_pages = body['outputPages']

        pdf_bytes = base64.b64decode(pdf_base64)
        pdf_buffer = io.BytesIO(pdf_bytes)

        pdf = PyPDF2.PdfReader(pdf_buffer)
        output_files = []

        for output_file, pages_str in output_pages.items():
            pdf_writer = PyPDF2.PdfWriter()
            pages = parse_page_ranges(pages_str)

            for page_num in pages:
                if 1 <= page_num <= len(pdf.pages):
                    page = pdf.pages[page_num - 1]
                    pdf_writer.add_page(page)

            output_buffer = io.BytesIO()
            pdf_writer.write(output_buffer)
            output_buffer.seek(0)
            output_files.append((output_file, output_buffer.getvalue()))

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for filename, file_bytes in output_files:
                zip_file.writestr(filename, file_bytes)

        zip_base64 = base64.b64encode(zip_buffer.getvalue()).decode('utf-8')

        return {
            'statusCode': 200,
            'body': json.dumps({'zip': zip_base64}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
