from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()


def create_jwt_pair_tokens(user: User, counselor=None):
    refresh = RefreshToken.for_user(user)

    refresh['email'] = user.email
    refresh['id'] = user.id
    refresh['role'] = user.role
    refresh['name'] = f'{user.first_name} {user.last_name}'
    refresh['is_active'] = user.is_active

    if counselor is not None:
        refresh['counselor'] = counselor
        
    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

    return tokens
