from django import forms
from . import models

class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'body', 'slug', 'thumb']
        labels = {
            'title': 'Título',
            'body': 'Corpo',
            'slug': 'Slug',
            'thumb': 'Imagem'
        }