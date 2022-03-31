from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken



class UserManager(BaseUserManager):

    def create_user(self, email, password=None, username=None):

        if not username:
            raise ValueError('Users Must Have an username')

        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            email=email, password=password, username=email.split('@')[0])
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


AUTH_PROVIDERS = {
    'google': 'google', 'email': 'email'
}


class User(AbstractBaseUser):

    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def get_username(self) -> str:
        return super().get_username()

    def __str__(self):
        return self.username

    class Meta:

        db_table = "UsersTable"


class UserFiles(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.TextField(null=True)
    file_size = models.CharField(max_length=100, null=True)
    file_type = models.CharField(max_length=100,null=True )
    created_on =  models.DateTimeField()
    update_on = models.DateTimeField()

    def __str__(self):
        return self.file_name

    class Meta:
        db_table = "userfiles"
        ordering = ['created_on']