import graphene
from graphene import Schema
import graphene_django
from rest_framework.exceptions import APIException

from django.shortcuts import (get_object_or_404, get_list_or_404)
from django.core import validators

from core.models import (Author, Book, Reader)
from core.validators import (name_no_numbers_symbols, phone_with_plus)


class BookObject(graphene_django.DjangoObjectType):
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'readers',
            'author',
        )

class ReaderObject(graphene_django.DjangoObjectType):
    class Meta:
        model = Reader
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'books',
        )


class AuthorObject(graphene_django.DjangoObjectType):
    '''
        Serializeing Author object
    '''
    readers_as_obj = graphene_django.DjangoListField(ReaderObject)
    books = graphene_django.DjangoListField(BookObject)
    class Meta:
        model = Author
        fields =  (
            'id',
            'name',
            'email',
            'phone',
            'books',
            'readers_as_obj'
        )



class Queries(graphene.ObjectType):
    '''
        API Interface for GraphQl Queries
    '''
    authors =  graphene_django.DjangoListField(AuthorObject)
    author_get = graphene.Field(AuthorObject, pk= graphene.NonNull(graphene.ID))

    def resolve_author_get(self, info, pk):
        if not pk:
            raise APIException('pk is mandatory')
        response =   get_object_or_404(Author, pk=pk)
        print(response)
        return response

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

        author = author.first()
        return AuthorUpdate(author=author, ok=True)



class Mutations(graphene.ObjectType):
    author_create = AuthorCreate.Field()
    author_update = AuthorUpdate.Field()


schema = Schema(query=Queries, mutation=Mutations,auto_camelcase=False)