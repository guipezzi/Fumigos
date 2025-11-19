from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from articles.models import Article
from .forms import ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect("accounts:profile", username=user.username)
    else:
        form = UserCreationForm()

    return render(request,'accounts/signup.html', { 'form':form })


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('accounts:profile', args=[request.user.username]))

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)

            return redirect(reverse('accounts:profile', args=[user.username]))
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@never_cache
def profile_view(request, username):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile
    articles = Article.objects.filter(author=user_obj).order_by('-date')

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "user_obj": user_obj,
        "articles": articles
    })


@never_cache
@login_required
def edit_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect(f'/accounts/profile/{request.user.username}/')

    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })

@never_cache
@login_required
def search_view(request):
    """
    Busca perfis por username ou display_name.
    Query string: ?q=texto
    Mostra perfis encontrados e, para cada perfil, alguns artigos recentes.
    """

    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    q = request.GET.get('q', '').strip()

    results = []
    page_obj = None

    if q:
        users_qs = User.objects.filter(
            Q(username__icontains=q) |
            Q(profile__display_name__icontains=q)
        ).distinct().order_by('username')

        paginator = Paginator(users_qs, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        results = []
        for user in page_obj:
            recent_articles = Article.objects.filter(author=user).order_by('-date')[:3]
            results.append({
                'user': user,
                'profile': getattr(user, 'profile', None),
                'recent_articles': recent_articles
            })

    return render(request, 'accounts/search_results.html', {
        'query': q,
        'results': results,
        'page_obj': page_obj
    })