from flask import Blueprint, render_template, request, redirect, flash
from validators.rules import validate_file_extension, validate_dataframe
from services.pdf_generator import generate_pdf
import pandas as pd
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate_pdf', methods=['POST'])
def handle_upload():
    file = request.files.get('file')
    if not file or not validate_file_extension(file.filename):
        flash("Invalid file. Please upload a .csv file.")
        return redirect('/')

    df = pd.read_csv(file)
    errors = validate_dataframe(df)

    if errors:
        flash("Validation errors: " + ", ".join(errors))
        return redirect('/')

    output_path = os.path.join('static', 'report.pdf')
    generate_pdf(df, output_path)

    return render_template("success.html", path=output_path)
