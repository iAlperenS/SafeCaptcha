import random, time, secrets

# Raw captcha response oluşturmak için
class APOCaptcha:
    def __init__(self):
        self.token_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        self.token_length = 64

        self.captcha_num1 = None
        self.captcha_num2 = None
        self.captcha_express1 = None
        self.captcha_id = None
        self.answer = None

    def generate_captcha_1(self): self.captcha_num1 = random.randint(1, 36)
    def generate_captcha_2(self):
        self.captcha_num2 = random.randint(1, 36) if self.captcha_num1 < 10 else random.randint(1, 9)
    def generate_captcha_3(self): self.captcha_express1 = random.choice(['+', '-'])
    def generate_captcha_4(self):
        self.captcha_id = ''.join(secrets.choice(self.token_chars) for _ in range(self.token_length))

    def calculate(self, num1, op, num2):
        return num1 + num2 if op == '+' else num1 - num2

    def result(self):
        self.generate_captcha_1()
        self.generate_captcha_2()
        self.generate_captcha_3()
        self.generate_captcha_4()
        self.answer = self.calculate(self.captcha_num1, self.captcha_express1, self.captcha_num2)
        return {
            "id": self.captcha_id,
            "raw": f"{self.captcha_num1}{self.captcha_express1}{self.captcha_num2}",
            "answer": self.answer,
            "time": time.time()
        }