from django.conf import settings
from django.core.cache import cache

from rest_framework.generics import (
    CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView)

from core.models import (Author, Book, Reader)
from core.serializers import (AuthorWriteSerializer, AuthorReadSerializer,  BookWriteSerializer,
                              BookReadSerializer, ReaderWriteSerializer, ReaderReadSerializer, ReaderBooksDeleteSerializer)
from core.tasks import make_queryset_key


# Author Views
class BaseAuthorConfig:
    queryset = Author.objects.all()
    # permission_classes = ()
    # authentication_class = ()


class AuthorCreate(BaseAuthorConfig, CreateAPIView):
    '''
        Creates Author
    '''
    serializer_class = AuthorWriteSerializer


class AuthorUpdate(BaseAuthorConfig, UpdateAPIView):
    '''
        Updates Author
    '''
    serializer_class = AuthorWriteSerializer


class AuthorDelete(BaseAuthorConfig, DestroyAPIView):
    '''
        Deletes Author
    '''
    pass


class AuthorGet(BaseAuthorConfig, RetrieveAPIView):
    '''
        Gets Author
    '''

    serializer_class = AuthorReadSerializer


class AuthorList(BaseAuthorConfig, ListAPIView):
    '''
        Lists Authors
    '''
    serializer_class = AuthorReadSerializer

    def get_queryset(self):
        '''
            Get or set cached queryset 
        '''
        cached_queryset_key = make_queryset_key(self.queryset, many=True)
        cached_qs = cache.get(cached_queryset_key)
        if cached_qs:
            return cached_qs
        fresh_qs = super().get_queryset()
        cache.set(cached_queryset_key,  fresh_qs,
                  timeout=settings.DEFAULT_CACHE_TIMEOUT)
        return fresh_qs

# Book Views


class BaseBookConfig:
    queryset = Book.objects.all()


class BookCreate(BaseBookConfig, CreateAPIView):
    '''
        Creates Book
    '''
    serializer_class = BookWriteSerializer


class BookUpdate(BaseBookConfig, UpdateAPIView):
    '''
        Updates Book
    '''
    serializer_class = BookWriteSerializer


class BookGet(BaseBookConfig, RetrieveAPIView):
    '''
        Gets Book
    '''
    serializer_class = BookReadSerializer


class BookList(BaseBookConfig, ListAPIView):
    '''
        Lists Books
    '''
    serializer_class = BookReadSerializer

    # i am going to refactor it
    # i don't like how it looks like
    def get_queryset(self):
        '''
            Get or set cached queryset 
        '''
        cached_queryset_key = make_queryset_key(self.queryset, many=True)
        cached_qs = cache.get(cached_queryset_key)
        if cached_qs:
            return cached_qs
        fresh_qs = super().get_queryset()
        cache.set(cached_queryset_key,  fresh_qs,
                  timeout=settings.DEFAULT_CACHE_TIMEOUT)
        return fresh_qs


class BookDelete(BaseBookConfig, DestroyAPIView):
    '''
        Deletes Book
    '''
    pass


# Book Views
class BaseReaderConfig:
    queryset = Reader.objects.all()


class ReaderCreate(BaseReaderConfig, CreateAPIView):
    '''
        Creates Reader
    '''
    serializer_class = ReaderWriteSerializer


class ReaderUpdate(BaseReaderConfig, UpdateAPIView):
    '''
        Updates Reader
    '''
    serializer_class = ReaderWriteSerializer


class ReaderGet(BaseReaderConfig, RetrieveAPIView):
    '''
        Gets Reader
    '''
    serializer_class = ReaderReadSerializer


class ReaderList(BaseReaderConfig, ListAPIView):
    '''
        Lists Readers
    '''
    serializer_class = ReaderReadSerializer

    def get_queryset(self):
        '''
            Get or set cached queryset 
        '''
        cached_queryset_key = make_queryset_key(self.queryset, many=True)
        cached_qs = cache.get(cached_queryset_key)
        if cached_qs:
            return cached_qs
        fresh_qs = super().get_queryset()
        cache.set(cached_queryset_key,  fresh_qs,
                  timeout=settings.DEFAULT_CACHE_TIMEOUT)
        return fresh_qs


class ReaderDelete(BaseReaderConfig, DestroyAPIView):
    '''
        Deletes Reader
    '''
    pass


class ReaderBooksDelete(BaseReaderConfig, UpdateAPIView):
    serializer_class = ReaderBooksDeleteSerializer

    def put(self, request, *args, **kwargs):
        raise NotImplementedError()
