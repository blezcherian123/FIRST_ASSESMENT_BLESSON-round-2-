# DBS Bank Credit Card Statement Generator

 Description

The DBS Bank Credit Card Statement Generator is a backend web application developed using Python and the Flask framework. It is designed to generate professional, multilingual PDF credit card statements for DBS Bank customers. This tool supports MySQL database integration for secure data retrieval and utilizes WeasyPrint for structured PDF rendering.  This application supports DBS's digital innovation by delivering personalized, secure, and multilingual banking statements.

## About DBS Bank

DBS Bank is a leading financial services group in Asia, headquartered in Singapore.

## Tech Stack

* Python (Flask)
* MySQL
* WeasyPrint
* HTML/CSS
* Jinja2 Templates

## Features

* **Multilingual PDF Statements:** Generates statements in English, Chinese, Malay, and Tamil.
* **Secure Data Retrieval:** Retrieves customer data securely from a MySQL database.
* **Responsive Output Layout:** Creates well-structured and visually appealing PDF statements.
* **Downloadable via GET API:** Statements can be downloaded via a simple GET API endpoint.
* **Modular Code Design:** Designed for maintainability and scalability.

## API Usage

### Endpoint: `/generate_pdf`

### Method: `GET`

### Parameters:

* `customer_id` (required):  The unique identifier for the customer.
* `language` (optional):  The desired language for the statement.  Possible values: `en` (English), `zh` (Chinese), `ms` (Malay), `ta` (Tamil).  Default is English if not provided.

### Example:

`http://localhost:5000/generate_pdf?customer_id=123&language=zh`

## Project Setup

1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git) #Replace with actual repo
    ```
2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    (Ensure you have a `requirements.txt` file listing the project dependencies.  If not, create one using `pip freeze > requirements.txt` after installing the necessary packages.)

4.  Set up the MySQL database:
    * Ensure you have a MySQL server running.
    * Create a database for the application.
    * Configure the database connection settings in your application (e.g., in a config file or environment variables).  (Details of how to do this are project-specific and should be documented in your application.)
    * Create the necessary tables in the database. (Include SQL schema in your project)
5. Run the application:
    ```bash
    python app.py
    ```
6.  Access the application:

    Open your web browser and go to `http://localhost:5000`.

## Credits

* Intern: Blezcherian
* Bank: DBS Bank - Credit Card Systems
* Year: 2025

## License

DBS Bank Credit Card Statement Generator (c) DBS Bank - Internal Use Only


## Project Overview
A transaction validation system to identify high-value transactions from uploaded bank statements.

## Features
- UI with multi-page support
- File upload
- Validation and rules checking
- PDF output for different categories

## Folder Structure
FIRST_ASSESMENT_BLESSON-round-2/
│
├── app/
│   ├── __init__.py
│   ├── routes.py              # All Flask routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_generator.py   # PDF generation logic
│   │   ├── db_utils.py        # DB access logic
│   │   └── language_utils.py  # Multilingual text support
│   └── config.py              # Any config (e.g. DB, fonts)
│
├── tests/
│   ├── __init__.py
│   └── test_pdf_generator.py  # Unit tests for PDF generation
│
├── sample_output/             # Example generated PDFs
├── static/                    # Static files (if any)
├── templates/                 # HTML templates (if needed)
├── requirements.txt
├── app.py                     # Run the Flask app from here
└── README.md


## How to Run
1. pip install -r requirements.txt
2. python app.py
