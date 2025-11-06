from django.shortcuts import render

def article_list(request):
    return render(request, 'articles/article_list.html' ) #Renderiza o template da lista de artigos