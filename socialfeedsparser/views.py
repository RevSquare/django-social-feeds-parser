from django.views.generic import ListView

from .models import Post


class PostList(ListView):
    """
    List view for the Post model instances.
    """
    model = Post
