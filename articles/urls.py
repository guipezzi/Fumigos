from django.urls import path, re_path
from . import views #importa o views no próprio diretorio para referenciar as URL's

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name="list"), #URL da lista de artigos
    path('<slug:slug>/', views.article_detail, name="detail"), #URL individual de cada artigo
]
