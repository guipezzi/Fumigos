from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from django.views.decorators.cache import never_cache

@never_cache
def article_list(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    articles = Article.objects.all().order_by('date') 
    return render(request, 'articles/article_list.html', {'articles':articles})

@never_cache
def article_detail(request, slug):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    article = get_object_or_404(Article, slug=slug)
    
    root_comments = article.comments.filter(parent__isnull=True).order_by('-created_at')
    
    return render(request, 'articles/article_detail.html', {
        'article': article,
        'root_comments': root_comments
    })

@never_cache
@login_required(login_url='/accounts/login/')
def article_create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect("accounts:profile", username=request.user.username)
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', {'form': form})