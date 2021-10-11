from abc import ABC, abstractmethod
import email

from django.test import TestCase

from rest_framework.test import APIClient

from core.models import Author, Book, Reader
from core.TestHelplers import (
        author_helper, 
        book_helper, 
        reader_helper,
        basic_author_fields, 
        basic_book_fields, 
        basic_reader_fields
    )


class TestObjectMainOperations(ABC):
    @abstractmethod
    def test_create_object_return_201(self): ...

    @abstractmethod
    def test_get_object_return_200(self): ...

    @abstractmethod
    def test_list_objects_return_200(self): ...

    @abstractmethod
    def test_put_object_return_200(self): ...

    @abstractmethod
    def test_patch_object_return_200(self): ...

    @abstractmethod
    def test_delete_object_return_204(self): ...


class TestAuthor(TestObjectMainOperations, TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.author_helper = author_helper

    def test_create_object_return_201(self):
        create_url = self.author_helper.create()
        body = basic_author_fields
        response = self.client.post(create_url, data=body)
        self.assertEqual(
            response.status_code,
            201
        )

    def test_delete_object_return_204(self):
        Author.objects.create(
            **basic_author_fields
        )
        delete_url = self.author_helper.delete(pk=1)
        response = self.client.delete(
            delete_url
        )
        self.assertEqual(response.status_code, 204)

    def test_get_object_return_200(self):
        Author.objects.create(
            **basic_author_fields
        )
        get_url = self.author_helper.get(pk=1)
        response = self.client.get(
            get_url
        )
        self.assertEqual(response.status_code, 200)

    def test_list_objects_return_200(self):
        basic_create_fields = basic_author_fields.copy()
        Author.objects.create(
            **basic_create_fields
        )
        basic_create_fields.update(
            email='newemail@domain.extension', phone="+201314222111")
        Author.objects.create(
            **basic_create_fields
        )
        list_url = self.author_helper.list()
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)

    def test_put_object_return_200(self):
        Author.objects.create(
            **basic_author_fields
        )
        put_url = self.author_helper.update(pk=1)
        response = self.client.put(put_url, data={
                                   'name': "new name", 'email': 'newemail@author.api', 'phone': '+20142455454'})
        self.assertEqual(response.status_code, 200)

    def test_patch_object_return_200(self):
        Author.objects.create(
            **basic_author_fields
        )
        patch_url = self.author_helper.update(pk=1)
        response = self.client.patch(patch_url, data={'name': "new name", })
        self.assertEqual(response.status_code, 200)


class BookTest(TestObjectMainOperations, TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book_helper = book_helper
        self.author = Author.objects.create(**basic_author_fields)
        self.author2 = Author.objects.create(
            name='author2', email='author2@author.api', phone="+201311546445")

    def _ready_book_basic(self, **kwargs):
        basic_book_fields_copy = basic_book_fields.copy()
        basic_book_fields_copy.update(author=self.author, **kwargs)
        return basic_book_fields_copy

    def test_create_object_return_201(self):
        create_url = self.book_helper.create()
        data = basic_book_fields
        response = self.client.post(create_url, data=data)
        self.assertEqual(
            response.status_code,
            201
        )

    def test_delete_object_return_204(self):
        Book.objects.create(
            **self._ready_book_basic()
        )
        delete_url = self.book_helper.delete(pk=1)
        response = self.client.delete(
            delete_url
        )
        self.assertEqual(response.status_code, 204)

    def test_get_object_return_200(self):
        Book.objects.create(
            **self._ready_book_basic()
        )
        get_url = self.book_helper.get(pk=1)
        response = self.client.get(
            get_url
        )
        self.assertEqual(response.status_code, 200)

    def test_list_objects_return_200(self):
        basic_create_fields = basic_book_fields.copy()
        Book.objects.create(
            **self._ready_book_basic()
        )
        basic_create_fields.update(
            email='newemail@domain.extension', phone="+201314222111")
        Book.objects.create(
            **self._ready_book_basic(title="new title")
        )
        list_url = self.book_helper.list()
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)

    def test_put_object_return_200(self):
        Book.objects.create(
            **self._ready_book_basic()
        )

        put_url = self.book_helper.update(pk=1)
        response = self.client.put(
            put_url, data={'title': "new name", 'author': 2, })
        self.assertEqual(response.status_code, 200)

    def test_patch_object_return_200(self):
        Book.objects.create(
            **self._ready_book_basic()
        )
        patch_url = self.book_helper.update(pk=1)
        response = self.client.patch(patch_url, data={'title': "new title", })
        self.assertEqual(response.status_code, 200)


