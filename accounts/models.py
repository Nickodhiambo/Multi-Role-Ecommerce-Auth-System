from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Permission, PermissionsMixin, Group


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, role, password=None):
        if not email:
            raise ValueError('Please provide an email address')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role
        )
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, role, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            role=role
        )

        user.is_admin=True
        user.is_staff=True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=50)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=15, null=True, choices=ROLE_CHOICES)
    date_joined = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(
        Group,
        related_name='core_user_set',
        help_text='This group belongs to this user',
        verbose_name='group',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='core_user_permission',
        blank=True,
        help_text='Specific user permissions',
        verbose_name='user permissions',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    
    def __str__(self):
        return self.email
    
    
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    business_name = models.CharField(max_length=255)
    business_address = models.CharField(max_length=300)
    bio = models.TextField()
    contact_details = models.CharField(max_length=300)
    payment_details = models.CharField(max_length=300)
    shipping_policy = models.TextField()
    return_policy = models.TextField()
    license = models.ImageField(upload_to='business_documents/', null=True)
    
    def __str__(self):
        return self.business_name
    

class Customer(models.Model):
    
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer')
    
    def __str__(self):
        return self.user.email