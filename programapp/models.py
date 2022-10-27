
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid




class UserManger(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError('Users Must Have an email address')
        user = self.model(
            email=self.normalize_email(email),

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user=self.create_user(email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser):
        id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
        email=models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
        )
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)
        is_superuser = models.BooleanField(default=False)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = [ ]
        objects = UserManger()



        def __str__(self):
            return self.email

        class Meta:
            db_table = "login"







class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
    age = models.PositiveIntegerField(null=False, blank=False)
    # img=models.ImageField(upload_to='product',blank=True)
    # img_cover=models.ImageField(upload_to='products',blank=True)

    class Meta:
        db_table = "profile"

    def __str__(self):
        return self.first_name

