from django.shortcuts import render, redirect
from .models import Article
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms

def article_list(request):
    articles = Article.objects.all().order_by('date') #Recupera todos os objetos de artigos ordenados por data
    return render(request, 'articles/article_list.html', {'articles':articles} ) #Renderiza o template da lista de artigos e associa a variavel artigos

def article_detail(request, slug): #Captura a URL digitada pelo usuario
    #return HttpResponse(slug) 
    article = Article.objects.get(slug=slug)
    return render(request,'articles/article_detail.html', {'article':article})

@login_required(login_url='/accounts/login/')
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            #salvar artigo no banco de dados
            instance =form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    # Quando o usuário faz login, será redirecionado de volta para /articles/create/ através do parâmetro 'next'
    return render(request, 'articles/article_create.html', { 'form': form })