# Day-2-credit_statement

About the Project
 DBS Bank Credit Card Statement Generator
 This is a backend web application developed using Flask (Python) to generate professional PDF credit card statements
 for DBS Bank customers. It supports MySQL database integration and structured PDF rendering using WeasyPrint.
 About DBS Bank
 DBS Bank is one of Asia's leading financial services groups, headquartered in Singapore. This tool supports DBS's
 digital innovation by delivering personalized, secure, and multilingual banking statements.
 Tech Stack- Python (Flask)- MySQL- WeasyPrint- HTML/CSS- Jinja2 Templates
 Features- Multilingual PDF Statements (English, Chinese, Malay, Tamil)- Secure Data Retrieval- Responsive Output Layout- Downloadable via GET API- Modular Code Design
 API Usage
 Endpoint: /generate_pdf
 Method: GET
 Parameters:
 - customer_id (required)
 - language (optional: en, zh, ms, ta)
 Example: http://localhost:5000/generate_pdf?customer_id=123&language=zh
 Project Setup
 1. Clone the repo
 2. Create a virtual environment
 3. Install dependencies
 4. Run the app with python app.py
 5. Access via http://localhost:5000
 Credits
 Intern: Blezcherian
 Bank: DBS Bank - Credit Card Systems
Year: 2025
 DBS Bank Credit Card Statement Generator
 (c) DBS Bank - Internal Use Only
