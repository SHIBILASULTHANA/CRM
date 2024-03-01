from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    usertype = models.CharField(
        max_length=128,
        choices=[
            ("Employee", "Employee"),
            ("Client", "Client"),
        ],
        default="Administrator",
    )
    objects = CustomUserManager()


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee', null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    mobile = models.BigIntegerField(
        validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ]
    )
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='----')

    def __str__(self):
        return self.name

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client', null=True)
    SALUTATION_CHOICES = [
        ('MR', 'Mr.'),
        ('MRS', 'Mrs.'),
        ('MISS', 'Miss'),
        ('DR', 'Dr.'),
    ]
    salutation = models.CharField(max_length=5, choices=SALUTATION_CHOICES, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    client_name = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=50)
    mobile = models.BigIntegerField(
        validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ]
    )
    client_category = models.CharField(max_length=50)
    can_login = models.BooleanField(default=False)
    receive_notifications = models.BooleanField(default=False)

    # Company Details
    company_name = models.CharField(max_length=100)
    official_website_count = models.PositiveIntegerField()
    gst_vat_number = models.CharField(max_length=20)
    office_phone_number = models.BigIntegerField(
        validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ]
    )
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    company_address = models.TextField()

    def __str__(self):
        return f"{self.get_salutation_display()} {self.client_name}"

