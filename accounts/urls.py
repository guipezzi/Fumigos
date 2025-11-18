from django.urls import path
import accounts.views as views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('login/',views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
]