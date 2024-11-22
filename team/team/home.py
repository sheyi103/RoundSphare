from django.http import HttpResponse
from django.shortcuts import render

def landing_page(request):
    name = request.session['name']
    return render(request, "index.html", {"name": name})