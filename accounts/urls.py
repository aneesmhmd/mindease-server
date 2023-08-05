from django.urls import path, include
from . import views
from . views import *
from . views_profile import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.get_routes),
    path('user-auth/', views.user_auth, name='user-auth'),
    path('register/', UserRegistration.as_view()),
    # path('login/', MyTokenObtainPairView.as_view()),
    path('activate/<uidb64>/<token> ', views.activate, name='activate'),

    path('forgot-password/', ForgotPassword.as_view()),
    path('reset-validate/<uidb64>/<token> ',
         views.reset_validate, name='reset_validate'),
    path('reset-password/', ResetPassword.as_view()),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google_authentication/', GoogleAuthentication.as_view()),

    path('user-profile/<int:id>/', UserProfile.as_view()),
    path('update-profile/<int:id>/', UpdateUserProfile.as_view()),
    path('change-password/<int:id>/', ChangePassword.as_view()),
    path('update-profile-photo/<int:id>/', UpdateUserProfilePhoto.as_view()),
    path('remove-profile-photo/<int:id>/', RemoveUserProfilePhoto.as_view()),
]
