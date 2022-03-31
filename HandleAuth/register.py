from datetime import datetime
from django.contrib.auth import authenticate
from HandleAuth.models import User
import random
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):

    filtered_user_by_email = User.objects.filter(email=email)
    print("filtered_user_by_email: ", filtered_user_by_email)

    if filtered_user_by_email.exists():
        print("PROVIDER NAME: ", provider)
        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=settings.SOCIAL_SECRET)
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens(),
                'user_id': registered_user.id,
                'is_superuser': registered_user.is_superuser,
            }

        else:
            if filtered_user_by_email[0].auth_provider == None:
                raise AuthenticationFailed(
                    detail='Please continue your login using registered email and password')
            else:
                raise AuthenticationFailed(
                    detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': settings.SOCIAL_SECRET}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()
        new_user = authenticate(
            email=user.email, password=settings.SOCIAL_SECRET)
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens(),
            'user_id': user.id,
            'is_superuser': new_user.is_superuser,
        }
