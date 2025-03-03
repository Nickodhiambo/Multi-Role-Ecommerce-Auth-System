from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Vendor, Customer
from .serializers import UserSerializer, VendorSerializer, CustomerSerializer
from OTP.models import EmailOTP
from django.core.mail import send_mail


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerSignUpView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': 'Please provide all the fields'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data['user']['email']
        
        if Customer.objects.filter(user__email=email).exists():
            return Response(
                {'error': 'Customer with this email already exists'},
                status=status.HTTP_409_CONFLICT
            )

        try:
            user_data = request.data.pop('user')
            user = User.objects.create_user(**user_data)
            customer = Customer.objects.create(user=user, **serializer.validated_data)
            customer.save()

            otp_instance, created = EmailOTP.objects.get_or_create(user=user)
            
            if not created and otp_instance.is_expired:
                otp_instance.generate_otp()
            else:
                otp_instance.generate_otp()

            send_mail(
                'OTP for site',
                f'Your OTP is {otp_instance.otp}',
                'nodhiambo01@gmail.com',
                [email],
                fail_silently=False
            )
            
            return Response(
                {'message': 'Customer successfully created. Please check your email to activate your account'},
                status=status.HTTP_201_CREATED
                )
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
                )
        
class VendorSignUpView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        email = request.data.get('user', {}).get('email')

        if not email:
            return Response({
                'error': 'Email field is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)

            if user.role == 'customer':
                user.role = 'vendor'
                user.save()
                return self._register_vendor(user, request)
            else:
                return Response({
                    'message': 'User is already registered with a business account'
                })
        except User.DoesNotExist:
            
            user_data = request.data.pop('user')
            user = User.objects.create_user(**user_data)
            return self._register_vendor(user, request)
        
        
    def _register_vendor(self, user, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            vendor = Vendor.objects.create(user=user, **serializer.validated_data)
            vendor.save()

            otp_instance, created = EmailOTP.objects.get_or_create(user=user)
            
            if not created and otp_instance.is_expired:
                otp_instance.generate_otp()
            else:
                otp_instance.generate_otp()

            send_mail(
                'OTP for site',
                f'Your OTP is {otp_instance.otp}',
                'nodhiambo01@gmail.com',
                [user.email],
                fail_silently=False
            )
            return Response({
                'message': 'A OTP has been sent to your email.'
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response_data = {
                    'message': 'Logged in successfully',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }

                if user.role == 'customer':
                    customer = user.customer
                    if customer is not None:
                        customer_data = CustomerSerializer(customer).data
                        response_data['user_data'] = customer_data
                        response_data['redirect_to'] = 'customer_dashboard'
                
                if user.role == 'vendor':
                    vendor = user.vendor
                    if vendor is not None:
                        vendor_data = VendorSerializer(vendor).data
                        response_data['user_data'] = vendor_data
                        response_data['redirect_to'] = 'vendor_dashboard'
                
                return Response(
                    response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Please activate your account'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response({
                'error': 'Invalid credentials',
            }, status=status.HTTP_401_UNAUTHORIZED)
        

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)


class CheckUserExistence(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({
                'message': 'Email field is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            return Response({
                'exists': True, 'message': 'User already exists'
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                'exists': False, 'message': 'User does not exists'
                }, status=status.HTTP_200_OK)
        
