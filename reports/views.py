from django.shortcuts import render,render_to_response
import logging


def index(request):
    return render_to_response('index.html')
