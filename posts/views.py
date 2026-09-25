from datetime import datetime

from django.http.response import HttpResponse

# Create your views here.


def hello(r):
    return HttpResponse("Hello <h1>world!</h1>")


def name(r):
    name = "Islam"
    return HttpResponse(f"Hello <h1>{name}</h1>")


def time(r):
    dt = datetime.now()

    return HttpResponse(f"NOW: {dt.strftime('%d-%m-%Y %H:%M:%S')}")
