from django.test import TestCase
from datetime import datetime
from production.servicelayer import parse_expiration_date

class ParseExpirationDateTests(TestCase):

    def test_parse_expiration_date(self):
        # 테스트 코드 작성
        text = "The expiration date is 2024-09-15."
        result = parse_expiration_date(text)
        self.assertEqual(result, datetime.strptime('2024-09-15', '%Y-%m-%d').date())