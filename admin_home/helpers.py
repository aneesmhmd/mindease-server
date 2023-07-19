from rest_framework.validators import ValidationError
import random
import string
from .models import RandomTokenGenerator

def generate_token(token_length=33):
    characters = string.ascii_letters + string.digits  # Generate token using letters and digits
    token = ''.join(random.choice(characters) for _ in range(token_length))
    
    if RandomTokenGenerator.objects.filter(token=token).exists():
        generate_token()

    return token

def generate_random_password(password_length=13):
    characters = string.ascii_letters + string.digits + '@&#$'
    password = ''.join(random.choice(characters) for _ in range(password_length))
    
    return password

