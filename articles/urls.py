from django.urls import path, re_path
from . import views #importa o views no próprio diretorio para referenciar as URL's

urlpatterns = [
    path('', views.article_list ), #URL da lista de artigos
]
