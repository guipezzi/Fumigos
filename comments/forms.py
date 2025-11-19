from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from articles.models import Article
from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] 

@login_required
def add_comment(request, article_id):
    """
    Adiciona um comentário a um artigo.
    Permite resposta a outro comentário através de parent_id.
    """
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        parent_id = request.POST.get('parent_id')

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article

            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id, article=article)
                comment.parent = parent_comment

            comment.save()

    return redirect('articles:detail', article_id=article.id)


@login_required
def edit_comment(request, comment_id):
    """
    Edita um comentário existente, apenas se for do autor.
    """
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_id=comment.article.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comments/edit_comment.html', {
        'form': form,
        'comment': comment
    })


@login_required
def delete_comment(request, comment_id):
    """
    Deleta um comentário existente, apenas se for do autor.
    Apenas POST é aceito para deletar.
    """
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        article_id = comment.article.id
        comment.delete()
        return redirect('articles:detail', article_id=article_id)

    return redirect('articles:detail', article_id=comment.article.id)
