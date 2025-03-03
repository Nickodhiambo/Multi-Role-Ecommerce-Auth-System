from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import EmailOTP
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

class VerifyOTPView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        email = request.data.get('user', {}).get('email')
        otp_code = request.data.get('otp')

        if not email or not otp_code:
            return Response({"error": "Email and OTP are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            otp_instance = EmailOTP.objects.get(user=user, otp=otp_code)

            if otp_instance.is_verified:
                return Response({"message": "Email is already verified."},
                                status=status.HTTP_200_OK)

            if otp_instance.is_expired():
                return Response({"error": "OTP has expired. Please request a new one."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Mark the OTP as verified and activate the user
            otp_instance.is_verified = True
            otp_instance.save()
            user.is_active = True  # Activate the user's account
            user.save()

            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                'message': 'Logged in successfully',
                'access_token': access_token,
                'refresh_token': refresh_token,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except (User.DoesNotExist, EmailOTP.DoesNotExist):
            return Response({"error": "Invalid OTP or email."},
                            status=status.HTTP_400_BAD_REQUEST)
