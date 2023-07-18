from rest_framework.validators import ValidationError
import random
import string
from .models import RandomTokenGenerator

def generate_token(token_length=33,id=None):
    characters = string.ascii_letters + string.digits  # Generate token using letters and digits
    token = ''.join(random.choice(characters) for _ in range(token_length))
    token = token.__add__(f'@{id}')
    
    if RandomTokenGenerator.objects.filter(token=token).exists():
        generate_token()

    return token

