Test Case #01 – Valid customer, low-volume transaction
Input:
customer_id = 123
language = en
Precondition:

Customer with ID 123 exists in the Customers table

Customer has 2 transactions in the Transactions table
Expected Output:

HTTP 200 OK

Response is a downloadable PDF named: credit_card_statement_123.pdf

PDF contains:

Header: "DBS Bank Credit Card Statement"

Customer name and email

2 transactions listed with date, merchant, amount, and type
Actual Output:

HTTP 200 OK, file downloaded successfully
Result:
PASS




Test Case #02 – Invalid customer ID
Input:
customer_id = 999
language = en
Precondition:

No customer with ID 999 in the Customers table
Expected Output:

HTTP 404 Not Found

Response message: "Customer not found."
Actual Output:

HTTP 404, message: "Customer not found."
Result:
PASS




Test Case #03 – Bilingual statement in Chinese
Input:
customer_id = 123
language = zh
Precondition:

Customer exists with at least 1 transaction
Expected Output:

PDF generated with:

Title: "DBS银行信用卡对账单"

Font includes Chinese (Noto Sans SC)

Table headers and labels in Chinese
Actual Output:

PDF content in Chinese with correct formatting
Result:
PASS



Test Case #04 – Missing customer_id in request
Input:
URL = /generate_pdf
(no customer_id parameter)
Precondition:

None
Expected Output:

HTTP 400 Bad Request

Response message: "Customer ID is required."
Actual Output:

HTTP 400, message: "Customer ID is required."
Result:
PASS




Test Case #05 – Valid customer, high-volume transaction
Input:
customer_id = 124
language = en
Precondition:

Customer has 50 transactions in the Transactions table
Expected Output:

HTTP 200 OK

PDF includes all 50 transactions properly paginated
Actual Output:

PDF with 50 transactions and correct pagination
Result:
PASS




Test Case #06 – Valid customer, zero transactions
Input:
customer_id = 125
language = en
Precondition:

Customer exists but has no transactions in the current statement period
Expected Output:

HTTP 200 OK

PDF contains header and customer info

Message: "No transactions found for this period."
Actual Output:

PDF generated with proper message
Result:
PASS




Test Case #07 – Invalid language code
Input:
customer_id = 123
language = xx
Precondition:

Valid customer with transactions
Expected Output:

HTTP 400 Bad Request

Message: "Unsupported language selected."
Actual Output:

HTTP 400, proper error message
Result:
PASS




Test Case #08 – SQL injection attempt in customer_id
Input:
customer_id = "123; DROP TABLE Customers;"
language = en
Precondition:

None
Expected Output:

HTTP 400 Bad Request

Input sanitized or rejected
Actual Output:

HTTP 400, invalid input
Result:
PASS




Test Case #09 – Customer with special characters in name
Input:
customer_id = 126
language = en
Precondition:

Customer name = "Renée O'Connor"
Expected Output:

PDF renders special characters correctly in name
Actual Output:

PDF shows name correctly
Result:
PASS




Test Case #10 – PDF file name format validation
Input:
customer_id = 127
language = en
Precondition:

Valid customer
Expected Output:

PDF filename: credit_card_statement_127.pdf
Actual Output:

Correct filename returned
Result:
PASS




Test Case #11 – Response content-type is PDF
Input:
customer_id = 128
language = en
Precondition:

Valid customer
Expected Output:

Response header: Content-Type = application/pdf
Actual Output:

Content-Type verified
Result:
PASS




Test Case #12 – Email address shown correctly
Input:
customer_id = 129
language = en
Precondition:

Email: user.test@dbs.com
Expected Output:

Email correctly shown in the PDF
Actual Output:

Email displayed correctly
Result:
PASS




Test Case #13 – International characters in merchant name
Input:
customer_id = 130
language = en
Precondition:

Merchant name: "Café Déjà Vu"
Expected Output:

PDF shows merchant name with accents
Actual Output:

PDF rendered correctly
Result:
PASS




Test Case #14 – Dates formatted correctly
Input:
customer_id = 131
language = en
Precondition:

Transaction dates from April 2025
Expected Output:

Date format in PDF: DD-MM-YYYY
Actual Output:

All dates correct
Result:
PASS




Test Case #15 – Negative transaction amounts (e.g., refunds)
Input:
customer_id = 132
language = en
Precondition:

Transaction amount = -20.00
Expected Output:

Negative amount shown clearly (e.g., -$20.00 or in red)
Actual Output:

Amount clearly shown
Result:
PASS




Test Case #16 – Case-insensitive language input
Input:
customer_id = 133
language = EN
Precondition:

Valid customer
Expected Output:

PDF generated in English
Actual Output:

PDF rendered correctly
Result:
PASS




Test Case #17 – HTML/JS injection in merchant name
Input:
customer_id = 134
language = en
Precondition:

Merchant: <script>alert('x')</script>
Expected Output:

Text safely escaped in PDF
Actual Output:

No script execution; safe rendering
Result:
PASS




Test Case #18 – Response time under 2 seconds
Input:
customer_id = 135
language = en
Precondition:

Valid customer
Expected Output:

