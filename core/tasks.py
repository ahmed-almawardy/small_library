from re import L
from django.core.cache import cache

from celery import shared_task
from django.db.models.query import QuerySet





def make_queryset_key(obj, many=False):
    '''
        Generate key for each app using its model name
    '''
    if many:
        key = obj.model.__name__
    else:
        key = obj._meta.model.__name__
        
    key += "_qs"
    return key

#TODO::Refactor
def get_set_cache_for_list(model, default_queryset=None):
    '''
        Returns a cached value if any or just makes a new one
        if there  a default queryset it will be consider as cahce queryset regredless if there is any value or not
    '''
    key = make_queryset_key(model)
    if default_queryset and isinstance(default_queryset, QuerySet):
        cache.set(key, default_queryset)
    elif not cache.get(key):
        cache.set(key, model.objects.all())
    return cache.get(key)
     

@shared_task
def refresh_cached_queryset(obj):
    '''
        Refersh all apps querysets Async using celery worker
    '''
    key = make_queryset_key(obj)
    fresh_queryset = obj._meta.model.objects.all() # 5 mins for cache being alive
    cache.set(key, fresh_queryset, timeout=60 * 5)
