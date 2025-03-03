from django.urls import path
from .views import VerifyOTPView

urlpatterns = [
    path('api/verify-email/', VerifyOTPView.as_view(), name='verify_otp'),
]