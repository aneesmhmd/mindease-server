from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()


def create_jwt_pair_tokens(user: User):
    refresh = RefreshToken.for_user(user)

    refresh['email'] = user.email
    refresh['role'] = user.role
    refresh['is_active'] = user.is_active
    
    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

    return tokens
