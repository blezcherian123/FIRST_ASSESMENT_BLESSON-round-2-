from flask import Flask, request, send_file, render_template, jsonify, abort
import pymysql
from weasyprint import HTML
from datetime import datetime
import io
import os
import logging
import configparser
from decimal import Decimal

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("statement_web_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("statement_web_app")

app = Flask(__name__)

# Load configuration
def load_config():
    config = configparser.ConfigParser()
    config_file = 'config.ini'
    
    if os.path.exists(config_file):
        config.read(config_file)
        return {
            'DB_HOST': config.get('Database', 'DB_HOST', fallback='localhost'),
            'DB_USER': config.get('Database', 'DB_USER', fallback='root'),
            'DB_PASSWORD': config.get('Database', 'DB_PASSWORD', fallback='root'),
            'DB_NAME': config.get('Database', 'DB_NAME', fallback='DBS_CreditCard')
        }
    else:
        # Use defaults if config file doesn't exist
        logger.warning(f"Config file {config_file} not found. Using default values.")
        return {
            'DB_HOST': 'localhost',
            'DB_USER': 'root',
            'DB_PASSWORD': 'root',
            'DB_NAME': 'DBS_CreditCard'
        }

config = load_config()

# Translations dictionary
translations = {
    'en': {
        'statement_title': 'DBS Bank Credit Card Statement',
        'customer': 'Customer',
        'email': 'Email',
        'phone': 'Phone',
        'address': 'Address',
        'statement_date': 'Statement Date',
        'account_number': 'Account Number',
        'card_number': 'Card Number',
        'credit_limit': 'Credit Limit',
        'date': 'Date',
        'merchant': 'Merchant',
        'category': 'Category',
        'amount': 'Amount',
        'transaction_type': 'Transaction Type',
        'account_summary': 'Account Summary',
        'total_purchases': 'Total Purchases',
        'total_payments': 'Total Payments',
        'total_fees': 'Total Fees',
        'total_credits': 'Total Credits',
        'current_balance': 'Current Balance',
        'transaction_details': 'Transaction Details',
        'footer_text': 'This statement is for informational purposes only. For questions or concerns, please contact our customer service.',
        'copyright': '© {year} DBS Bank. All rights reserved.',
        'html_dir': 'ltr',  # left-to-right
        'font_family': 'Helvetica, Arial, sans-serif'
    },
    'zh': {
        'statement_title': 'DBS银行信用卡对账单',
        'customer': '客户',
        'email': '电子邮件',
        'phone': '电话',
        'address': '地址',
        'statement_date': '对账单日期',
        'account_number': '账号',
        'card_number': '卡号',
        'credit_limit': '信用额度',
        'date': '日期',
        'merchant': '商家',
        'category': '类别',
        'amount': '金额',
        'transaction_type': '交易类型',
        'account_summary': '账户摘要',
        'total_purchases': '总购买金额',
        'total_payments': '总支付金额',
        'total_fees': '总费用',
        'total_credits': '总退款',
        'current_balance': '当前余额',
        'transaction_details': '交易明细',
        'footer_text': '此对账单仅供参考。如有疑问或顾虑，请联系我们的客户服务。',
        'copyright': '© {year} 星展银行。保留所有权利。',
        'html_dir': 'ltr',
        'font_family': '"Noto Sans SC", Helvetica, Arial, sans-serif'
    },
    'ms': {
        'statement_title': 'Penyata Kad Kredit Bank DBS',
        'customer': 'Pelanggan',
        'email': 'E-mel',
        'phone': 'Telefon',
        'address': 'Alamat',
        'statement_date': 'Tarikh Penyata',
        'account_number': 'Nombor Akaun',
        'card_number': 'Nombor Kad',
        'credit_limit': 'Had Kredit',
        'date': 'Tarikh',
        'merchant': 'Peniaga',
        'category': 'Kategori',
        'amount': 'Jumlah',
        'transaction_type': 'Jenis Transaksi',
        'account_summary': 'Ringkasan Akaun',
        'total_purchases': 'Jumlah Pembelian',
        'total_payments': 'Jumlah Pembayaran',
        'total_fees': 'Jumlah Yuran',
        'total_credits': 'Jumlah Kredit',
        'current_balance': 'Baki Semasa',
        'transaction_details': 'Butiran Transaksi',
        'footer_text': 'Penyata ini adalah untuk tujuan maklumat sahaja. Untuk pertanyaan atau kebimbangan, sila hubungi perkhidmatan pelanggan kami.',
        'copyright': '© {year} Bank DBS. Hak cipta terpelihara.',
        'html_dir': 'ltr',
        'font_family': 'Helvetica, Arial, sans-serif'
    },
    'ta': {
        'statement_title': 'DBS வங்கி கடன் அட்டை அறிக்கை',
        'customer': 'வாடிக்கையாளர்',
        'email': 'மின்னஞ்சல்',
        'phone': 'தொலைபேசி',
        'address': 'முகவரி',
        'statement_date': 'அறிக்கை தேதி',
        'account_number': 'கணக்கு எண்',
        'card_number': 'அட்டை எண்',
        'credit_limit': 'கடன் வரம்பு',
        'date': 'தேதி',
        'merchant': 'வணிகர்',
        'category': 'வகை',
        'amount': 'தொகை',
        'transaction_type': 'பரிவர்த்தனை வகை',
        'account_summary': 'கணக்கு சுருக்கம்',
        'total_purchases': 'மொத்த கொள்முதல்கள்',
        'total_payments': 'மொத்த கொடுப்பனவுகள்',
        'total_fees': 'மொத்த கட்டணங்கள்',
        'total_credits': 'மொத்த வரவுகள்',
        'current_balance': 'தற்போதைய இருப்பு',
        'transaction_details': 'பரிவர்த்தனை விவரங்கள்',
        'footer_text': 'இந்த அறிக்கை தகவல் நோக்கங்களுக்காக மட்டுமே. கேள்விகள் அல்லது கவலைகளுக்கு, எங்கள் வாடிக்கையாளர் சேவையைத் தொடர்பு கொள்ளவும்.',
        'copyright': '© {year} DBS வங்கி. அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.',
        'html_dir': 'ltr',
        'font_family': '"Noto Sans Tamil", Helvetica, Arial, sans-serif'
    }
}

class DatabaseConnection:
    """Manages database connections and operations."""
    
    def __init__(self, config):
        """Initialize database connection parameters from config."""
        self.db_host = config['DB_HOST']
        self.db_user = config['DB_USER']
        self.db_password = config['DB_PASSWORD']
        self.db_name = config['DB_NAME']

    def fetch_customer_data(self, customer_id):
        """Fetch customer details and transactions from database."""
        connection = None
        try:
            connection = pymysql.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
                cursorclass=pymysql.cursors.DictCursor  # Return results as dictionaries
            )
            
            with connection.cursor() as cursor:
                # Query to fetch customer details
                cursor.execute("""
                    SELECT customer_id, first_name, last_name, email, 
                           COALESCE(phone, 'N/A') as phone, 
                           COALESCE(address, 'N/A') as address 
                    FROM Customers 
                    WHERE customer_id = %s
                """, (customer_id,))
                customer = cursor.fetchone()

                if not customer:
                    logger.warning(f"No customer found with ID {customer_id}")
                    return None, None, None
                
                # Query to fetch account details
                cursor.execute("""
                    SELECT account_id, account_number, account_type, 
                           card_number, credit_limit 
                    FROM Accounts 
                    WHERE customer_id = %s
                """, (customer_id,))
                account = cursor.fetchone()
                
                if not account:
                    logger.warning(f"No account found for customer ID {customer_id}")
                    return customer, None, None

                # Query to fetch transactions for the customer
                cursor.execute("""
                    SELECT 
                        t.transaction_id,
                        t.transaction_date, 
                        t.merchant_name, 
                        t.transaction_amount, 
                        t.transaction_type,
                        COALESCE(t.category, 'General') as category
                    FROM Transactions t
                    WHERE t.account_id = %s
                    ORDER BY t.transaction_date DESC
                """, (account['account_id'],))
                transactions = cursor.fetchall()

                return customer, account, transactions

        except pymysql.MySQLError as e:
            logger.error(f"Database error: {e}")
            return None, None, None
        finally:
            if connection:
                connection.close()


