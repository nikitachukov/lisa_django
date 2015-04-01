from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
import logging

from django.conf import settings

@login_required
def index(request):
    logger = logging.getLogger(__name__)
    logger.debug(settings.LOGIN_URL)
    return render_to_response('index.html')