class ReaderTest(TestObjectMainOperations, TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.reader_helper = reader_helper
        self.author = self._create_author()
        self.author2 = self._create_author(name='author2', email='author2@author.api', phone="+201456487856")
        self.book = self._create_book(author=self.author)
        self.book2 = self._create_book(author=self.author2, title='anthoer book')

    def _create_author(self, **kwargs) -> Author:
        basic_author_fields_copy = basic_author_fields.copy()
        basic_author_fields_copy.update(**kwargs)
        return Author.objects.create(**basic_author_fields_copy)

    def _create_book(self, **kwargs) -> Book:
        basic_book_fields_copy = basic_book_fields.copy()
        basic_book_fields_copy.update(**kwargs)
        return Book.objects.create(**basic_book_fields_copy)

    def _ready_reader_basic(self, **kwargs):
        '''
            make acopy of reader dict with editable option as kwargs argument
        '''
        basic_reader_fields_copy = basic_reader_fields.copy()
        basic_reader_fields_copy.update(**kwargs)
        return basic_reader_fields_copy

    def test_create_object_return_201(self):
        create_url = self.reader_helper.create()
        data = basic_reader_fields
        response = self.client.post(create_url, data=data)
        self.assertEqual(
            response.status_code,
            201
        )

    def test_delete_object_return_204(self):
        Reader.objects.create(
            **self._ready_reader_basic()
        )
        delete_url = self.reader_helper.delete(pk=1)
        response = self.client.delete(
            delete_url
        )
        self.assertEqual(response.status_code, 204)

    def test_get_object_return_200(self):
        Reader.objects.create(
            **self._ready_reader_basic()
        )
        get_url = self.reader_helper.get(pk=1)
        response = self.client.get(
            get_url
        )
        self.assertEqual(response.status_code, 200)

    def test_list_objects_return_200(self):
        Reader.objects.create(
            **self._ready_reader_basic()
        )
        Reader.objects.create(
            **self._ready_reader_basic(email='newemail@domain.extension', phone="+201314222111")
        )
        list_url = self.reader_helper.list()
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)

    def test_put_object_return_200(self):
        Reader.objects.create(
            **self._ready_reader_basic()
        )

        put_url = self.reader_helper.update(pk=1)
        response = self.client.put(
            put_url, data={'name': "new name", 'email': 'newemail@api.com', 'phone': '+20111145444', 'books': []})
        self.assertEqual(response.status_code, 200)

    def test_patch_object_return_200(self):
        Reader.objects.create(
            **self._ready_reader_basic()
        )
        patch_url = self.reader_helper.update(pk=1)
        response = self.client.patch(patch_url, data={'name': "new name", })
        self.assertEqual(response.status_code, 200)

    def test_ptach_reader_books_200(self):
        reader = Reader.objects.create(**self._ready_reader_basic())
        update_url = self.reader_helper.update(pk=reader.pk)
        books_data= {'books': [1,2]}
        response = self.client.patch(
            update_url,
            data=books_data
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_reader_books_200(self):
        reader = Reader.objects.create(**self._ready_reader_basic())
        update_url = self.reader_helper.update(pk=reader.pk)
        books_data= {'books': [2,1]}
        self.client.patch(
            update_url,
            data=books_data
        )

        books_data_erase = {'books': [1]}
        books_delete_url = self.reader_helper.books_delete(pk=reader.pk)
        response = self.client.patch(books_delete_url, data=books_data_erase)
        self.assertEqual(response.status_code, 200)
