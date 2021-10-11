from rest_framework import serializers

from core.models import Author, Book, Reader


class AuthorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'name',
            'email',
            'phone',
            'books',
        )

class AuthorReadSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True)
    class Meta:
        model = Author
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'books',
            'readers'
        )

        extra_kwargs= {
            'name':  {'read_only': True},
            'email': {'read_only': True},
            'phone': {'read_only': True},
        }
    
    def create(self, validated_data):
        raise NotImplementedError()
    
    def update(self, instance, validated_data):
        raise NotImplementedError()


class BookWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Book
        fields = (
            'title',
            'author'
        )
    

class BookReadSerializer(serializers.ModelSerializer):
    readers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'author',
            'readers',
            'created_at',
            'serial_no'
        )

        extra_kwargs= {
            'title' : {'read_only': True},
            'author' : {'read_only': True},
            'readers' : {'read_only': True},
            'created_at' : {'read_only': True},
            'serial_no' : {'read_only': True},
        }

    
    def create(self, validated_data):
        raise NotImplementedError()
    
    def update(self, instance, validated_data):
        raise NotImplementedError()



class ReaderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = (
            'name',
            'email',
            'phone',
            'books',
        )


class ReaderReadSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Reader
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'books',
            'authors'

        )

        extra_kwargs= {
            'name' : {'read_only': True},
            'email' : {'read_only': True},
            'phone' : {'read_only': True},
            'books' : {'read_only': True},
        }


class ReaderBooksDeleteSerializer(serializers.Serializer):
    books = serializers.PrimaryKeyRelatedField(
        queryset= Book.objects.all(), many=True
    )

    def update(self, instance, validated_data):
        books_remove = validated_data['books']
        for book in instance.books.all():
            if book in books_remove:
                instance.books.remove(book)

        return instance