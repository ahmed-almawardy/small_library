from django.dispatch import Signal, receiver
from django.db.models.signals import pre_save, post_delete, post_save
from django.core.cache import cache

from core.models import (Author, Book, Reader)
from core import tasks

@receiver(post_save, sender=Reader)
@receiver(post_save, sender=Author)
@receiver(post_save, sender=Book)
def refresh_cached_queryset(signal, sender, instance, created, **kwargs):
    '''
        Interface for cache refresher
    '''
    if created:
        tasks.refresh_cached_queryset(instance)