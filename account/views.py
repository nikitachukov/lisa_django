import logging
import sys
import cx_Oracle
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from account.models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import traceback


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
                logger.error('The user %s exists, but does not have access' % username)
                return None

        except cx_Oracle.DatabaseError as e:
            if e.args[0].code == 1017:
                logger.debug('Please check your credentials %s (ORA-%05d)' % (username, e.args[0].code))
            else:
                logger.debug('Database connection error: ORA-%05d' % e.args[0].code)

        except:
            logger.error(traceback.format_exc())

            return False
    else:
        return False


def login(request):
    logger = logging.getLogger(__name__)
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '').upper()
        password = request.POST.get('password', '')
        db_userinfo = db_auth(username, password)
        if db_userinfo:
            logger.debug('Пользователь авторизован в Lisa')
            try:
                Profile = UserProfile.objects.get(user_id=User.objects.get(username=db_userinfo['USERNAME']).pk)
                logger.debug('Пользователь %s найден' % Profile.user.username)
                args['login_error'] = 'Welcome %s %s !!!' % (Profile.user.first_name, Profile.user.last_name)
                # Profile.user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, Profile.user)
                return redirect(reverse('reports:index'))


            except User.DoesNotExist:

                user = User.objects.create(username=username,
                                           password=password,
                                           first_name=db_userinfo['FIRSTNAME'],
                                           last_name=db_userinfo['LASTNAME'],
                                           email=db_userinfo['EMAIL'],
                                           # backend='django.contrib.auth.backends.ModelBackend'
                )

                Profile = UserProfile.objects.create(user=user,
                                                     phone=db_userinfo['PHONE'],
                                                     job=db_userinfo['JOB'])

                # Profile.user.backend='django.contrib.auth.backends.ModelBackend'

                args['login_error'] = 'Welcome %s %s !!!' % (Profile.user.first_name, Profile.user.last_name)
                logger.debug('Пользователь %s создан' % Profile.user.username)
                auth.login(request, Profile.user)
                return redirect(reverse('reports:index'))

            except Exception as E:
                logger.error(traceback.format_exc())

        else:
            logger.debug('Пользователь %s НЕ авторизован в Lisa' % username)
            args['login_error'] = 'Access denied'

    return render_to_response("login.html", args)


def logout(request):
    auth.logout(request)
    return redirect(reverse('account:login'))