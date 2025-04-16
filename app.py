from flask import Flask, request, send_file, render_template
import pymysql
from weasyprint import HTML
from datetime import datetime
import io

# Database connection details
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'  # Replace with your MySQL password
DB_NAME = 'DBS_CreditCard'

app = Flask(__name__)

# Translations dictionary
translations = {
    'en': {
        'statement_title': 'DBS Bank Credit Card Statement',
        'customer': 'Customer',
        'email': 'Email',
        'statement_date': 'Statement Date',
        'date': 'Date',
        'merchant': 'Merchant',
        'amount': 'Amount',
        'transaction_type': 'Transaction Type',
        'html_dir': 'ltr',  # left-to-right
        'font_family': 'Arial, sans-serif'
    },
    'zh': {
        'statement_title': 'DBS银行信用卡对账单',
        'customer': '客户',
        'email': '电子邮件',
        'statement_date': '对账单日期',
        'date': '日期',
        'merchant': '商家',
        'amount': '金额',
        'transaction_type': '交易类型',
        'html_dir': 'ltr',
        'font_family': '"Noto Sans SC", Arial, sans-serif'
    },
    'ms': {
        'statement_title': 'Penyata Kad Kredit Bank DBS',
        'customer': 'Pelanggan',
        'email': 'E-mel',
        'statement_date': 'Tarikh Penyata',
        'date': 'Tarikh',
        'merchant': 'Peniaga',
        'amount': 'Jumlah',
        'transaction_type': 'Jenis Transaksi',
        'html_dir': 'ltr',
        'font_family': 'Arial, sans-serif'
    },
    'ta': {
        'statement_title': 'DBS வங்கி கடன் அட்டை அறிக்கை',
        'customer': 'வாடிக்கையாளர்',
        'email': 'மின்னஞ்சல்',
        'statement_date': 'அறிக்கை தேதி',
        'date': 'தேதி',
        'merchant': 'வணிகர்',
        'amount': 'தொகை',
        'transaction_type': 'பரிவர்த்தனை வகை',
        'html_dir': 'ltr',
        'font_family': '"Noto Sans Tamil", Arial, sans-serif'
    }
}

# Serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML form

# Function to fetch customer and transaction data
def fetch_data(customer_id):
    try:
        # Establish a connection to the database
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        with connection.cursor() as cursor:
            # Query to fetch customer details
            cursor.execute("SELECT first_name, last_name, email FROM Customers WHERE customer_id = %s", (customer_id,))
            customer = cursor.fetchone()

            if not customer:
                return None, None

            # Query to fetch transactions for the customer
            cursor.execute("""
                SELECT t.transaction_date, t.merchant_name, t.transaction_amount, t.transaction_type
                FROM Transactions t
                JOIN Accounts a ON t.account_id = a.account_id
                WHERE a.customer_id = %s
                ORDER BY t.transaction_date DESC
            """, (customer_id,))
            transactions = cursor.fetchall()

            return customer, transactions

    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None, None

    finally:
        connection.close()

# Function to generate PDF statement in the specified language
def generate_pdf(customer, transactions, language='en'):
    if not customer or not transactions:
        return None
    
    # Use default language (English) as fallback
    if language not in translations:
        language = 'en'
        
    text = translations[language]
    first_name, last_name, email = customer
    today = datetime.today().strftime('%Y-%m-%d')

    transactions_html = ""
    for transaction in transactions:
        transaction_date = transaction[0].strftime('%Y-%m-%d')
        merchant_name = transaction[1]
        transaction_amount = f"${transaction[2]:,.2f}"
        transaction_type = transaction[3]
        transactions_html += f"""
        <tr>
            <td>{transaction_date}</td>
            <td>{merchant_name}</td>
            <td>{transaction_amount}</td>
            <td>{transaction_type}</td>
        </tr>
        """

    html_content = f"""
    <html dir="{text['html_dir']}">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC&family=Noto+Sans+Tamil&display=swap');
            body {{
                font-family: {text['font_family']};
                line-height: 1.6;
                margin: 40px;
            }}
            h1 {{
                text-align: center;
                color: #2C3E50;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
            }}
        </style>
    </head>
    <body>
        <h1>{text['statement_title']}</h1>
        <p><strong>{text['customer']}:</strong> {first_name} {last_name}</p>
        <p><strong>{text['email']}:</strong> {email}</p>
        <p><strong>{text['statement_date']}:</strong> {today}</p>
        <table>
            <thead>
                <tr>
                    <th>{text['date']}</th>
                    <th>{text['merchant']}</th>
                    <th>{text['amount']}</th>
                    <th>{text['transaction_type']}</th>
                </tr>
            </thead>
            <tbody>
                {transactions_html}
            </tbody>
        </table>
    </body>
    </html>
    """

    pdf = HTML(string=html_content).write_pdf()

    # Convert the PDF to a file-like object
    pdf_io = io.BytesIO(pdf)
    pdf_io.seek(0)

    return pdf_io

@app.route('/generate_pdf', methods=['GET'])
def generate_pdf_route():
    customer_id = request.args.get('customer_id')
    language = request.args.get('language', 'en')  # Default to English if no language specified

    if not customer_id:
        return "Customer ID is required.", 400

    customer, transactions = fetch_data(customer_id)

    if not customer:
        return "Customer not found.", 404

    pdf_io = generate_pdf(customer, transactions, language)

    if pdf_io:
        return send_file(
            pdf_io, 
            as_attachment=True, 
            download_name=f"credit_card_statement_{customer_id}.pdf", 
            mimetype="application/pdf"
        )

    return "Failed to generate PDF.", 500

if __name__ == '__main__':
    app.run(debug=True)