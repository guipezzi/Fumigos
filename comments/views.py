from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from articles.models import Article
from .models import Comment
from .forms import CommentForm

@login_required
def add_comment(request, article_id):
    """
    Adiciona um comentário em um artigo ou responde a um comentário existente.
    """
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')

        if content:
            parent_comment = get_object_or_404(Comment, id=parent_id) if parent_id else None

            Comment.objects.create(
                article=article,
                author=request.user,
                content=content,
                parent=parent_comment
            )

    return redirect('articles:detail', slug=article.slug)


@login_required
def edit_comment(request, comment_id):
    """
    Edita um comentário do usuário logado.
    """
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', slug=comment.article.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comments/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    """
    Deleta um comentário do usuário logado.
    """
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    article_slug = comment.article.slug
    comment.delete()
    return redirect('articles:detail', slug=article_slug)
