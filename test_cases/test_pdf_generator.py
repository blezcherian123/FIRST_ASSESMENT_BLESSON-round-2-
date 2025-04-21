import unittest
from app.pdf_generator import generate_pdf

class TestPDFGenerator(unittest.TestCase):
    def test_generate_pdf(self):
        customer = ("John", "Doe", "john.doe@example.com")
        transactions = []
        pdf = generate_pdf(customer, transactions)
        self.assertIsNotNone(pdf)
