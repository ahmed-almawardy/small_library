from django.core.cache import cache

from celery import shared_task





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


@shared_task
def refresh_cached_queryset(obj):
    '''
        Refersh all apps querysets Async using celery worker
    '''
    key = make_queryset_key(obj)
    fresh_queryset = obj._meta.model.objects.all() # 5 mins for cache being alive
    cache.set(key, fresh_queryset, timeout=60 * 5)
