import pymysql
from weasyprint import HTML
from datetime import datetime

# Database connection details
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'  # Replace with your MySQL password
DB_NAME = 'DBS_CreditCard'

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
                print(f"No customer found with ID {customer_id}")
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
        # Close the connection
        connection.close()

# Function to generate PDF statement
def generate_pdf(customer, transactions):
    try:
        if not customer or not transactions:
            print("No data to generate PDF.")
            return

        # Prepare the statement data
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

        # Create the HTML template for the statement
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
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
                .total {{
                    font-weight: bold;
                    background-color: #f4f4f4;
                }}
            </style>
        </head>
        <body>
            <h1>DBS Bank Credit Card Statement</h1>
            <p><strong>Customer:</strong> {first_name} {last_name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Statement Date:</strong> {today}</p>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Merchant</th>
                        <th>Amount</th>
                        <th>Transaction Type</th>
                    </tr>
                </thead>
                <tbody>
                    {transactions_html}
                </tbody>
            </table>
        </body>
        </html>
        """

        # Generate PDF from HTML
        pdf = HTML(string=html_content).write_pdf()

        # Save the PDF file
        pdf_filename = f"credit_card_statement_{customer[0]}_{customer[1]}_{today}.pdf"
        with open(pdf_filename, 'wb') as f:
            f.write(pdf)

        print(f"PDF statement generated successfully: {pdf_filename}")

    except Exception as e:
        print(f"Error generating PDF: {e}")

# Main function
if __name__ == "__main__":
    customer_id = int(input("Enter Customer ID: "))
    customer, transactions = fetch_data(customer_id)
    generate_pdf(customer, transactions)
