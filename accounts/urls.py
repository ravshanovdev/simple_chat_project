from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import UserRegistrationApiView, VerifyCodeTokenAPIView

urlpatterns = [
    path('register/', UserRegistrationApiView.as_view(), ),
    path('login/', VerifyCodeTokenAPIView.as_view(), ),
    path('token-refresh/', TokenRefreshView.as_view(), )

]


