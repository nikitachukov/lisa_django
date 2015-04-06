from django.conf import settings
from django.contrib.auth.models import User, check_password
from account.lisa_auth import db_auth


class SettingsBackend(object):
    """
    """

    def authenticate(self, username=None, password=None):
        lisa_user = db_auth(username=username, password=password)

        if lisa_user:
            try:
                user = User.objects.get(username=username, is_staff=False, is_superuser=False)
            except User.DoesNotExist:
                user = User(username=username, password=password)
                user.is_staff = False
                user.is_superuser = False
                user.save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None