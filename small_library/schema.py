import graphene
import graphene_django
from graphene_django.rest_framework.mutation import SerializerMutation

from rest_framework.exceptions import APIException

from django.shortcuts import (get_object_or_404, get_list_or_404)
from django.core import validators
from django.core.cache import cache

from core.models import (Author, Book, Reader)
from core.validators import (name_no_numbers_symbols, phone_with_plus)
from core.serializers import ReaderWriteSerializer

class BookObject(graphene_django.DjangoObjectType):
    '''
        Serializes a book object
    '''
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'readers',
            'author',
        )

class ReaderObject(graphene_django.DjangoObjectType):
    '''
        Serializes a reader object
    '''
    books_no = graphene.Int()
    class Meta:
        model = Reader
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'books',
            'books_no'
        )


class AuthorObject(graphene_django.DjangoObjectType):
    '''
        Serializeing Author object
    '''
    readers_as_obj = graphene_django.DjangoListField(ReaderObject)
    books = graphene_django.DjangoListField(BookObject)
    books_no = graphene.Int()

    class Meta:
        model = Author
        fields =  (
            'id',
            'name',
            'email',
            'phone',
            'books',
            'books_no',
            'readers_as_obj'
        )



## TODO::Refactor
class Queries(graphene.ObjectType):
    '''
        API Interface for GraphQl Queries
    '''
    authors =  graphene_django.DjangoListField(AuthorObject)
    author_get = graphene.Field(AuthorObject, pk= graphene.NonNull(graphene.ID))

    books =  graphene_django.DjangoListField(BookObject)
    book_get = graphene.Field(BookObject, pk= graphene.NonNull(graphene.ID))

    readers =  graphene_django.DjangoListField(ReaderObject)
    reader_get = graphene.Field(ReaderObject, pk= graphene.NonNull(graphene.ID))

    @staticmethod
    def _find_model_object(model, pk):
        '''
            Returns model object by id
        '''
        Queries._validate_pk(pk)
        return   get_object_or_404(model, pk=pk)

    @staticmethod
    def _validate_pk(pk):
        '''
            If non pk raises Exception
        '''
        if not pk:
            raise APIException('pk is mandatory')

    def resolve_author_get(self, info, pk):
        '''
            Returns  author object
        '''

        return Queries._find_model_object(Author, pk)

    def resolve_book_get(self, info, pk):
        '''
            Returns  book object
        '''
        return Queries._find_model_object(Book, pk)

    def resolve_reader_get(self, info, pk):
        '''
            Returns  book object
        '''
        return Queries._find_model_object(Reader, pk)



# Mutations
class AuthorCreate(graphene.Mutation):
    class Arguments:
        name = graphene.NonNull(graphene.String)
        email = graphene.NonNull(graphene.String)
        phone = graphene.NonNull(graphene.String)
    
    author = graphene.Field(AuthorObject)
    ok = graphene.Boolean()

    def mutate(parent, info, name, email, phone):
        name_no_numbers_symbols(name)
        validators.validate_email(email)
        phone_with_plus(phone)

        author = Author.objects.create(
            name=name, email=email, phone=phone
        )
        return AuthorCreate(author)


class AuthorUpdate(graphene.Mutation):
    class Arguments:
        pk    = graphene.NonNull(graphene.ID)
        name  = graphene.String()
        email = graphene.String()
        phone = graphene.String()

    author = graphene.Field(AuthorObject())
    ok = graphene.Boolean()
  
    def mutate(parent, info, pk, name=None, email=None, phone=None):
        author = Author.objects.filter(pk=pk)
        if name:
            name_no_numbers_symbols(name)
            author.name = name
        if email:
            validators.validate_email(email)
            author.email = email
        if phone:
            phone_with_plus(phone)
            author.phone = phone
        if books:
            author.books.set(books)

        author = author.first()
        return AuthorUpdate(author=author, ok=True)


class AuthorBooksDelete(graphene.Mutation):
    class Arguments:
        pk    = graphene.NonNull(graphene.ID)
        books = graphene.NonNull(graphene.List(graphene.ID)) 

    ok = graphene.Boolean()

    ## will refactor it
    def mutate(self, info , pk, books):
        '''
            Deletes an author books
        '''
        author = get_object_or_404(Author, pk=pk)
        if books:
            books = author.books.filter(id__in=books)
            if books.exists():
                books.delete()
                return AuthorBooksDelete(ok=True)
        return AuthorBooksDelete(ok=False)


class ReaderMutations(SerializerMutation):
    class Meta:
        serializer_class = ReaderWriteSerializer
        model_operations = 'create', 'update'
        lookup_field = 'id'





class Mutations(graphene.ObjectType):
    author_create = AuthorCreate.Field()
    author_update = AuthorUpdate.Field()
    author_books_delete = AuthorBooksDelete.Field()

    reader_create = ReaderMutations.Field()
    reader_update = ReaderMutations.Field()
    # author_books_delete = AuthorBooksDelete.Field()

    # author_create = AuthorCreate.Field()
    # author_update = AuthorUpdate.Field()



schema = graphene.Schema(query=Queries, mutation=Mutations,auto_camelcase=False)