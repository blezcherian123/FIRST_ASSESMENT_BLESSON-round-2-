# dbs_statement/validation/validators.py
import re
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional, Union

class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class StatementValidator:
    """Validates input data for statement generation."""
    
    @staticmethod
    def validate_customer_id(customer_id: Any) -> int:
        """Validate customer ID.
        
        Args:
            customer_id: The customer ID to validate
            
        Returns:
            Validated customer ID as integer
            
        Raises:
            ValidationError: If customer ID is invalid
        """
        if not customer_id:
            raise ValidationError("customer_id", "Customer ID is required")
        
        try:
            customer_id = int(customer_id)
            if customer_id <= 0:
                raise ValidationError("customer_id", "Customer ID must be a positive integer")
            return customer_id
        except (ValueError, TypeError):
            raise ValidationError("customer_id", "Customer ID must be a valid integer")

    @staticmethod
    def validate_language(language: str) -> str:
        """Validate language code.
        
        Args:
            language: The language code to validate
            
        Returns:
            Validated language code
            
        Raises:
            ValidationError: If language is invalid
        """
        supported_languages = ['en', 'zh', 'ms', 'ta']
        language = language.lower() if language else 'en'
        
        if language not in supported_languages:
            raise ValidationError("language", f"Unsupported language. Must be one of: {', '.join(supported_languages)}")
        
        return language

    @staticmethod
    def validate_card_number(card_number: str) -> str:
        """Validate credit card number.
        
        Args:
            card_number: The card number to validate
            
        Returns:
            Validated card number
            
        Raises:
            ValidationError: If card number is invalid
        """
        # Remove any spaces or hyphens
        card_number = re.sub(r'[\s-]', '', card_number)
        
        # Check length and format
        if not re.match(r'^\d{16}$', card_number):
            raise ValidationError("card_number", "Card number must be exactly 16 digits")
        
        # Implement Luhn algorithm check for credit card validation
        digits = [int(d) for d in card_number]
        check_sum = 0
        
        # Double every second digit from right to left
        for i in range(len(digits) - 2, -1, -2):
            doubled = digits[i] * 2
            if doubled > 9:
                doubled -= 9
            digits[i] = doubled
        
        # Sum all digits
        check_sum = sum(digits)
        
        # Check if divisible by 10
        if check_sum % 10 != 0:
            raise ValidationError("card_number", "Invalid card number (checksum failed)")
        
        return card_number

    @staticmethod
    def validate_date(date_str: str) -> datetime:
        """Validate date string.
        
        Args:
            date_str: The date string to validate (YYYY-MM-DD)
            
        Returns:
            Validated datetime object
            
        Raises:
            ValidationError: If date is invalid
        """
        if not date_str:
            raise ValidationError("date", "Date is required")
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj
        except ValueError:
            raise ValidationError("date", "Invalid date format. Use YYYY-MM-DD")

    @staticmethod
    def validate_amount(amount: Union[str, float, int]) -> float:
        """Validate transaction amount.
        
        Args:
            amount: The amount to validate
            
        Returns:
            Validated amount as float
            
        Raises:
            ValidationError: If amount is invalid
        """
        try:
            amount = float(amount)
            # Round to 2 decimal places
            amount = round(amount, 2)
            
            if amount < 0:
                raise ValidationError("amount", "Amount cannot be negative")
                
            return amount
        except (ValueError, TypeError):
            raise ValidationError("amount", "Amount must be a valid number")

    @staticmethod
    def validate_currency(currency: str) -> str:
        """Validate currency code.
        
        Args:
            currency: The currency code to validate
            
        Returns:
            Validated currency code
            
        Raises:
            ValidationError: If currency is invalid
        """
        supported_currencies = ['USD', 'SGD', 'MYR', 'INR']
        
        if not currency:
            raise ValidationError("currency", "Currency is required")
            
        currency = currency.upper()
        
        if currency not in supported_currencies:
            raise ValidationError("currency", f"Unsupported currency. Must be one of: {', '.join(supported_currencies)}")
            
        return currency

    @staticmethod
    def validate_postal_code(postal_code: str, country: str) -> str:
        """Validate postal/ZIP code based on country.
        
        Args:
            postal_code: The postal code to validate
            country: The country code (US, SG, MY, IN)
            
        Returns:
            Validated postal code
            
        Raises:
            ValidationError: If postal code is invalid for the country
        """
        if not postal_code:
            raise ValidationError("postal_code", "Postal code is required")
            
        country = country.upper() if country else ''
        
        # Define regex patterns for different countries
        patterns = {
            'US': r'^\d{5}$',
            'SG': r'^\d{6}$',
            'MY': r'^\d{5}$',
            'IN': r'^\d{6}$'
        }
        
        if country not in patterns:
            raise ValidationError("country", f"Unsupported country code. Must be one of: {', '.join(patterns.keys())}")
            
        pattern = patterns[country]
        
        if not re.match(pattern, postal_code):
            raise ValidationError("postal_code", f"Invalid postal code format for {country}")
            
        return postal_code

    @staticmethod
    def validate_email(email: str) -> str:
        """Validate email address.
        
        Args:
            email: The email address to validate
            
        Returns:
            Validated email address
            
        Raises:
            ValidationError: If email is invalid
        """
        if not email:
            raise ValidationError("email", "Email is required")
            
        # Use a simple regex for basic email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("email", "Invalid email address format")
            
        return email