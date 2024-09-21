import random
import string
from .models import Customer

def generate_unique_code():
    length = 8
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not Customer.objects.filter(code=code).exists():
            return code