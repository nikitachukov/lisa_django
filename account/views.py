from django.shortcuts import render
from django.db import connection
from django.contrib import auth
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
import sys, traceback
from django.conf import settings
import logging
import cx_Oracle

from account.models import *


def db_auth(username, password):
    logger = logging.getLogger(__name__)

    if username and password:
        try:

            dsn_tns = cx_Oracle.makedsn(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'], settings.DATABASES['default']['NAME'])
            logger.debug(username)
            logger.debug(password)
            con = cx_Oracle.connect(username, password[::-1], dsn_tns)
            cursor = con.cursor()
            cursor.execute('set role lisaro identified by lisaro')
            cursor.execute('select username,lastname,firstname,middlename,phone,email,job from lisa.usr_django_auth where username=user')
            row = cursor.fetchone()

            if row:
                return dict(zip([x[0] for x in cursor.description], row))
            else:
                logger.error('The user %s exists, but does not have access' % username)
                return None

        except cx_Oracle.DatabaseError as e:
            # logger.error(str(e.args[0]))
            if e.args[0].code == 1017:
                logger.debug('Please check your credentials %s (ORA-%s)' % (username,str(e.args[0].code)))
            else:
                logger.debug('Database connection error: ORA-%s' % (str(e.args[0].code)))

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
                logger.debug('Пользователь %s найден'%Profile.user.username)
                args['login_error'] = 'Welcome %s %s !!!' % (Profile.user.first_name,Profile.user.last_name)


            except User.DoesNotExist:
                Profile=UserProfile.objects.create(user=User.objects.create(username=username,
                                                                    password=password,
                                                                    first_name=db_userinfo['FIRSTNAME'],
                                                                    last_name=db_userinfo['LASTNAME'],
                                                                    email=db_userinfo['EMAIL']),
                                           phone=db_userinfo['PHONE'],
                                           job=db_userinfo['JOB'])
                args['login_error'] = 'Welcome %s %s !!!' % (Profile.user.first_name,Profile.user.last_name)
                logger.debug('Пользователь %s создан'%Profile.user.username)
        else:
            logger.debug('Пользователь %s НЕ авторизован в Lisa'%username)
            args['login_error'] = 'Access denied'

    return render_to_response("login.html", args)
