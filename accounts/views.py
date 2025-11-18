from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from articles.models import Article
from .forms import ProfileEditForm
from django.contrib.auth.decorators import login_required

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


def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile
    articles = Article.objects.filter(author=user_obj).order_by('-date')

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "user_obj": user_obj,
        "articles": articles
    })


@login_required
def edit_profile_view(request):
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
