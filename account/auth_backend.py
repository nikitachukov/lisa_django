from django.contrib.auth.models import User
from account.lisa_auth import db_auth


class SettingsBackend(object):
    def authenticate(self, username=None, password=None):
        lisa_user = db_auth(username=username, password=password)

        if lisa_user:
            try:
                user = User.objects.get(username=username, is_staff=False, is_superuser=False)
                user.userprofile.phone = lisa_user['PHONE']
                user.userprofile.job = lisa_user['JOB']
                user.userprofile.save()

            except User.DoesNotExist:
                user = User(username=username)
                user.is_staff = False
                user.is_superuser = False
                user.first_name = lisa_user['FIRSTNAME']
                user.last_name = lisa_user['LASTNAME']
                user.email = lisa_user['EMAIL']
                user.save()
                user.userprofile.phone = lisa_user['PHONE']
                user.userprofile.job = lisa_user['JOB']
                user.userprofile.save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None