class StatementGenerator:
    """Generates credit card statements in PDF format."""
    
    def __init__(self):
        """Initialize statement generator."""
        pass
    
    def calculate_totals(self, transactions):
        """Calculate transaction totals by type."""
        totals = {
            'purchases': Decimal('0.00'),
            'payments': Decimal('0.00'),
            'fees': Decimal('0.00'),
            'credits': Decimal('0.00')
        }
        
        for transaction in transactions:
            amount = Decimal(str(transaction['transaction_amount']))
            t_type = transaction['transaction_type'].lower()
            
            if t_type == 'purchase':
                totals['purchases'] += amount
            elif t_type == 'payment':
                totals['payments'] += amount
            elif t_type == 'fee':
                totals['fees'] += amount
            elif t_type == 'credit' or t_type == 'refund':
                totals['credits'] += amount
        
        # Calculate net total
        totals['net_total'] = totals['purchases'] + totals['fees'] - totals['payments'] - totals['credits']
        
        return totals
    
    def format_currency(self, amount):
        """Format amount as currency string."""
        if amount < 0:
            return f"-${abs(amount):,.2f}"
        return f"${amount:,.2f}"
    
    def generate_statement_pdf(self, customer, account, transactions, language='en'):
        """Generate a professional PDF statement in the specified language."""
        try:
            if not customer or not transactions:
                logger.error("Insufficient data to generate statement")
                return None
            
            # Use default language (English) as fallback
            if language not in translations:
                language = 'en'
                logger.warning(f"Language {language} not supported, falling back to English")
                
            text = translations[language]
            statement_date = datetime.today()
            date_str = statement_date.strftime('%B %d, %Y')
            
            # Calculate transaction totals
            totals = self.calculate_totals(transactions)
            
            # Build transaction rows HTML
            transactions_html = ""
            for transaction in transactions:
                transaction_date = transaction['transaction_date'].strftime('%Y-%m-%d')
                merchant_name = transaction['merchant_name']
                amount = self.format_currency(transaction['transaction_amount'])
                transaction_type = transaction['transaction_type']
                category = transaction.get('category', 'General')
                
                # Style debit/credit amounts differently
                amount_class = "debit" if transaction_type.lower() in ['purchase', 'fee'] else "credit"
                
                transactions_html += f"""
                <tr>
                    <td>{transaction_date}</td>
                    <td>{merchant_name}</td>
                    <td>{category}</td>
                    <td>{transaction_type}</td>
                    <td class="{amount_class}">{amount}</td>
                </tr>
                """

            # Create the HTML template for the statement
            html_content = f"""
            <!DOCTYPE html>
            <html lang="{language}" dir="{text['html_dir']}">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{text['statement_title']}</title>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC&family=Noto+Sans+Tamil&display=swap');
                    @page {{
                        size: letter;
                        margin: 2cm;
                        @top-right {{
                            content: "Page " counter(page) " of " counter(pages);
                            font-size: 9pt;
                        }}
                    }}
                    body {{
                        font-family: {text['font_family']};
                        font-size: 10pt;
                        line-height: 1.6;
                        color: #333333;
                    }}
                    .header {{
                        border-bottom: 2px solid #0066b3;
                        padding-bottom: 10px;
                        margin-bottom: 20px;
                    }}
                    .logo {{
                        font-size: 24pt;
                        font-weight: bold;
                        color: #0066b3;
                    }}
                    .statement-title {{
                        font-size: 18pt;
                        margin-top: 0;
                        color: #333333;
                    }}
                    .customer-info {{
                        margin-bottom: 30px;
                    }}
                    .account-summary {{
                        background-color: #f7f7f7;
                        border: 1px solid #e0e0e0;
                        border-radius: 5px;
                        padding: 15px;
                        margin-bottom: 20px;
                    }}
                    .summary-title {{
                        font-size: 14pt;
                        font-weight: bold;
                        margin-top: 0;
                        margin-bottom: 10px;
                        color: #0066b3;
                    }}
                    .info-grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 15px;
                    }}
                    .info-item {{
                        margin-bottom: 5px;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #555555;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                        font-size: 9pt;
                    }}
                    th, td {{
                        border: 1px solid #e0e0e0;
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #0066b3;
                        color: white;
                        font-weight: normal;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f9f9f9;
                    }}
                    .debit {{
                        color: #d9534f;
                    }}
                    .credit {{
                        color: #5cb85c;
                    }}
                    .totals {{
                        margin-top: 20px;
                        border: 1px solid #e0e0e0;
                        border-radius: 5px;
                        padding: 15px;
                        background-color: #f7f7f7;
                    }}
                    .totals-table {{
                        width: 350px;
                        margin-left: auto;
                        border: none;
                    }}
                    .totals-table td {{
                        border: none;
                        padding: 3px 0;
                    }}
                    .totals-table .total-row {{
                        font-weight: bold;
                        font-size: 12pt;
                        border-top: 1px solid #e0e0e0;
                        padding-top: 8px;
                    }}
                    .footer {{
                        margin-top: 30px;
                        font-size: 9pt;
                        color: #777777;
                        text-align: center;
                        border-top: 1px solid #e0e0e0;
                        padding-top: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <div class="logo">DBS Bank</div>
                    <h1 class="statement-title">{text['statement_title']}</h1>
                </div>
                
                <div class="customer-info info-grid">
                    <div>
                        <div class="info-item">
                            <span class="label">{text['customer']}:</span> {customer['first_name']} {customer['last_name']}
                        </div>
                        <div class="info-item">
                            <span class="label">ID:</span> {customer['customer_id']}
                        </div>
                        <div class="info-item">
                            <span class="label">{text['email']}:</span> {customer['email']}
                        </div>
                        <div class="info-item">
                            <span class="label">{text['phone']}:</span> {customer['phone']}
                        </div>
                    </div>
                    <div>
                        <div class="info-item">
                            <span class="label">{text['statement_date']}:</span> {date_str}
                        </div>
                        <div class="info-item">
                            <span class="label">{text['account_number']}:</span> {account['account_number']}
                        </div>
                        <div class="info-item">
                            <span class="label">{text['card_number']}:</span> {'XXXX-XXXX-XXXX-' + account['card_number'][-4:]}
                        </div>
                        <div class="info-item">
                            <span class="label">{text['credit_limit']}:</span> {self.format_currency(account['credit_limit'])}
                        </div>
                    </div>
                </div>
                
                <div class="account-summary">
                    <h2 class="summary-title">{text['account_summary']}</h2>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="label">{text['total_purchases']}:</span> {self.format_currency(totals['purchases'])}
                        </div>
                        <div class="info-item">
                            <span class="label">{text['total_payments']}:</span> {self.format_currency(totals['payments'])}
                        </div>
                        <div class="info-item">
                            <span class="label">{text['total_fees']}:</span> {self.format_currency(totals['fees'])}
                        </div>
                        <div class="info-item">
                            <span class="label">{text['total_credits']}:</span> {self.format_currency(totals['credits'])}
                        </div>
                    </div>
                </div>
                
                <h2 class="summary-title">{text['transaction_details']}</h2>
                <table>
                    <thead>
                        <tr>
                            <th>{text['date']}</th>
                            <th>{text['merchant']}</th>
                            <th>{text['category']}</th>
                            <th>{text['transaction_type']}</th>
                            <th>{text['amount']}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {transactions_html}
                    </tbody>
                </table>
                
                <div class="totals">
                    <table class="totals-table">
                        <tr>
                            <td class="label">{text['total_purchases']}:</td>
                            <td class="debit">{self.format_currency(totals['purchases'])}</td>
                        </tr>
                        <tr>
                            <td class="label">{text['total_fees']}:</td>
                            <td class="debit">{self.format_currency(totals['fees'])}</td>
                        </tr>
                        <tr>
                            <td class="label">{text['total_payments']}:</td>
                            <td class="credit">{self.format_currency(totals['payments'])}</td>
                        </tr>
                        <tr>
                            <td class="label">{text['total_credits']}:</td>
                            <td class="credit">{self.format_currency(totals['credits'])}</td>
                        </tr>
                        <tr class="total-row">
                            <td class="label">{text['current_balance']}:</td>
                            <td class="{'debit' if totals['net_total'] > 0 else 'credit'}">{self.format_currency(totals['net_total'])}</td>
                        </tr>
                    </table>
                </div>
                
                <div class="footer">
                    <p>{text['footer_text']}</p>
                    <p>{text['copyright'].format(year=datetime.today().year)}</p>
                </div>
            </body>
            </html>
            """

            # Generate PDF from HTML
            pdf = HTML(string=html_content).write_pdf()

            # Convert the PDF to a file-like object
            pdf_io = io.BytesIO(pdf)
            pdf_io.seek(0)
            
            return pdf_io

        except Exception as e:
            logger.error(f"Error generating PDF statement: {e}", exc_info=True)
            return None


# Serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/languages')
def get_languages():
    """Return available languages for statement generation."""
    available_languages = [
        {"code": code, "name": translations[code]['statement_title']} 
        for code in translations.keys()
    ]
    return jsonify(available_languages)

@app.route('/api/customer/<int:customer_id>')
def get_customer(customer_id):
    """Return customer information for preview."""
    try:
        db = DatabaseConnection(config)
        customer, account, _ = db.fetch_customer_data(customer_id)
        
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
            
        # Mask sensitive data for API response
        if account:
            account['card_number'] = 'XXXX-XXXX-XXXX-' + account['card_number'][-4:]
        
        return jsonify({
            "customer": customer,
            "account": account
        })
    except Exception as e:
        logger.error(f"Error fetching customer data: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/generate_statement', methods=['GET'])
def generate_pdf_route():
    """Generate and return PDF statement."""
    try:
        customer_id = request.args.get('customer_id')
        language = request.args.get('language', 'en')  # Default to English
        
        if not customer_id:
            return "Customer ID is required", 400
            
        try:
            customer_id = int(customer_id)
        except ValueError:
            return "Invalid customer ID format", 400

        # Fetch data from database
        db = DatabaseConnection(config)
        customer, account, transactions = db.fetch_customer_data(customer_id)

        if not customer:
            return "Customer not found", 404
            
        if not account:
            return "No account found for this customer", 404

        # Generate PDF
        generator = StatementGenerator()
        pdf_io = generator.generate_statement_pdf(customer, account, transactions, language)

        if not pdf_io:
            return "Failed to generate PDF statement", 500

        # Format filename for download
        filename = f"DBS_Statement_{customer['first_name']}_{customer['last_name']}_{datetime.today().strftime('%Y%m%d')}.pdf"
        
        return send_file(
            pdf_io, 
            as_attachment=True, 
            download_name=filename, 
            mimetype="application/pdf"
        )
        
    except Exception as e:
        logger.error(f"Error in generate_statement route: {e}", exc_info=True)
        return "An error occurred while generating the statement", 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)