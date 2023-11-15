from flask import Flask, render_template, request, flash, redirect, url_for
import openpyxl
import csv
import os
import tempfile

app = Flask(__name__)
app.secret_key = 'maps'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'csv', 'xlsx', 'xlsm', 'xltx', 'xltm'}

UPLOAD_EXCEL = 'static/excel_data'
app.config['UPLOAD_EXCEL'] = UPLOAD_EXCEL

def process_excel_file(upload_file):
    try:
        workbook = openpyxl.load_workbook(upload_file)
        sheet = workbook.active
        district_counts = {}
        total_rows = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            total_rows += 1
            if len(row) == 2:
                district_name, phone_number = row
                if district_name in district_counts:
                    district_counts[district_name] += 1
                else:
                    district_counts[district_name] = 1
                print(total_rows)
            else:
                return None, f'Error: Row {total_rows} does not have exactly two values and format should be in District Name and Phone number'

        district_data = [{'name': district_name, 'count': count} for district_name, count in district_counts.items()]
        return district_data, None,total_rows
    except Exception as e:
        return None, f'An error occurred while processing the Excel file: {str(e)}'

def process_csv_file(upload_file):
    try:
        with open(upload_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            district_counts = {}
            total_rows = 0

            for row in csv_reader:
                total_rows += 1
                district_name = row['District Name']
                if district_name in district_counts:
                    district_counts[district_name] += 1
                else:
                    district_counts[district_name] = 1

            district_data = [{'name': district_name, 'count': count} for district_name, count in district_counts.items()]
            return district_data, None,total_rows
    except Exception as e:
        return None, f'Error: Row {total_rows} does not have exactly two values and format should be in District Name and Phone number'

@app.route('/excel_data/<filename>')
def excel_data(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_EXCEL"], filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    upload_file = None
    total_rows = 0
    district_data = None
    error_message = None

    if request.method == 'POST':
        upload_file = request.files['file']
        if upload_file.filename == '':
            flash('No file selected. Please choose a file.', 'error')
        else:
            ext = upload_file.filename.rsplit('.', 1)[1].lower() if '.' in upload_file.filename else ""
            if ext not in ALLOWED_EXTENSIONS:
                flash('Invalid file type. Please choose a valid file.', 'error')
            else:
                district_data = None
                if ext in ['xlsx', 'xlsm', 'xltx', 'xltm']:
                    district_data, error_message, total_rows = process_excel_file(upload_file)
                elif ext == 'csv':
                    district_data, error_message, total_rows = process_csv_file(upload_file)

                if error_message is not None:
                    flash(error_message, 'error')
                else:
                    flash('File uploaded successfully', 'success')
                    if not os.path.exists(app.config['UPLOAD_EXCEL']):
                        os.mkdir(app.config['UPLOAD_EXCEL'])
                    excel_sheet = app.config['UPLOAD_EXCEL']
                    file_path = os.path.join(excel_sheet, upload_file.filename)
                    upload_file.save(file_path)


    return render_template('index.html', district_data=district_data, total_rows=total_rows)  # Pass total_rows to the template

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)








    

