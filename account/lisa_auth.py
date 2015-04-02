__author__ = 'Nikitos'
import cx_Oracle
from django.conf import settings
import logging
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
