import string
import secrets

class SendEmailHelper:
    def makeRandomCode(self):
        digit_and_alpha = string.ascii_letters + string.digits
        return "".join(secrets.choice(digit_and_alpha) for _ in range(6))

sendEmailHelper = SendEmailHelper()