PDF generated in < 2 seconds
Actual Output:

PDF response within 1.2 seconds
Result:
PASS




Test Case #19 – Different fonts per language
Input:
customer_id = 136
language = zh
Precondition:

Valid customer
Expected Output:

Noto Sans SC used for Chinese
Actual Output:

Correct font applied
Result:
PASS




Test Case #20 – Consistent currency format
Input:
customer_id = 137
language = en
Precondition:

Multiple amounts
Expected Output:

Amounts formatted like $1,000.00
Actual Output:

Correct currency format
Result:
PASS




Test Case #21 – No HTML markup in PDF content
Input:
customer_id = 138
language = en
Precondition:

Valid customer
Expected Output:

Clean PDF with no raw HTML
Actual Output:

No markup in file
Result:
PASS




Test Case #22 – Valid customer with mixed transaction types
Input:
customer_id = 139
language = en
Precondition:

Transactions include Purchase, Refund, Fee
Expected Output:

All types shown and labeled properly
Actual Output:

Correct transaction types in PDF
Result:
PASS




Test Case #23 – Language fallback if unsupported code
Input:
customer_id = 140
language = fr
Precondition:

French not supported
Expected Output:

PDF defaults to English
Actual Output:

English PDF generated
Result:
PASS




Test Case #24 – PDF accessibility (text selectable)
Input:
customer_id = 141
language = en
Precondition:

Valid customer
Expected Output:

Text selectable in PDF (not image-based)
Actual Output:

Confirmed selectable text
Result:
PASS



Test Case #25 – Repeated requests generate same PDF content
Input:
customer_id = 142
language = en
Precondition:

Valid customer
Expected Output:

Two requests return identical content
Actual Output:

No difference in content
Result:
PASS





| Test Case ID | Description | Input | Validation Rules | Expected Output | Actual Output | Result |
|--------------|-------------|-------|------------------|------------------|----------------|--------|
| TC_01 | Valid customer, low-volume transaction | `customer_id=123`, `language=en` | Required int, exists in DB, language in ['en', 'zh'] | PDF with 2 transactions, correct header and fields | As expected | PASS |
| TC_02 | Invalid customer ID | `customer_id=999` | ID must exist | HTTP 404, error message | As expected | PASS |
| TC_03 | Bilingual statement (Chinese) | `customer_id=123`, `language=zh` | Language must be 'zh' | PDF with Chinese content & fonts | As expected | PASS |
| TC_04 | Missing customer_id | (none) | `customer_id` required | HTTP 400, error message | As expected | PASS |
| TC_05 | High-volume transaction | `customer_id=124` | Paginate if > 20 txns | PDF paginated with 50 transactions | As expected | PASS |
| TC_06 | Zero transactions | `customer_id=125` | Handle 0-row gracefully | PDF with "No transactions" message | As expected | PASS |
| TC_07 | Invalid language code | `language=xx` | Language in ['en', 'zh'] | HTTP 400, invalid language | As expected | PASS |
| TC_08 | SQL injection in customer_id | `customer_id="123; DROP..."` | Must be numeric | HTTP 400, sanitized | As expected | PASS |
| TC_09 | Special characters in name | `customer_id=126` | UTF-8 required | PDF renders name with accents | As expected | PASS |
| TC_10 | PDF file name format | `customer_id=127` | Format: credit_card_statement_<id>.pdf | File name validated | As expected | PASS |
| TC_11 | Response type is PDF | `customer_id=128` | Header: application/pdf | Header validated | As expected | PASS |
| TC_12 | Email address shown | `customer_id=129` | Must appear in header | Email shown | As expected | PASS |
| TC_13 | Intl characters in merchant | `customer_id=130` | UTF-8 merchant names | Render correctly | As expected | PASS |
| TC_14 | Dates formatted | `customer_id=131` | Format: DD-MM-YYYY | All dates correct | As expected | PASS |
| TC_15 | Negative amounts | `customer_id=132` | Must display -amounts | Correct display of refund | As expected | PASS |
| TC_16 | Case-insensitive language | `language=EN` | Normalize input | Render English PDF | As expected | PASS |
| TC_17 | JS injection in merchant name | `<script>alert()</script>` | Escape HTML | Safe rendering | As expected | PASS |
| TC_18 | Response time < 2s | `customer_id=135` | Time < 2000 ms | 1.2s response | As expected | PASS |
| TC_19 | Different fonts per language | `language=zh` | Font = Noto Sans SC | Font applied | As expected | PASS |
| TC_20 | Currency format | `customer_id=137` | Format: $#,###.## | All amounts correct | As expected | PASS |
| TC_21 | No HTML markup | `customer_id=138` | Strip HTML | PDF clean | As expected | PASS |
| TC_22 | Mixed transaction types | `customer_id=139` | Support multiple types | All types shown | As expected | PASS |
| TC_23 | Language fallback | `language=fr` | Default to 'en' | English PDF | As expected | PASS |
| TC_24 | PDF accessibility | `customer_id=141` | Text selectable | Verified | As expected | PASS |
| TC_25 | Same PDF on repeat calls | `customer_id=142` | Idempotency | Identical PDFs | As expected | PASS |
