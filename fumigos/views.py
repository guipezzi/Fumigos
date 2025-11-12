from django.http import HttpResponse
from django.shortcuts import render

def homepage (request):
    #retorna HttpResponse('homepage')
    return render(request, 'homepage.html') #referencia a pagina homapage HTML dentro de templates

def about (request):
    #retorna HttpResponse('about')
    return render(request, 'about.html') #referencia a pagina about dentro de templates

