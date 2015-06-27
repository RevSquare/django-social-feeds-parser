from django.db import models


class ChannelManager(models.Manager):
    """
    Manager class for the SpokeSource model.
    """

    def published(self):
        """
        Returns published sources.
        """
        return self.all().filter(is_active=True)

    def to_update(self):
        """
        Return sources to update.
        """
        queryset = self.published()
        return [channel for channel in queryset if channel.can_update()]


class PostManager(models.Manager):
    """
    Manager class for the SpokeAboutUs model.
    """

    def published(self):
        """
        Returns published posts.
        """
        return self.all().filter(is_active=True, source__is_active=True)
