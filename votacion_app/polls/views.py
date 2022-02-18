from django.shortcuts import render

# Create your views here.

# Importo modulo que permite ejecutar respuesta http

from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello World')