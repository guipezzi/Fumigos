from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

#Funcao de Cadastro
def signup_view(request):
    #Para requisicoes POST
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #logar o usuario apos cadastro
            login(request, user)
            #Redireciona para a página que o usuário tentou acessar originalmente, ou para a lista de artigos
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('articles:list')
    #Para requisicoes GET
    else:
        form = UserCreationForm()
    return render(request,'accounts/signup.html', { 'form':form })

#Funcao de Login
def login_view(request):
    #Para requisicoes POST
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #logar o usuario
            user = form.get_user()
            login(request, user)
            # Redireciona para a página que o usuário tentou acessar originalmente, ou para a lista de artigos
            next_url = request.GET.get('next', None)
            if next_url:
                return redirect(next_url)
            return redirect('articles:list')
    #Para requisicoes GET
    else:
        form = AuthenticationForm()
    return render(request,'accounts/login.html', { 'form':form })

#Funcao de Logout
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('articles:list')

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from articles.models import Article  # IMPORTANTE

def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile
    artigos = Article.objects.filter(author=user_obj).order_by('-date')

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "user_obj": user_obj,
        "artigos": artigos
    })

