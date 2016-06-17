from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from linkedin import linkedin

from .contrib.linkedin.settings import LINKEDIN_API_KEY, LINKEDIN_API_SECRET, \
    LINKEDIN_RETURN_URL, LINKEDIN_PERMISSIONS

from .models import Channel, Post


class PostList(ListView):
    """
    List view for the Post model instances.
    """
    model = Post


def save_linkedin_token(request):
    authentication = linkedin.LinkedInAuthentication(
        LINKEDIN_API_KEY, LINKEDIN_API_SECRET, LINKEDIN_RETURN_URL,
        LINKEDIN_PERMISSIONS)
    authentication.authorization_code = request.GET['code']
    token = authentication.get_access_token()
    Channel.objects.filter(source='linkedin').update(
        user_secret=authentication.authorization_code,
        user_token=token.access_token)
    messages.success(request, _('LinkedIn Channel Token updated successfully'))
    return redirect('admin:socialfeedsparser_channel_changelist')
