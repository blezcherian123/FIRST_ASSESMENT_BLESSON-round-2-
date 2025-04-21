# 🛡️ Validation Rules for Credit Card Statement Generator

This document outlines the validation rules enforced in the system to ensure data integrity and correctness.

---

## 💳 Card Details

- **Card Number**
  - Must be exactly 16 digits
  - Numeric only (no spaces or hyphens)
  - Reject if contains letters or wrong length

- **Card Expiry**
  - Format: `MM/YY`
  - Must be a future date
  - Reject if expired

- **CVV**
  - Must be exactly 3 digits
  - Numeric only

---

## 📅 Date Fields

- **Transaction Date**
  - Format: `YYYY-MM-DD`
  - Must be a valid calendar date
  - Reject if empty or malformed

- **Statement Period**
  - Start Date < End Date
  - Same format: `YYYY-MM-DD`

---

## 🏦 Bank & User Info

- **Name**
  - Only alphabets and spaces allowed
  - Max 50 characters

- **ZIP / Postal Code**
  - US: 5 digits
  - SG: 6 digits
  - MY: 5 digits
  - Reject if format mismatches bank country

- **Email**
  - Must be valid email format (e.g., `user@bank.com`)

---

## 💰 Currency & Amounts

- **Currency**
  - Accept: `USD`, `SGD`, `MYR`, `INR`
  - Reject other currencies

- **Amount**
  - Numeric only
  - Up to 2 decimal places
  - Must be >= 0

---

## 📄 PDF Format Rules

- Statement must include:
  - Bank name + logo
  - Customer name and masked card number
  - List of transactions
  - Reward points (if applicable)
  - Total due and due date
  - Bilingual content if enabled

---

## ✅ Input Acceptance Criteria Summary

| Field           | Required | Format       | Validation Example                |
|----------------|----------|--------------|----------------------------------|
| Card Number     | Yes      | 16 digits    | `1234567812345678`               |
| Date            | Yes      | YYYY-MM-DD   | `2025-04-15`                     |
| Currency        | Yes      | Uppercase    | `USD`, `SGD`                     |
| Amount          | Yes      | Float (>= 0) | `99.99`                          |
| ZIP Code        | Yes      | Region-based | `12345` (US), `560001` (IN)     |

---

## 🚫 Rejection Scenarios

- Invalid card number format
- Empty required fields
- Expired card
- Unsupported currency
- Negative amount
- Invalid dates


## Validation Rules

1. File type must be CSV or XLSX.
2. Maximum file size: 5MB.
3. Required columns: account_number, amount, date.
4. Amount > 10,000 is flagged as high value.
5. Date format must be valid.
