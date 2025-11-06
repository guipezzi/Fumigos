from django.contrib import admin    
from django.urls import path, re_path, include #O include permite importar URL's de outros apps, como articles por exemplo.
from . import views #importa o views no próprio diretorio para referenciar as URL's

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include ('articles.urls')), #Django procura dentro de Articles.urls pela referência articles, desta forma importando as url de articles de outro arquivo
    path('about',  views.about), #Dispara a função about do views quando alguem visitar essa URL
    path('', views.homepage), #URL da Homepage. Dispara a função homepage do views quando alguem visitar essa URL
]
