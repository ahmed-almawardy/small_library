from django.urls.base import reverse_lazy
from abc import ABC, abstractclassmethod
import inspect


'''
   Helpers For initialize test objects/cases 
'''


_AUTHOR_FIELDS = ['name', 'phone', 'email', 'books', 'readers']
_BOOK_FIELDS = ['title', 'author', 'readers']
_READER_FIELDS = ['name', 'phone', 'email', 'books']


class _MainTestHelperClassMethods(ABC):
    @abstractclassmethod
    def fields(self):
        ...
  
    @abstractclassmethod
    def pk(self):
        ...

    @abstractclassmethod
    def create(self):
        ...

    @abstractclassmethod
    def get(self):
        ...

    @abstractclassmethod
    def list(self):
        ...

    @abstractclassmethod
    def update(self):
        ...

    @abstractclassmethod
    def delete(self):
        ...


class _TestHelper(_MainTestHelperClassMethods):
    '''
        model's urls generator throught based logic
        {project}:{app}-{action}, [pk,] 
    '''

    def __init__(self, pk, model_name, fields) -> None:
        self.fields = fields
        self.pk = pk
        self.model_name = model_name

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, fields):
        self._fields = fields

    def create(self):
        action = inspect.currentframe().f_code.co_name
        path = f'{self.model_name}-{action}'
        return reverse_lazy(path)

    def get(self, pk):
        pk = pk if pk else self.pk
        action = inspect.currentframe().f_code.co_name
        path = f'{self.model_name}-{action}'
        return reverse_lazy(path, kwargs={'pk': pk})

    def update(self, pk):
        pk = pk if pk else self.pk
        action = inspect.currentframe().f_code.co_name
        path = f'{self.model_name}-{action}'
        return reverse_lazy(path, kwargs={'pk': pk})

    def delete(self, pk):
        pk = pk if pk else self.pk
        action = inspect.currentframe().f_code.co_name
        path = f'{self.model_name}-{action}'
        return reverse_lazy(path, kwargs={'pk': pk})

    def list(self):
        action = inspect.currentframe().f_code.co_name
        path = f'{self.model_name}-{action}'
        return reverse_lazy(path)

    @property
    def pk(self):
        return self._pk

    @pk.setter
    def pk(self, pk):
        '''
            change the object pk
        '''
        self._pk = pk


class AutherTestHelper(_TestHelper):
    def __init__(self, pk=None) -> None:
        super().__init__(pk, model_name='author', fields=_AUTHOR_FIELDS)

class ReaderTestHelper(_TestHelper):
    def __init__(self, pk=None) -> None:
        super().__init__(pk, model_name='reader', fields=_READER_FIELDS)

    def books_delete(self, pk):
        return reverse_lazy('reader-books_delete', kwargs={'pk': pk})

class BookTestHelper(_TestHelper):
    def __init__(self, pk=None) -> None:
        super().__init__(pk, model_name='book', fields=_BOOK_FIELDS)

author_helper = AutherTestHelper()
book_helper = BookTestHelper()
reader_helper = ReaderTestHelper()


basic_author_fields = {
            'name': 'author',
            'email': 'author@app.api',
            'phone': '+201122124545',
}

basic_book_fields = {
            'title': 'book 1',
            'author': 1,
}

basic_reader_fields = {
            'name': 'reader',
            'email': 'reader@app.api',
            'phone': '+201122124545',
}