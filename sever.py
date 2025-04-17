import pymysql
import logging
from weasyprint import HTML
from datetime import datetime
import os
import configparser
from decimal import Decimal
import argparse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("statement_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("statement_generator")

class DatabaseConnection:
    """Manages database connections and operations."""
    
    def __init__(self, config_file='config.ini'):
        """Initialize database connection parameters from config file."""
        try:
            config = configparser.ConfigParser()
            if os.path.exists(config_file):
                config.read(config_file)
                self.db_host = config.get('Database', 'DB_HOST', fallback='localhost')
                self.db_user = config.get('Database', 'DB_USER', fallback='root')
                self.db_password = config.get('Database', 'DB_PASSWORD', fallback='root')
                self.db_name = config.get('Database', 'DB_NAME', fallback='DBS_CreditCard')
            else:
                # Use defaults if config file doesn't exist
                self.db_host = 'localhost'
                self.db_user = 'root'
                self.db_password = 'root'
                self.db_name = 'DBS_CreditCard'
                logger.warning(f"Config file {config_file} not found. Using default values.")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise

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
                    SELECT customer_id, first_name, last_name, email, phone, address 
                    FROM Customers 
                    WHERE customer_id = %s
                """, (customer_id,))
                customer = cursor.fetchone()

                if not customer:
                    logger.warning(f"No customer found with ID {customer_id}")
                    return None, None
                
                # Query to fetch account details
                cursor.execute("""
                    SELECT account_id, account_number, account_type, card_number, credit_limit 
                    FROM Accounts 
                    WHERE customer_id = %s
                """, (customer_id,))
                account = cursor.fetchone()
                
                if not account:
                    logger.warning(f"No account found for customer ID {customer_id}")
                    return customer, None

                # Query to fetch transactions for the customer
                # Limit to most recent transactions to fit on single page
                cursor.execute("""
                    SELECT 
                        t.transaction_id,
                        t.transaction_date, 
                        t.merchant_name, 
                        t.transaction_amount, 
                        t.transaction_type,
                        t.category
                    FROM Transactions t
                    WHERE t.account_id = %s
                    ORDER BY t.transaction_date DESC
                    LIMIT 10
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
    
    def __init__(self, output_dir="statements"):
        """Initialize with output directory for statements."""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
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
    
    def generate_statement_pdf(self, customer, account, transactions, statement_date=None):
        """Generate a professional PDF statement that fits on a single page."""
        try:
            if not customer or not transactions:
                logger.error("Insufficient data to generate statement")
                return None
            
            statement_date = statement_date or datetime.today()
            date_str = statement_date.strftime('%B %d, %Y')
            file_date = statement_date.strftime('%Y%m%d')
            
            # Calculate transaction totals
            totals = self.calculate_totals(transactions)
            
            # Build transaction rows HTML - more compact
            transactions_html = ""
            for transaction in transactions:
                transaction_date = transaction['transaction_date'].strftime('%Y-%m-%d')
                merchant_name = transaction['merchant_name']
                amount = self.format_currency(transaction['transaction_amount'])
                transaction_type = transaction['transaction_type']
                category = transaction.get('category', 'General')
                
                # Style debit/credit amounts differently
                amount_class = "debit" if transaction_type in ['Purchase', 'Fee'] else "credit"
                
                transactions_html += f"""
                <tr>
                    <td>{transaction_date}</td>
                    <td>{merchant_name}</td>
                    <td>{category}</td>
                    <td>{transaction_type}</td>
                    <td class="{amount_class}">{amount}</td>
                </tr>
                """

            # Create the HTML template for the statement - optimized for single page
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>DBS Bank Credit Card Statement</title>
                <style>
                    @page {{
                        size: letter;
                        margin: 1cm;
                        @top-right {{
                            content: "Page " counter(page) " of " counter(pages);
                            font-size: 8pt;
                        }}
                    }}
                    body {{
                        font-family: 'Helvetica', 'Arial', sans-serif;
                        font-size: 9pt;
                        line-height: 1.3;
                        color: #333333;
                        margin: 0;
                        padding: 0;
                    }}
                    .header {{
                        border-bottom: 1px solid #0066b3;
                        padding-bottom: 5px;
                        margin-bottom: 10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
                    .logo {{
                        font-size: 18pt;
                        font-weight: bold;
                        color: #0066b3;
                    }}
                    .statement-title {{
                        font-size: 14pt;
                        margin: 0;
                        color: #333333;
                    }}
                    .customer-info {{
                        margin-bottom: 10px;
                        display: flex;
                        justify-content: space-between;
                    }}
                    .info-column {{
                        width: 48%;
                    }}
                    .account-summary {{
                        background-color: #f7f7f7;
                        border: 1px solid #e0e0e0;
                        border-radius: 3px;
                        padding: 8px;
                        margin-bottom: 10px;
                    }}
                    .summary-title {{
                        font-size: 11pt;
                        font-weight: bold;
                        margin: 0 0 5px 0;
                        color: #0066b3;
                    }}
                    .info-grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr 1fr 1fr;
                        gap: 10px;
                    }}
                    .info-item {{
                        margin-bottom: 3px;
                        font-size: 8pt;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #555555;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 10px;
                        font-size: 8pt;
                    }}
                    th, td {{
                        border: 1px solid #e0e0e0;
                        padding: 4px;
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
                        margin-top: 10px;
                        border: 1px solid #e0e0e0;
                        border-radius: 3px;
                        padding: 8px;
                        background-color: #f7f7f7;
                        display: flex;
                        justify-content: flex-end;
                    }}
                    .totals-table {{
                        width: 300px;
                        border: none;
                        margin: 0;
                    }}
                    .totals-table td {{
                        border: none;
                        padding: 2px 0;
                        font-size: 8pt;
                    }}
                    .totals-table .total-row {{
                        font-weight: bold;
                        font-size: 10pt;
                        border-top: 1px solid #e0e0e0;
                        padding-top: 4px;
                    }}
                    .footer {{
                        margin-top: 10px;
                        font-size: 7pt;
                        color: #777777;
                        text-align: center;
                        border-top: 1px solid #e0e0e0;
                        padding-top: 5px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <div class="logo">DBS Bank</div>
                    <h1 class="statement-title">Credit Card Statement</h1>
                </div>
                
                <div class="customer-info">
                    <div class="info-column">
                        <div class="info-item">
                            <span class="label">Customer:</span> {customer['first_name']} {customer['last_name']} (ID: {customer['customer_id']})
                        </div>
                        <div class="info-item">
                            <span class="label">Email:</span> {customer['email']}
                        </div>
                        <div class="info-item">
                            <span class="label">Phone:</span> {customer.get('phone', 'N/A')}
                        </div>
                    </div>
                    <div class="info-column">
                        <div class="info-item">
                            <span class="label">Statement Date:</span> {date_str}
                        </div>
                        <div class="info-item">
                            <span class="label">Account #:</span> {account['account_number']} | <span class="label">Card #:</span> {'XXXX-' + account['card_number'][-4:]}
                        </div>
                        <div class="info-item">
                            <span class="label">Credit Limit:</span> {self.format_currency(account['credit_limit'])}
                        </div>
                    </div>
                </div>
                
                <div class="account-summary">
                    <h2 class="summary-title">Account Summary</h2>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="label">Purchases:</span> {self.format_currency(totals['purchases'])}
                        </div>
                        <div class="info-item">
                            <span class="label">Payments:</span> {self.format_currency(totals['payments'])}
                        </div>
                        <div class="info-item">
                            <span class="label">Fees:</span> {self.format_currency(totals['fees'])}
                        </div>
                        <div class="info-item">
                            <span class="label">Credits:</span> {self.format_currency(totals['credits'])}
                        </div>
                    </div>
                </div>
                
                <h2 class="summary-title">Transaction Details</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Merchant</th>
                            <th>Category</th>
                            <th>Type</th>
                            <th>Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        {transactions_html}
                    </tbody>
                </table>
                
                <div class="totals">
                    <table class="totals-table">
                        <tr>
                            <td class="label">Total Purchases:</td>
                            <td class="debit">{self.format_currency(totals['purchases'])}</td>
                        </tr>
                        <tr>
                            <td class="label">Total Fees:</td>
                            <td class="debit">{self.format_currency(totals['fees'])}</td>
                        </tr>
                        <tr>
                            <td class="label">Total Payments:</td>
                            <td class="credit">{self.format_currency(totals['payments'])}</td>
                        </tr>
                        <tr>
                            <td class="label">Total Credits:</td>
                            <td class="credit">{self.format_currency(totals['credits'])}</td>
                        </tr>
                        <tr class="total-row">
                            <td class="label">Current Balance:</td>
                            <td class="{'debit' if totals['net_total'] > 0 else 'credit'}">{self.format_currency(totals['net_total'])}</td>
                        </tr>
                    </table>
                </div>
                
                <div class="footer">
                    <p>This statement is for informational purposes only. For questions, contact our customer service at 1-800-DBS-BANK. © {datetime.today().year} DBS Bank.</p>
                </div>
            </body>
            </html>
            """

            # Generate PDF from HTML with specific page size settings
            pdf = HTML(string=html_content).write_pdf()

            # Create filename and save the PDF
            customer_id = customer['customer_id']
            pdf_filename = f"{self.output_dir}/DBS_Statement_{customer_id}_{file_date}.pdf"
            with open(pdf_filename, 'wb') as f:
                f.write(pdf)

            logger.info(f"Single-page PDF statement generated successfully: {pdf_filename}")
            return pdf_filename

        except Exception as e:
            logger.error(f"Error generating PDF statement: {e}", exc_info=True)
            return None


def main():
    """Main function to run the statement generator."""
    parser = argparse.ArgumentParser(description='Generate credit card statements')
    parser.add_argument('--customer_id', type=int, help='Customer ID to generate statement for')
    parser.add_argument('--config', default='config.ini', help='Path to configuration file')
    parser.add_argument('--output_dir', default='statements', help='Directory for output files')
    args = parser.parse_args()
    
    try:
        customer_id = args.customer_id
        if not customer_id:
            customer_id = int(input("Enter Customer ID: "))
        
        logger.info(f"Generating statement for customer ID: {customer_id}")
        
        # Connect to database and fetch customer data
        db = DatabaseConnection(args.config)
        customer, account, transactions = db.fetch_customer_data(customer_id)
        
        if not customer:
            logger.error(f"Could not retrieve data for customer ID {customer_id}")
            return
        
        # Generate and save PDF statement
        generator = StatementGenerator(args.output_dir)
        pdf_file = generator.generate_statement_pdf(customer, account, transactions)
        
        if pdf_file:
            print(f"Statement generated successfully: {pdf_file}")
        else:
            print("Failed to generate statement. Check logs for details.")
    
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        print("Please enter a valid customer ID (numeric value)")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()