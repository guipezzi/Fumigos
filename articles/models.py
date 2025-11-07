from django.db import models

'''Nesta classe serao armazenados os models, itens presentes no banco de dados
Cada um de seus atributos sera uma caraceteristica que esse item tera.
Django ja tem preparacoes e validacoes para alguns tipos de dados, como o
slug por exemplo'''

class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField() #slug se refere a parte legivel da url
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True) #os parametros dessa funcao fazem com que seja automaticmente preenchida a data e hora ao criar o objeto
    #thumb
    #author
