from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from hashlib import md5
import logging
import traceback
import cx_Oracle
from django.conf import settings


def db_auth(username, password):
    logger = logging.getLogger(__name__)

    if username and password:
        try:
            dsn_tns = cx_Oracle.makedsn(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'], settings.DATABASES['default']['NAME'])
            con = cx_Oracle.connect(username, password[::-1], dsn_tns)
            cursor = con.cursor()
            cursor.execute("set role lisaro identified by lisaro")
            cursor.execute("SELECT username,lastname,firstname,middlename,phone,email,job FROM lisa.usr_django_auth WHERE username=user")
            row = cursor.fetchone()
            if row:
                return dict(zip([x[0] for x in cursor.description], row))
            else:
                logger.info('Пользователь %s существует, но не имеет доступа к системе' % username)
        except cx_Oracle.DatabaseError as e:
            if e.args[0].code == 1017:
                pass
            else:
                logger.critical('Database connection error: ORA-%05d' % e.args[0].code)
        except:
            logger.error(traceback.format_exc())
            return False


class LisaBackend(object):
    def authenticate(self, username=None, password=None):
        logger = logging.getLogger(__name__)
        try:
            lisa_user = db_auth(username=username, password=password)

            if lisa_user:
                try:
                    logger.info('Пользователь %s авторизован в LISA (%s)' % (username, md5(password.encode('utf-8')).hexdigest().upper()))
                    user = User.objects.get(username=username, is_staff=False, is_superuser=False)
                    logger.info('Пользователь найден (ID=%d)' % user.pk)
                    user.userprofile.phone = lisa_user['PHONE']
                    user.userprofile.job = lisa_user['JOB']
                    user.userprofile.save()
                    logger.info('Профиль пользователя обновлен')
                    return user
                except User.DoesNotExist:
                    user = User(username=username,
                                first_name=lisa_user['FIRSTNAME'],
                                last_name=lisa_user['LASTNAME'],
                                email=lisa_user['EMAIL'])
                    user.save()
                    logger.info('Пользователь создан (ID=%d)' % user.pk)
                    user.userprofile.phone = lisa_user['PHONE']
                    user.userprofile.job = lisa_user['JOB']
                    user.userprofile.save()
                    logger.info('Профиль пользователя создан (ID=%d)' % user.userprofile.pk)
                    return user
            else:
                logger.info('Пользователь %s НЕ авторизован в LISA (%s)' % (username, md5(password.encode('utf-8')).hexdigest().upper()))

        except Exception:
            logger.error(traceback.format_exc())

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def login(request):
    logger = logging.getLogger(__name__)

    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '').upper()
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            logger.info('Пользователь %s вошел в систему' % user.username)
            return redirect(reverse('reports:index'))
        else:

            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


def logout(request):
    logger = logging.getLogger(__name__)
    logger.info('Пользователь %s вышел из системы' % request.user.username)
    auth.logout(request)
    return redirect(reverse('account:login'))