from django import template
from django.contrib.postgres.search import SearchVector

from ..models import Bookmark, Snippet, SnippetFlag

register = template.Library()


@register.filter
def is_bookmarked(snippet, user):
    """
    {% if snippet|is_bookmarked:request.user %}
        already bookmarked
    {% else %}
        not bookmarked yet
    {% endif %}
    """
    return (
        Bookmark.objects.filter(snippet=snippet, user=user).exists()
        if user.is_authenticated
        else False
    )


@register.filter
def has_flagged(user, snippet):
    return (
        SnippetFlag.objects.filter(snippet=snippet, user=user).exists()
        if user.is_authenticated
        else False
    )


@register.filter
def more_like_this(snippet, limit=None):
    try:
        sqs = Snippet.objects.annotate(
            search=SearchVector(
                "language__name",
            )
        )
        sqs = sqs.filter(language__name=snippet.language)
        if limit is not None:
            sqs = sqs[:limit]
    except AttributeError:
        sqs = []
    return sqs
