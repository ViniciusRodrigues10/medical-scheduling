from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email is not given.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff = True')
        
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser = True')  
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    GENDER_CHOICES = (
        (1, 'male'),
        (2, 'female'),
        (3, 'other')
    )

    USER_TYPE_CHOICES = (
        (1, 'patient'),
        (2, 'doctor')
    )

    id_user = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    password = models.CharField(max_length=128, blank=False, null=True)
    first_name = models.CharField(max_length=255, blank=False, null=True,)
    last_name = models.CharField(max_length=255, blank=False, null=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, blank=False)
    telephone = models.CharField(max_length=15, blank=False, null=True)
    date_of_birth = models.DateField(blank=False, null=True)
    user_type = models.SmallIntegerField(choices=GENDER_CHOICES, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'user_type']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    specialty = models.CharField(max_length=255)
    crm = models.CharField(max_length=50, unique=True)
    biography = models.TextField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.specialty}' 
