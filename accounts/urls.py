from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet, VendorViewSet, LoginView, LogoutView,
    CustomerSignUpView, VendorSignUpView, CheckUserExistence
)



router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('vendors', VendorViewSet)

app_name = 'accounts'

urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/signup/customer/', CustomerSignUpView.as_view(), name='customer_signup'),
    path('api/signup/vendor/', VendorSignUpView.as_view(), name='vendor_signup'),
    path('api/check-user/', CheckUserExistence.as_view(), name='check_user_existence'),
]