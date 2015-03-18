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
            con = cx_Oracle.connect(username, password[::-1], dsn_tns)
            cursor = con.cursor()
            cursor.execute('select username,lastname,firstname,middlename,phone,email,job from lisa.usr_django_auth where username=user')
            row = cursor.fetchone()

            if row:
                return dict(zip([x[0] for x in cursor.description], row))
            else:
                logger.error('The user %s exists, but does not have access' % username)
                return None

        except cx_Oracle.DatabaseError as e:
            logger.error(str(e.args[0].code))
            # logger.error(str(e.args[0]))
            if e.args[0].code == 1017:
                logger.error('Please check your credentials.(%s)' % username)
            else:
                logger.error('Database connection error: %s'%(e.args[0].code))
                logger.error('Database connection error: %s'%(str(e.args)))

            return False
    else:
        return False


def login(request):
    logger = logging.getLogger(__name__)

    # username = 'CHUKOVNA'.upper()
    # password = '2wsx@WSX'

    #
    # logger.debug( db_auth(username, password))
    #

    args = {}
    args.update(csrf(request))
    if request.POST:

        username = request.POST.get('username', '').upper()
        password = request.POST.get('password', '')

        db_userinfo = db_auth(username, password)

        if db_userinfo:
            logger.debug(db_userinfo)
            args['login_error'] = 'Welcome %s %s %s !!!' % (db_userinfo['LASTNAME'], db_userinfo['FIRSTNAME'], db_userinfo['MIDDLENAME'])
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username, password=password, first_name=db_userinfo['FIRSTNAME'], last_name=db_userinfo['LASTNAME'],email=db_userinfo['EMAIL'])
                user.is_staff = True
                user.is_superuser = False
                user.userprofile.phone=db_userinfo['PHONE']
                user.userprofile.job=db_userinfo['JOB']
                user.save()



                # profile.save()
        else:
            args['login_error'] = 'Access denied'

    return render_to_response('login.html', args)





    # user = auth.authenticate(username=username, password=password)
    #
    #     if user is not None:
    #         auth.login(request, user)
    #         return redirect('/')
    #     else:
    #         args['login_error'] = 'Пользователь не найден'
    #         return render_to_response('account/login.html', args)
    # else:
    #     return render_to_response('account/login.html', args)


# Create your views here.
