from django.shortcuts import render
from .models import Article
from django.http import HttpResponse
def article_list(request):
    articles = Article.objects.all().order_by('date') #Recupera todos os objetos de artigos ordenados por data
    return render(request, 'articles/article_list.html', {'articles':articles} ) #Renderiza o template da lista de artigos e associa a variavel artigos

def article_detail(request, slug): #Captura a URL digitada pelo usuario
    return HttpResponse(slug)